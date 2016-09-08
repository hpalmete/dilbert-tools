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

from __future__ import print_function

import datetime
import re
import time


YEAR_RE = re.compile("^[0-9]{4}[0-9]*$")


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


def firefox_version(today=None):
 """Returns (approximately) the latest major version of Firefox."""
 
 if today != None and not isinstance(today, datetime.date):
  raise TypeError("today must be a datetime.date")
 
 epoch_date = datetime.date(2014, 2, 4)
 epoch_version = 27
 today = today or datetime.date.today()
 days = (today - epoch_date).days
 weeks = days // 7
 cycles = weeks // 6
 return epoch_version + cycles


def user_agent(today=None):
 """Returns a user agent string for (approximately) the latest major version of Firefox."""
 
 tpl = "Mozilla/5.0 (Windows NT 10.0; rv:{v}) Gecko/20100101 Firefox/{v}"
 version = str(firefox_version(today)) + ".0"
 return tpl.format(v=version)


def is_year(s):
 return bool(YEAR_RE.search(s))
