# Dilbert Tools (fetch-dilbert)
# Copyright (c) 2008-2016 Scott Zeid
# https://code.s.zeid.me/dilbert-tools
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

import argparse
import json
import logging
import os
import re
import sys
import time
import traceback

from collections import OrderedDict

try:
 import cStringIO as StringIO
except ImportError:
 import StringIO

from PIL import Image

from . import providers

from . import __version__
from .errors import *
from .utils import generate_year_list, is_year


PROVIDERS_LIST = providers.list()

logger = logging.getLogger("fetch-dilbert")


def main(argv=sys.argv, recurse=True):
 if recurse:
  try:
   return main(argv, False)
  except KeyboardInterrupt:
   return 1
 
 setup_logging()
 
 error_msg = "fetch-dilbert: error downloading the strip for " 
 
 p = argparse.ArgumentParser(
  prog='fetch-dilbert',
  description='Downloads a given Dilbert strip or strips.'
 )
 p.add_argument("-V", "--version", action="store_true",
                help="show version number and exit")
 p.add_argument("-v", "--verbose", action="store_true",
                help="show verbose status output")
 p.add_argument("-o", "--output", "--output-dir", dest="output_dir",
                default=".",
                help="directory to save the strip(s) to.  Defaults to the"
                     " current directory.")
 
 # dates argument with custom representation in usage string
 # (also suppressing deprecated arguments from usage)
 dates_metavar = "DATE/YEAR"
 p_usage = re.sub(r"^usage: ", "", p.format_usage()).rstrip()
 p_usage += "\n" + " " * len("usage: " + re.search(r"^([^ ]+ )", p_usage).group(1))
 p_usage += dates_metavar + " [...]"
 p.add_argument("dates", nargs="*", metavar=dates_metavar,
                help="a date in YYYY-MM-DD format, a year, or the word"
                     " \"today\"")
 
 # deprecated date/dates/year arguments
 d = p.add_argument_group("deprecated arguments (use positional arguments"
                          " instead)")
 d.add_argument("-d", "--date", dest="old_date", metavar="DATE",
                help="download one or more strips, separated by a comma.  May"
                     " be in YYYY-MM-DD format, or the word today.")
 d.add_argument("--dates", dest="old_dates", metavar="DATES",
                help="same as above")
 d.add_argument("-y", "--year", dest="old_year", metavar="YEAR",
                help="download all strips from the given year (1989 or later)")
 
 p.usage = p_usage
 
 try:
  options = p.parse_args(argv[1:])
 except SystemExit as exc:
  return exc.code
 
 if options.version:
  print __version__
  return 0
 
 output_dir = os.path.abspath(os.path.expanduser(os.path.expandvars(options.output_dir)))
 
 verbose = options.verbose
 
 date_args = options.dates[:]

 # handle deprecated arguments
 for mode in ("date", "dates", "year"):
  arg = "old_" + mode
  if hasattr(options, arg) and getattr(options, arg) != None:
   logger.warning("the `--%s` argument is deprecated; use positional arguments"
                  " instead" % mode)
   if mode == "date" or mode == "dates":
    date_args += getattr(options, arg).split(",")
   elif mode == "year":
    date_args += [getattr(options, arg)]
 
 dates = []
 for d in date_args:
  if is_year(d):
   current_year = time.strftime("%Y")
   if d == current_year:
    year_list = generate_year_list(d, "%Y-%m-%d", True)
   else:
    year_list = generate_year_list(d, "%Y-%m-%d")
   dates += year_list
  elif d == "today":
   dates += [time.strftime("%Y-%m-%d")]
  else:
   dates += [d]
 
 if not len(dates):
  print >> sys.stderr, p.format_help()
  print >> sys.stderr, p.prog + ": error: no date/year argument given"
  return 2
 
 failed = []
 for d in dates:
  if verbose:
   print "Fetching strip for " + d + "...",
   sys.stdout.flush()
  try:
   fetch_strip(d, output_dir, _newline_before_warnings=verbose)
  except KeyboardInterrupt:
   raise
  except Exception:
   tb = traceback.format_exc()
   if verbose:
    print "failed!"
   print >> sys.stderr, error_msg + d
   print >> sys.stderr, tb
   failed += [d]
  else:
   if verbose:
    print "done!"
 if failed:
  if len(failed) == 1:
   print >> sys.stderr, "fetch-dilbert: there was a problem while downloading one strip:"
  else:
   print >> sys.stderr, "fetch-dilbert: there were problems while downloading %s strips:" % str(len(failed))
  print >> sys.stderr, " " + ", ".join(failed)


def fetch_strip(date, output_dir, save_strip=True, save_metadata=True,
                _newline_before_warnings=False):
 """Downloads a Dilbert strip and converts it to PNG format."""
 
 any_warnings = [False]
 def warn(message):
  if not any_warnings[0]:
   any_warnings[0] = True
   if _newline_before_warnings:
    print >> sys.stderr
  logger.warning(message)
 
 image_data = None
 metadata = providers.BaseProvider._metadata(date)
 last_provider = None
 last_source_url = None
 any_metadata = False
 
 for Provider in PROVIDERS_LIST:
  if image_data:
   if any_metadata:
    break
   elif not Provider.HAS_METADATA:
    continue
  
  if last_provider:
   warn("%s: trying alternate source `%s`" % (date, Provider.DESCRIPTION))
  
  strip = Provider().get(date, metadata_only=not save_strip)
  last_provider = Provider
  last_source_url = strip.source_url
  
  # update only the output metadata keys that have changed from None to not None
  # or have changed from one non-None value to another non-None value
  for k in strip.metadata:
   if not metadata[k] or (strip.metadata[k] and metadata[k] != strip.metadata[k]):
    metadata[k] = strip.metadata[k]
  
  for k in metadata:
   if k != "date" and metadata[k]:
    any_metadata = True
    break

  if save_strip:
   if strip.image_data and not image_data:
    image_data = strip.image_data
    if any_metadata:
     break
  elif any_metadata:
   break
 
 if not image_data and not any_metadata:
  raise DilbertToolsError("could not find strip image or metadata")
 
 alternate_provider = last_provider != PROVIDERS_LIST[0]
 
 output_file = os.path.join(output_dir, date + ".png")
 meta_file = os.path.join(output_dir, date + ".yml")
 mtime = time.mktime(time.strptime(date, "%Y-%m-%d"))
 
 if save_metadata:
  with open(meta_file, "w") as f:
   f.write("date: %s\n" % metadata["date"])
   f.write("title: %s\n" % (json.dumps(metadata["title"] or None)))
   f.write("tags: %s\n" % json.dumps(metadata["tags"]))
   if alternate_provider:
    f.write("alternate-source: %s\n" % json.dumps(last_source_url))
   if metadata["transcript"]:
    f.write("transcript: |\n %s\n" % metadata["transcript"].rstrip().replace("\n", "\n "))
   else:
    f.write("transcript: null\n")
  os.utime(meta_file, (mtime, mtime))
 if save_strip:
  if strip:
   image_stringio = StringIO.StringIO(image_data)
   image_pillow = Image.open(image_stringio)
   image_pillow.save(output_file)
   image_stringio.close()
   os.utime(output_file, (mtime, mtime))
  else:
   raise DilbertToolsError("could not find strip image")


if __name__ == "__main__":
 sys.exit(main(sys.argv))
