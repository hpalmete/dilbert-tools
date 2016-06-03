# Dilbert Tools (DilbertDotComProvider)
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

import re

from bs4 import BeautifulSoup

from ..errors import *

from . import BaseProvider


class DilbertDotComProvider(BaseProvider):
 DESCRIPTION = "dilbert.com"
 HAS_IMAGES = True
 HAS_METADATA = True
 
 def get(self, iso_date, metadata_only=False):
  strip = self.Strip(iso_date)
  meta = strip.metadata
  
  strip.source_url = "http://dilbert.com/strip/%s" % iso_date
  resp = self.http.get(strip.source_url)
  # this provider redirects to the latest strip if a future date is given,
  # and to the earliest strip if a date before the first strip (1989-04-16)
  # is given
  if not re.match(r"/%s/?$" % re.escape(iso_date), resp.url):
   raise NoSuchStripError(iso_date)
  html = resp.text
  if html:
   parser = BeautifulSoup(html, "lxml")
   container = parser.find(class_="img-comic-container")
   image_el = container.find("img", class_="img-comic")
   image_url = image_el["src"]
   title_el = parser.find(class_="comic-title-name")
   meta["title"] = (title_el.text.strip() if title_el else None) or None
   meta["transcript"] = image_el["alt"].strip() if image_el.get("alt", "") else None
   tags_el = parser.find(class_="comic-tags")
   if tags_el:
    for el in tags_el.findAll("a"):
     if el.text:
      meta["tags"] += [el.text.strip()]
   if image_url:
    if not metadata_only:
     resp = self.http.get(image_url)
     strip.image_data = resp.content
  
  return strip
