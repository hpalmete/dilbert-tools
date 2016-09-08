# Dilbert Tools (DilbertStoreProvider)
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

import time

from . import BaseProvider


FIRST_AVAILABLE_STRIP = time.mktime(time.strptime("2008-04-01", "%Y-%m-%d"))


class DilbertStoreProvider(BaseProvider):
 DESCRIPTION = "thedilbertstore.com"
 HAS_IMAGES = True
 HAS_METADATA = False
 
 def get(self, iso_date, metadata_only=False):
  strip = self.Strip(iso_date)
  
  if not metadata_only:
   date_struct = time.strptime(iso_date, "%Y-%m-%d")
   if time.mktime(date_struct) >= FIRST_AVAILABLE_STRIP:
    url_date = time.strftime("%y%m%d", date_struct)
    weekday_type = "s" if date_struct.tm_wday == 6 else "d"
    url_fmt = "http://thedilbertstore.com/images/periodic_content/dilbert/" \
              "dt{url_date}{weekday_type}hct.jpg"
    image_url = url_fmt.format(url_date=url_date, weekday_type=weekday_type)
    strip.source_url = image_url
    resp = self.http.get(image_url)
    strip.image_data = resp.content
  
  return strip
