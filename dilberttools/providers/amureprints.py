# Dilbert Tools (AMUReprintsProvider)
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

from bs4 import BeautifulSoup

from . import BaseProvider


class AMUReprintsProvider(BaseProvider):
 DESCRIPTION = "amureprints.com"
 HAS_IMAGES = True
 HAS_METADATA = False
 
 def get(self, iso_date, metadata_only=False):
  strip = self.Strip(iso_date)
  
  if not metadata_only:
   url_date = time.strftime("%m/%d/%Y", time.strptime(iso_date, "%Y-%m-%d"))
   strip.source_url = "http://www.amureprints.com/reprints/dt/%s" % url_date
   resp = self.http.get(strip.source_url)
   html = resp.text
   if html:
    parser = BeautifulSoup(html, "lxml")
    container = parser.find(class_="js-reprint-result")
    image_el = container.find("img", class_="img-responsive")
    image_url = image_el["src"]
    if image_url:
     resp = self.http.get(image_url)
     strip.image_data = resp.content
  
  return strip
