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


def date_from_str(s):
    """Convert a string to a date object.
    
    Args:
        s (str): A string containing a date in the format YYYY-MM-DD.

    Returns:
        date: A datetime.date object.

    Raises:
        ValueError: If the string is in the wrong format or if the date given
        is invalid.
    """

    dt = s.split('-')
    if len(dt) != 3:
        raise ValueError()
    return datetime.date(int(dt[0]), int(dt[1]), int(dt[2]))

def input_loop(process_input, prompt=''):
    while True:
        try:
            s = input(prompt)
            result = process_input(s)
            break
        except ValueError:
            pass
    return result

def input_int(prompt='', min_value=0, max_value=1):
    while True:
        try:
            i = int(input(prompt))
            if i < min_value or i > max_value:
                raise ValueError
            break
        except ValueError:
            print('Enter an integer between ' + str(min_value)
                  + ' and ' + str(max_value))
    return i

def process_yn_input(s):
    yes_answers = ['y', 'Y', 'yes', 'Yes', 'YES']
    no_answers = ['n', 'N', 'no', 'No', 'NO']
    if s in yes_answers:
        return True
    elif s in no_answers:
        return False
    else:
        print('Enter y or n')
        raise ValueError

def process_rating_input(s):
    if s:
        # Get rating and max_rating from a string in the format
        # rating/max_rating
        sub_s = s.split('/')
        rating = float(sub_s[0])
        if len(sub_s) > 1:
           max_rating = float(sub_s[1])
        else:
           max_rating = 10.0
        # Test if rating is inside the bounds
        if rating < 0 or rating > max_rating or max_rating <= 0:
            print('Rating must be a number in the interval [0, '
                  + str(max_rating) + ']')
            raise ValueError
    else:
       rating = -1
       max_rating = 10.0
    return [rating, max_rating]

def process_year_input(s):
    try:
        y = int(s)
        if (y < datetime.MINYEAR or y > datetime.MAXYEAR):
            raise ValueError()
    except ValueError:
        print('Value must be an integer between '
              + str(datetime.MINYEAR) + ' and ' + str(datetime.MAXYEAR))
        raise ValueError
    return y

def process_date_input(s):
    try:
        if s in ['t', 'today', 'T', 'TODAY']:
            d = datetime.date.today()
        elif s in ['y', 'yesterday', 'Y', 'YESTERDAY']:
            d = datetime.date.today() - datetime.timedelta(days=1)
        elif s in ['n', 'never', 'N', 'NEVER'] or not s:
            d = ''
        else:
            d = date_from_str(s)
    except ValueError:
        print('Enter date in YYYY-MM-DD format')
        raise ValueError
    return d

