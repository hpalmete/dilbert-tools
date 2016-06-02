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
import sys
import time
import traceback

from collections import OrderedDict

try:
 import cStringIO as StringIO
except ImportError:
 import StringIO

from PIL import Image

import providers

from . import __version__
from .errors import *
from .utils import generate_year_list


PROVIDERS_LIST = providers.list()

logger = logging.getLogger("fetch-dilbert")


def main(argv=sys.argv, recurse=True):
 if recurse:
  try:
   return main(argv, False)
  except KeyboardInterrupt:
   pass
 
 setup_logging()
 
 error_msg = "fetch-dilbert: error downloading the strip for " 
 modes = ['date', 'dates', 'year']
 
 p = argparse.ArgumentParser(
  prog='fetch-dilbert',
  description='Downloads a given Dilbert strip or strips.'
 )
 p.add_argument("--version", "-V", action="store_true",
                help="show version number and exit")
 p.add_argument("--verbose", "-v", action="store_true",
                help="show verbose status output")
 p.add_argument("--date", "-d",
                help="download one or more strips, separated by a comma.  May"
                     " be in YYYY-MM-DD format, or the word today.")
 p.add_argument("--dates", help="same as above")
 p.add_argument("--year", "-y",
                help="download all strips from the given year (1989 or later)")
 p.add_argument("--output-dir", "--output", "-o", default='.',
                help="directory to save the strip(s) to.  Defaults to the"
                     " current directory.")
 try:
  options = p.parse_args(argv[1:])
 except SystemExit as exc:
  return exc.code
 
 if options.version:
  print __version__
  return 0
 
 output_dir = os.path.abspath(os.path.expanduser(os.path.expandvars(options.output_dir)))
 
 verbose = options.verbose
 
 mode = None
 for i in modes:
  if hasattr(options, i) and getattr(options, i) != None:
   mode = i

 if mode == 'date' or mode == 'dates':
  dates = getattr(options, mode).split(',')
  for d in dates:
   if d == "today":
    use_date = time.strftime("%Y-%m-%d")
   else:
    use_date = d
   if verbose:
    print "Fetching strip for " + use_date + "...",
    sys.stdout.flush()
   try:
    fetch_strip(use_date, output_dir, _newline_before_warnings=verbose)
   except Exception:
    tb = traceback.format_exc()
    if verbose:
     print "failed!"
    print >> sys.stderr, error_msg + use_date
    print >> sys.stderr, tb
    return 1
   else:
    if verbose:
     print "done!"
 elif mode == 'year':
  year = time.strftime("%Y")
  if options.year == year:
   array = generate_year_list(options.year, "%Y-%m-%d", True)
  else:
   array = generate_year_list(options.year, "%Y-%m-%d")
  failed = 0
  for d in array:
   if verbose:
    print "Fetching strip for " + d + "...",
    sys.stdout.flush()
   try:
    fetch_strip(d, output_dir, _newline_before_warnings=verbose)
   except Exception:
    tb = traceback.format_exc()
    if verbose:
     print "failed!"
    print >> sys.stderr, error_msg + d
    print >> sys.stderr, tb
    failed = failed + 1
   else:
    if verbose:
     print "done!"
  if failed == 1:
   print >> sys.stderr, "fetch-dilbert: there was a problem while downloading one strip."
  elif failed > 1:
   print >> sys.stderr, "fetch-dilbert: there were problems while downloading %s strips." % str(failed)
 else:
  print >> sys.stderr, p.format_help()
  print >> sys.stderr, p.prog + ": error: no date/year argument given"
  return 2


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
   if strip.image_data:
    image_data = strip.image_data
    if any_metadata:
     break
  elif any_metadata:
   break
 
 if not image_data and not any_metadata:
  raise DilbertToolsError("could not find strip image or metadata")
 
 alternate_provider = last_provider != PROVIDERS_LIST[0]
 
 output_file = output_dir + "/" + date + ".png"
 meta_file = output_dir + "/" + date + ".yml"
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
