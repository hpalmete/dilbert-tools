#!/usr/bin/env python

# Dilbert Tools (update-dilbert)
# Copyright (C) 2008-2009 Scott Wallace
# http://code.google.com/p/dilbert-tools/
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
#
# IMPORTANT NOTE:  PyInstaller is provided through the project's SVN repository
# for convenience only.  It is not covered under the above license statement.
# See its source files (e.g. pyinstaller/Build.py) for its license information.

import optparse, os, time, sys

def main():
	'''Handles options and does the magic'''
	p = optparse.OptionParser(
		description='Updates a collection of Dilbert strips.',
		prog='update-dilbert')
	p.add_option(
		"--verbose",
		"-v", 
		action="store_true",
		help="give details about what the program is doing.")
	p.add_option("--path", "-p", default='.', help="path to your Dilbert collection.  Should have one subdirectory for each year of Dilberts you have (e.g. 1999, 2000, etc.), each with one strip for each day of the year, named YYYY-MM-DD.png.")
	options, args = p.parse_args()
	path = os.path.abspath(os.path.expanduser(os.path.expandvars(options.path)))
	if options.verbose == None:
		verbose = False
	else:
		verbose = True
	if update_collection(path, verbose) != True:
		sys.exit(1)
	

def update_collection(path, verbose):
	year = time.strftime("%Y")
	current_year_path = path + "/" + year
	if os.path.isdir(current_year_path) != True or os.path.exists(current_year_path) != True:
		os.mkdir(current_year_path, 0755)
		if verbose == True:
			print "Created directory %s." % current_year_path
	directory_list_raw = os.listdir(current_year_path)
	directory_list_raw.sort()
	directory_list = []
	for f in directory_list_raw:
		directory_list.append(f.replace(".png", ""))
	ytd = generate_year_list(year, "%Y-%m-%d", True)
	needed_dates = []
	for d in ytd:
		if (d in directory_list) == False:
			needed_dates.append(d)
	needed_dates.sort()
	if verbose == True:
		if len(needed_dates) == 0:
			print "You're up to date!"
		elif len(needed_dates) == 1:
			print "Need to get one strip."
		else:
			print "Need to get %s strips." % str(len(needed_dates))
	failed = 0
	for d in needed_dates:
		if verbose == True:
			print "Fetching strip for " + d + "...",
		if fetch_strip(d, current_year_path) != True:
			if verbose == True:
				print "failed!"
			else:
				print "update-dilbert: problem downloading strip for " + d
			failed = failed + 1
		else:
			if verbose == True:
				print "done!"
	if verbose == True and len(needed_dates) > 0:
		print "You're up to date now!"
	if failed == 0:
		return True
	elif failed == 1:
		print "update-dilbert: there was a problem while downloading one strip."
		return False
	elif failed > 1:
		print "update-dilbert: there were problems while downloading %s strips." % str(failed)
		return False

from PIL import Image
import StringIO, os, time, urllib, sys

# Dilbert Tools (common functions)
# Copyright (C) 2008-2009 Scott Wallace
# http://code.google.com/p/dilbert-tools/
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
#
# IMPORTANT NOTE:  PyInstaller is provided through the project's SVN repository
# for convenience only.  It is not covered under the above license statement.
# See its source files (e.g. pyinstaller/Build.py) for its license information.

def fetch_strip(date, output):
	'''Downloads a Dilbert strip, makes it a PNG, and puts it in output.  Requires PIL module (python-imaging package in Ubuntu)'''
	
	try:
		url = urllib.urlopen("http://www.dilbert.com/fast/%s/" % date)
		html = url.read()
		url.close()
		if html != '':
			pieces = html.split('<img src="/dyn/str_strip/0', 1)
			pieces2 = pieces[1].split(".strip.print.gif", 1)
			output_file = output + "/" + date + ".png"
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
	except KeyboardInterrupt:
		print
		sys.exit()
	except:
		return False

def generate_year_list(year, format, todate = False):
	year = int(year)
	last_day = int(time.strftime("%j", time.strptime(str(year) + "-12-31", "%Y-%m-%d")))
	first_dilbert = time.strftime(format, time.strptime("1989-04-16", "%Y-%m-%d"))
	if todate == True:
		days = int(time.strftime("%j"))
	elif last_day == 366:
		days = 366
	else:
		days = 365
	array = []
	while days > 0:
		day_str = time.strftime(format, time.strptime(str(year) + "-" + str(days), "%Y-%j"))
		array.append(day_str)
		if year == 1989 and day_str == first_dilbert:
			days = 0
		else:
			days = days - 1
	array.sort()
	return array

def error(msg, code = 0):
	print msg
	exit(code)

if __name__ == '__main__':
	main()