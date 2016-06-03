# Dilbert Tools (providers/__init__)
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

_PROVIDERS = []
_add = lambda p: _PROVIDERS.append(p)


from .base import BaseProvider

# Provider class imports.  Classes are added to the list using _add(), with
# the most preferred provider added first and the least preferred added last.
from .dilbertdotcom import DilbertDotComProvider as p; _add(p)
from .dilbertstore import DilbertStoreProvider as p; _add(p)
from .amureprints import AMUReprintsProvider as p; _add(p)


def list():
 """Returns a list of provider classes.  Each item is an actual class."""
 return _PROVIDERS[:]
