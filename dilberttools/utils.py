# Dilbert Tools (utils)
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

import time


def generate_year_list(year, format, todate=False):
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
