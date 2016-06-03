# Dilbert Tools (BaseProvider)
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

from collections import OrderedDict as odict

import requests

from ..utils import user_agent


DEFAULT_USER_AGENT = user_agent()


class BaseProvider(object):
 """The abstract base class for strip providers.

This cannot be used on its own; it is to be overriden by subclasses for each
strip provider.
"""
 
 #: str:  A terse description of the provider, such as a domain name.
 DESCRIPTION = NotImplemented
 
 #: bool:  Whether or not the provider can find strip images.
 HAS_IMAGES = NotImplemented
 
 #: bool:  Whether or not the provider can find metadata.
 HAS_METADATA = NotImplemented
 
 def get(self, iso_date, metadata_only=False):
  """Gets the strip and metadata for a given date.

Implementations SHOULD use ``self.http`` (a ``requests.Session``) or its alias
``self.https`` to make HTTP(S) requests.

:param iso_date: The strip's date in ISO 8601 format.
:type iso_date: str

:param metadata_only: (optional) Causes only metadata to be downloaded.
                      Implementations MUST respect this option.  MUST default
                      to ``False``.
:type metadata_only: bool

:return: A :class:`BaseProvider.Strip` object containing as much information for
         the requested strip as possible.
:rtype: :class:`BaseProvider.Strip`
"""
  raise NotImplementedError
 
 class Strip(object):
  """Contains information for a strip.

:param iso_date: The strip's date in ISO 8601 format.
:type iso_date: str
"""
  def __init__(self, iso_date):
   #: str:  The URL of the page that was first examined to find the image URL,
   #: or a more human-friendly source.
   self.source_url = None
   
   #: bytes:  The raw image data suitable for passing to PIL.Image.
   self.image_data = None
   
   #: collections.OrderedDict:  The strip's metadata, consisting of the
   #: following keys:
   #: 
   #: * ``date: str`` - The strip's date in ISO 8601 format.
   #: * ``title: str`` - The strip's title, or None.
   #: * ``tags: list`` - The strip's tags, each a str.  Leave empty if no tags.
   #: * ``transcript: str`` - The strip's transcript, or None.
   self.metadata = BaseProvider._metadata(iso_date)
   self.metadata["date"] = iso_date
 
 #: requests.Session:  This should be used to make all HTTP(S) requests.
 http = https = None
 
 # Internal stuffs
 
 def __init__(self):
  self._session = requests.Session()
  self._session.headers["User-Agent"] = DEFAULT_USER_AGENT
  self.http = self.https = self._session
 
 @classmethod
 def _metadata(cls, date, title=None, tags=None, transcript=None):
  if tags is None:
   tags = []
  
  result = odict()
  result["date"] = date
  result["title"] = title
  result["tags"] = tags
  result["transcript"] = transcript
  return result
