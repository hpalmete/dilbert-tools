# Write the actual Makefile.
# Copyright (C) 2005, Giovanni Bajo
# Based on previous work under copyright (c) 2002 McMillan Enterprises, Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

import os
import string

def writevars(outfp, makevars, target):
    outfp.write("# Makefile generated by freeze.py script\n\n")

    keys = makevars.keys()
    keys.sort()
    for key in keys:
        outfp.write("%s=%s\n" % (key, makevars[key]))
    outfp.write("\nall: %s\n\n" % target)
    outfp.write("\nclean:\n\t-rm -f *.o %s\n" % target)

def writerules(outfp, files, suffix, dflag, target):
    deps = []
    for i in range(len(files)):
        file = files[i]
        if file[-2:] == '.c':
            base = os.path.basename(file)
            dest = base[:-2] + suffix + '.o'
            outfp.write("%s: %s\n" % (dest, file))
            outfp.write("\t$(CC) %s $(CFLAGS) -c %s -o %s\n" % (dflag, file, dest))
            files[i] = dest
            deps.append(dest)

    outfp.write("\n%s: %s\n" % (target, string.join(deps)))
    outfp.write("\t$(CC) %s -o %s $(LDLAST)\n" %
                (string.join(files), target))


