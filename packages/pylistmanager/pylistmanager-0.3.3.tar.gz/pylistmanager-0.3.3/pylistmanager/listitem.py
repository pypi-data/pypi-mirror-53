# pylistmanager
# Copyright (C) 2018  Sotiris Papatheodorou  (sotirisp@protonmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-


import datetime


class ListItem:
    def __init__(self):
        self.id = 1
        self.name = 'NO NAME'
        self.date_added = datetime.date.today()
        self.tags = []

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def tags_from_str(self, s):
        """Given a string s containing comma-separated tags, place one tag in
        each element of the tag attribute list.
        """
        s = s.rstrip(' ,')
        self.tags = [x.strip() for x in s.split(',')]
        # Remove duplicate keys
        self.tags = list(dict.fromkeys(self.tags))
        self.tags.sort()


class ListItems:
    def __init__(self):
        self.list = []

