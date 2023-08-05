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


import csv
import datetime
import sys
from .listitem import *


class LegoSet(ListItem):
    def __init__(self, item='0000-1', quantity=1):
        super().__init__()
        self.item = item
        self.quantity = quantity
        self.name = 'Set Name'
        self.year = datetime.date.today().year
        self.brickset_URI = 'https://brickset.com/sets/'+self.item
        self.rebrickable_URI = 'https://rebrickable.com/sets/'+self.item

    def __str__(self):
        s = [
            str(self.id),
            ') ',
            self.item,
            '\n  Name: ',
            self.name,
            '\n  Year: ',
            str(self.year),
            '\n'
        ]
        if self.tags:
            s.append('  Tags: ')
            [s.append(str(x)+', ') for x in self.tags]
            s.append('\b\b  \n')
        if self.brickset_URI:
            s.append('  Brickset URI: ' + str(self.brickset_URI) + '\n')
        if self.rebrickable_URI:
            s.append('  Rebrickable URI: ' + str(self.rebrickable_URI) + '\n')
        s.append('  Added on: ' + str(self.date_added) + '\n')
        return ''.join(s)


class LegoSets(ListItems):
    def __str__(self):
        s = [str(x)+'\n' for x in self.list]
        return ''.join(s)

    def read(self, fname):
        with open(fname, newline='') as f:
            reader = csv.reader(f)
            try:
                # Skip first line
                next(reader)
                for row in reader:
                    # Item and quantity
                    self.list.append(LegoSet(row[0], row[1]))
                    # ID
                    self.list[-1].id = len(self.list)
                    # Date added
                    self.list[-1].date_added = datetime.date.today()
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(filename,
                                                       reader.line_num, e))


