# Dilbert Tools (update-dilbert spec file for Windows)
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

a = Analysis(
	[
		os.path.join(HOMEPATH,'support\\_mountzlib.py'),
		os.path.join(HOMEPATH,'support\\useUnicode.py'),
		'specs\\update-dilbert.py'])
pyz = PYZ(a.pure)
exe = EXE(
	pyz,
	a.scripts,
	a.binaries,
	name='update-dilbert.exe',
	debug=False,
	strip=False,
	upx=False,
	console=True)
