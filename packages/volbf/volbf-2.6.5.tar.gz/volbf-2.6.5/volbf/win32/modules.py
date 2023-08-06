# volbf
# Copyright (C) 2007-2013 volbf Foundation
#
# This file is part of volbf.
#
# volbf is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# volbf is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with volbf.  If not, see <http://www.gnu.org/licenses/>.
#

"""
@author:       AAron Walters and Nick Petroni
@license:      GNU General Public License 2.0
@contact:      awalters@4tphi.net, npetroni@4tphi.net
@organization: volbf Foundation
"""

#pylint: disable-msg=C0111
import volbf.win32.tasks as tasks

def lsmod(addr_space):
    """ A Generator for modules """

    for m in tasks.get_kdbg(addr_space).modules():
        yield m
