# Dilbert Tools (update-dilbert)
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
import logging
import os
import sys
import time
import traceback

from collections import OrderedDict as odict

from . import __version__
from .errors import *
from .fetch import fetch_strip
from .utils import generate_year_list


logger = logging.getLogger("update-dilbert")


def main(argv=sys.argv, recurse=True):
 if recurse:
  try:
   return main(argv, False)
  except KeyboardInterrupt:
   return 1
 
 setup_logging()
 
 p = argparse.ArgumentParser(
  prog='update-dilbert',
  description='Updates a collection of Dilbert strips.'
 )
 p.add_argument("--version", "-V", action="store_true",
                help="show version number and exit")
 p.add_argument("--verbose", "-v", action="store_true",
                help="show verbose status output")
 p.add_argument("--path", "-p", default='.',
                help="path to your Dilbert collection.  Should have one"
                     " subdirectory for each year of Dilberts you have"
                     " (e.g. 1999, 2000, etc.), each with one strip for"
                     " each day of the year, named YYYY-MM-DD.png.")
 p.add_argument("--metadata-only", "-m", action="store_true",
                help="only save metadata")
 try:
  options = p.parse_args(argv[1:])
 except SystemExit as exc:
  return exc.code
 
 if options.version:
  print __version__
  return 0
 
 path = os.path.abspath(os.path.expanduser(os.path.expandvars(options.path)))
 
 verbose = options.verbose
 
 if len(update_collection(path, verbose, not options.metadata_only, True)):
  sys.exit(1)
 

def update_collection(path, verbose, save_strips=True, save_metadata=True):
 errors = odict()
 year = time.strftime("%Y")
 current_year_path = os.path.join(path, year)
 if os.path.isdir(current_year_path) != True or os.path.exists(current_year_path) != True:
  os.mkdir(current_year_path, 0755)
  if verbose:
   print "Created directory `%s`." % current_year_path
 directory_list_raw = os.listdir(current_year_path)
 directory_list_raw.sort()
 directory_list = []
 for f in directory_list_raw:
  directory_list.append(f.lower())
 ytd = generate_year_list(year, "%Y-%m-%d", True)
 needed_dates = []
 for d in ytd:
  if d + ".png" not in directory_list or d + ".yml" not in directory_list:
   needed_dates.append(d)
 needed_dates.sort()
 if verbose:
  if len(needed_dates) == 0:
   print "You're up to date!"
  elif len(needed_dates) == 1:
   if save_metadata and not save_strips:
    print "Need to get one strip's metadata."
   else:
    print "Need to get one strip."
  else:
   if save_metadata and not save_strips:
    print "Need to get %s strips' metadata." % str(len(needed_dates))
   else:
    print "Need to get %s strips." % str(len(needed_dates))
 failed = 0
 for d in needed_dates:
  if verbose:
   if save_metadata and not save_strips:
    print "Fetching metadata for " + d + "...",
   else:
    print "Fetching strip for " + d + "...",
    sys.stdout.flush()
  try:
   fetch_strip(d, current_year_path, save_strips, save_metadata,
               _newline_before_warnings=verbose)
  except KeyboardInterrupt:
   raise
  except Exception:
   tb = traceback.format_exc()
   errors[d] = tb
   if verbose:
    print "failed!"
   if save_metadata and not save_strips:
    print >> sys.stderr, "update-dilbert: problem downloading metadata for " + d
   else:
    print >> sys.stderr, "update-dilbert: problem downloading strip for " + d
   print >> sys.stderr, tb
   failed = failed + 1
  else:
   if verbose:
    print "done!"
 if verbose and len(needed_dates) > 0 and not failed:
  print "You're up to date now!"
 if failed == 1:
  if save_metadata and not save_strips:
   print >> sys.stderr, "update-dilbert: there was a problem while downloading one strip's metadata."
  else:
   print >> sys.stderr, "update-dilbert: there was a problem while downloading one strip."
 elif failed > 1:
  if save_metadata and not save_strips:
   print >> sys.stderr, "update-dilbert: there were problems while downloading %s strips' metadata." % str(failed)
  else:
   print >> sys.stderr, "update-dilbert: there were problems while downloading %s strips." % str(failed)
 return errors


if __name__ == "__main__":
 sys.exit(main(sys.argv))
