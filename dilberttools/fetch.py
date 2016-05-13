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
import os
import sys
import time
import urllib

try:
	import cStringIO as StringIO
except ImportError:
	import StringIO

from PIL import Image

from .utils import generate_year_list


def main(argv=sys.argv, recurse=True):
	if recurse:
		try:
			return main(argv, False)
		except KeyboardInterrupt:
			pass
	
	error_msg = "fetch-dilbert: error downloading the strip for " 
	modes = ['date', 'dates', 'year']
	p = argparse.ArgumentParser(
		description='Downloads a given Dilbert strip or strips.',
		prog='fetch-dilbert')
	p.add_argument("--date", "-d", help="download one or more strips, separated by a comma. 	May be in YYYY-MM-DD format, or the word today (to download today's strip).")
	p.add_argument("--dates", help="same as above.")
	p.add_argument("--year", "-y", help="download all strips from YEAR.")
	p.add_argument("--output-dir", "--output", "-o", default='.', help="directory to save the strip(s) to. 	Defaults to the current directory.")
	try:
		options = p.parse_args(argv[1:])
	except SystemExit as exc:
		return exc.code
	output_dir = os.path.abspath(os.path.expanduser(os.path.expandvars(options.output_dir)))
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
			if fetch_strip(use_date, output_dir) != True:
				print >> sys.stderr, error_msg + use_date
				return 1
	elif mode == 'year':
		year = time.strftime("%Y")
		if options.year == year:
			array = generate_year_list(options.year, "%Y-%m-%d", True)
		else:
			array = generate_year_list(options.year, "%Y-%m-%d")
		failed = 0
		for d in array:
			if fetch_strip(d, output_dir) != True:
				print >> sys.stderr, error_msg + d
				failed = failed + 1
		if failed == 1:
			print >> sys.stderr, "fetch-dilbert: there was a problem while downloading one strip."
		elif failed > 1:
			print >> sys.stderr, "fetch-dilbert: there were problems while downloading %s strips." % str(failed)
	else:
		p.print_help()


def fetch_strip(date, output_dir):
	"""Downloads a Dilbert strip and converts it to PNG format."""
	
	try:
		url = urllib.urlopen("http://www.dilbert.com/fast/%s/" % date)
		html = url.read()
		url.close()
		if html != '':
			pieces = html.split('<img src="/dyn/str_strip/0', 1)
			pieces2 = pieces[1].split(".strip.print.gif", 1)
			output_file = output_dir + "/" + date + ".png"
			image = urllib.urlopen("http://www.dilbert.com/dyn/str_strip/0" + pieces2[0] + ".strip.gif")
			strip = image.read()
			image.close()
			if strip != '':
				imagestring = StringIO.StringIO(strip)
				imagedata = Image.open(imagestring)
				imagedata.save(output_file)
				imagestring.close()
				thetime = time.mktime(time.strptime(date, "%Y-%m-%d"))
				os.utime(output_file, (thetime, thetime))
				return True
			else:
				return False
		else:
			return False
	except:
		return False


if __name__ == "__main__":
	sys.exit(main(sys.argv))
