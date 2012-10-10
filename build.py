#!/usr/bin/env python

# Dilbert Tools (build script)
# Copyright (c) 2008-2012 Scott Zeid
# http://code.srwz.us/dilbert-tools
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

import optparse, platform, os, shutil

def main():
	p = optparse.OptionParser(
		description='Builds the dilbert-tools suite.',
		prog='build.py')
	p.add_option("--output", "-o", default=None, help="directory to save the resulting files to.  Defaults to unix for Unices and windows for Windows.")
	p.add_option("--no-exes", "-n", default=False, action="store_true", help="do not make EXE files on Windows, but make regular Python files instead.  Only applicable on Windows.")
	options, args = p.parse_args()
	if platform.system() == "Windows":
		windows = True;
	else:
		windows = False;
	
	if options.output != None:
		output = options.output;
	elif windows == True:
		output = 'windows'
	else:
		output = 'unix'
	if windows == True:
		if options.no_exes == False:
			build_by_appending("specs", "src\\fetch-dilbert.src.py", "fetch-dilbert.py")
			build_by_appending("specs", "src\\update-dilbert.src.py", "update-dilbert.py")
			if build_with_pyinstaller(output, "specs\\fetch_windows.spec", "specs\\fetch-dilbert.exe") == True:
				os.remove("specs\\fetch-dilbert.py")
				if build_with_pyinstaller(output, "specs\\update_windows.spec", "specs\\update-dilbert.exe") == True:
					os.remove("specs\\update-dilbert.py")
					exit(0)
				else:
					exit(1)
			else:
				exit(1)
		else:
			build_by_appending(output, "src\\fetch-dilbert.src.py", "fetch-dilbert.py")
			build_by_appending(output, "src\\update-dilbert.src.py", "update-dilbert.py")
	else:
		build_by_appending(output, "src/fetch-dilbert.src.py", "fetch-dilbert")
		build_by_appending(output, "src/update-dilbert.src.py", "update-dilbert")
		

def build_with_pyinstaller(output, spec, spec_target):
	spec_basename = os.path.basename(spec).replace(".spec", "")
	if platform.system() != "Windows":
		return False;
	exit1 = os.system("python pyinstaller\\Configure.py")
	if exit1 == 0:
		exit2 = os.system("python pyinstaller\\Build.py " + spec)
		if exit2 == 0:
			shutil.move(spec_target, output)
			build_dir = "specs\\build" + spec_basename
			for r, d, f in os.walk(build_dir, topdown=False):
				for n in f:
					os.remove(os.path.join(r, n))
				for n in d:
					os.rmdir(os.path.join(r, n))
			os.rmdir(build_dir)
			os.remove("specs\\warn" + spec_basename + ".txt")
			return True
	return False

def build_by_appending(output, source, outfile):
	source_file_open = open(source, "r")
	source_file_str = source_file_open.read()
	source_file_open.close()
	common_file_open = open("src/common.inc.py", "r")
	common_file_str = common_file_open.read()
	common_file_open.close()
	
	output_file = output + "/" + outfile
	output_file_str = source_file_str + "\n" + common_file_str
	output_file_open = open(output_file, "w")
	output_file_open.write(output_file_str)
	output_file_open.close()
	os.chmod(output_file, 0755)

if __name__ == "__main__":
	main()
