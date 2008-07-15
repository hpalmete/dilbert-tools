from PIL import Image
import StringIO, os, time, urllib

# Dilbert Tools (common functions)
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

def fetch_strip(date, output):
	'''Downloads a Dilbert strip, makes it a PNG, and puts it in output.  Requires PIL module (python-imaging package in Ubuntu)'''
	
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

def generate_year_list(year, format, todate = False):
	last_day = int(time.strftime("%j", time.strptime(year + "-12-31", "%Y-%m-%d")))
	if todate == True:
		days = int(time.strftime("%j"))
	elif last_day == 366:
		days = 366
	else:
		days = 365
	array = []
	while days > 0:
		array.append(
			time.strftime(format,
			time.strptime(str(year) + "-" + str(days), "%Y-%j")))
		days = days - 1
	array.sort()
	return array

def error(msg, code = 0):
	print msg
	exit(code)

if __name__ == '__main__':
	main()
