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

#: List of provider class names (sans the trailing "Provider"), sorted from
#: most to least preferred.  All must be contained in modules inside this
#: subpackage whose names are the same as the list items but lowercase.  The
#: modules will be automatically imported and the classes will automatically
#: appear in ``providers.list()``.
_names = [
 "DilbertDotCom",
 "DilbertStore",
 "AMUReprints",
]


import importlib

from collections import OrderedDict as odict

from .base import BaseProvider


_modules = odict()
for i in _names:
 _modules[i] = importlib.import_module("." + i.lower(), __package__)
del i


def list():
 """Returns a list of provider classes.  Each item is an actual class."""
 return [getattr(_modules[i], i + "Provider") for i in _names]
