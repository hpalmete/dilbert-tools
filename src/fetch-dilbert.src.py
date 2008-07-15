#!/usr/bin/env python

# Dilbert Tools (fetch-dilbert)
# Copyright (C) 2008 Scott Wallace
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

import optparse, time

def main():
	'''Handles options and does the magic'''
	error_msg = "fetch-dilbert:  error downloading the strip for "	
	modes = ['date', 'dates', 'year']
	p = optparse.OptionParser(
		description='Downloads a given Dilbert strip or strips.',
		prog='fetch-dilbert')
	p.add_option("--date", "-d", help="download one or more strips, separated by a comma.  May be in YYYY-MM-DD format, or the word today (to download today's strip).")
	p.add_option("--dates", help="same as above.")
	p.add_option("--year", "-y", help="download all strips from YEAR.")
	p.add_option("--output", "-o", default='.', help="directory to save the strip(s) to.  Defaults to the current directory.")
	options, args = p.parse_args()
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
			if fetch_strip(use_date, options.output) != True:
				error(error_msg + use_date)
	elif mode == 'year':
		year = time.strftime("%Y")
		if options.year == year:
			array = generate_year_list(options.year, "%Y-%m-%d", True)
		else:
			array = generate_year_list(options.year, "%Y-%m-%d")
		for d in array:
			if fetch_strip(d, options.output) != True:
				error(error_msg + d)
	else:
		p.print_help()
