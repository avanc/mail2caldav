# Copyright (C) 2020 Sven Klomp (mail@klomp.eu)
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

class MergeFailedError(Exception):
  """Exception raised if merge failed.
  Attributes:
      errormessage -- errormessage
  """

  def __init__(self, message, ics):
      self.message = message
      self.ics=ics
      
  def __str__(self):
      return "{message} for {ics}".format(message=self.message, ics=self.ics.decode("utf-8"))
