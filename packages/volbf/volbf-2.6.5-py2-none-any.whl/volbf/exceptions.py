# volbf
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

class volbfException(Exception):
    """Generic volbf Specific exception, to help differentiate from other exceptions"""
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class AddrSpaceError(volbfException):
    """Address Space Exception, so we can catch and deal with it in the main program"""
    def __init__(self):
        self.reasons = []
        volbfException.__init__(self, "No suitable address space mapping found")

    def append_reason(self, driver, reason):
        self.reasons.append((driver, reason))

    def __str__(self):
        result = volbfException.__str__(self) + "\nTried to open image as:\n" #pylint: disable-msg=E1101
        for k, v in self.reasons:
            result += " {0}: {1}\n".format(k, v)

        return result

class CacheRelativeURLException(volbfException):
    """Exception for gracefully not saving Relative URLs in the cache"""

class SanityCheckException(volbfException):
    """Exception for failed sanity checks (which can potentially be disabled)"""
