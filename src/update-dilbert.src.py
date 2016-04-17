#!/usr/bin/env python

# Dilbert Tools (update-dilbert)
# Copyright (c) 2008-2012 Scott Zeid
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
#
# IMPORTANT NOTE:  PyInstaller is provided through the project's git repository
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
