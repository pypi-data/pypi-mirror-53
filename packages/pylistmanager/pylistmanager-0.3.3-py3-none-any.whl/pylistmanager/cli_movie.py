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


import argparse
import os
import sys
from pathlib import PurePath
from xdg import XDG_DATA_HOME
import colorama
from .__version__ import __version__
from .movie import *
from .common import *


# Global variables
modes = ['list', 'add', 'delete', 'remove', 'edit', 'convert', 'tags']


def info():
    print(str(PurePath(sys.argv[0]).name) + ' ' + str(__version__))
    print("""Copyright (C) 2018  Sotiris Papatheodorou
License GPLv3: GNU GPL version 3 <https://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.""")


def cli_arg_parser():
    parser = argparse.ArgumentParser(
        description='Movie list manager',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'mode', choices=modes+[x[0] for x in modes], nargs='?', default='list',
        help='l, list     list all movies in the file\n\
a, add      add a single movie to the file\n\
d, delete   delete a single movie from the file\n\
r, remove   alias for d, delete\n\
e, edit     edit a single movie from the file\n\
c, convert  convert the file to the native csv format in-place\n\
t, tags     show only the movies from the file matching some tags\n\
'
    )
    parser.add_argument(
        '-f', '--file', nargs='?', 
        default=str(XDG_DATA_HOME) + '/pylistmanager/movies.csv',
        help='the csv file containing the movie list'
    )
    parser.add_argument(
        '--version', const=True, default=False, action='store_const',
        help='show the version and license information and exit'
    )
    args = parser.parse_args()
    args.file = args.file.strip()
    args.file = os.path.expanduser(args.file)
    return args


def main():
    colorama.init()

    # Parse command line arguments
    args = cli_arg_parser()
    if args.version:
        info()
        return

    # Perform action depending on selected mode
    if args.mode == 'list' or args.mode == 'l':
        # list
        lst = Movies()
        try:
            lst.read(args.file)
        except FileNotFoundError:
            print('File \'' + args.file + '\' could not be opened.')
            print('You can create the file and add a movie to it by running:')
            if args.file == str(XDG_DATA_HOME) + '/pylistmanager/movies.csv':
                print('    movielist add')
            else:
                print('    movielist -f \"' + args.file + '\" add')
            return
        print(lst)
    elif args.mode == 'add' or args.mode == 'a':
        # add
        m = Movie()
        m.read_from_user()
        # Add after confirmation
        confirm = input_loop(process_yn_input,
                             'Add movie and write changes to \''
                             + args.file + '\'? [y/n] ')
        if confirm:
            m.write(args.file)
    elif (args.mode == 'remove' or args.mode == 'r'
            or args.mode == 'delete' or args.mode == 'd'):
        # remove
        lst = Movies()
        try:
            lst.read(args.file)
        except FileNotFoundError:
            print('File \'' + args.file + '\' could not be opened.')
            print('You can create the file and add a movie to it by running:')
            if args.file == str(XDG_DATA_HOME) + '/pylistmanager/movies.csv':
                print('    movielist add')
            else:
                print('    movielist -f \"' + args.file + '\" add')
            return
        print(lst)
        # Movie selection
        selection = input_int('Select movie to delete: ', 1, len(lst.list))
        selection = selection - 1
        print('\nSelected movie details\n')
        print(lst.list[selection])
        # Delete after confirmation
        confirm = input_loop(process_yn_input,
                             'Delete movie and write changes to \''
                             + args.file + '\'? [y/n] ')
        if confirm:
            del lst.list[selection]
            lst.write(args.file, 'w')
    elif args.mode == 'edit' or args.mode == 'e':
        # edit
        lst = Movies()
        try:
            lst.read(args.file)
        except FileNotFoundError:
            print('File \'' + args.file + '\' could not be opened.')
            print('You can create the file and add a movie to it by running:')
            if args.file == str(XDG_DATA_HOME) + '/pylistmanager/movies.csv':
                print('    movielist add')
            else:
                print('    movielist -f \"' + args.file + '\" add')
            return
        print(lst)
        # Movie selection
        selection = input_int('Select movie to edit: ', 1, len(lst.list))
        selection = selection - 1
        # Edit movie data
        lst.list[selection].edit_from_user()
        print('\nChanged movie details\n')
        print(lst.list[selection])
        # Write movie list after confirmation
        confirm = input_loop(process_yn_input, 'Write changes to \''
                             + args.file + '\'? [y/n] ')
        if confirm:
            lst.write(args.file, 'w')
    elif args.mode == 'convert' or args.mode == 'c':
        # convert
        lst = Movies()
        try:
            lst.import_data(args.file)
        except FileNotFoundError:
            print('File \'' + args.file + '\' could not be opened.')
            return
        if len(lst.list) > 0:
            confirm = input_loop(process_yn_input, 'Write changes to \''
                                 + args.file
                                 + '\'? Old contents will be lost. [y/n] ')
            if confirm:
                lst.write(args.file, 'w')
                print('Converted ' + str(len(lst.list))
                      + ' movies from \'' + args.file + '\'')
    elif args.mode == 'tags' or args.mode == 't':
        # tags
        lst = Movies()
        try:
            lst.read(args.file)
        except FileNotFoundError:
            print('File \'' + args.file + '\' could not be opened.')
            print('You can create the file and add a movie to it by running:')
            if args.file == str(XDG_DATA_HOME) + '/pylistmanager/movies.csv':
                print('    movielist add')
            else:
                print('    movielist -f \"' + args.file + '\" add')
            return
        # Tag selection
        s = input('Enter tags to show (comma separated): ')
        s = s.rstrip(' ,')
        tags = [x.strip() for x in s.split(',')]
        tags = list(dict.fromkeys(tags))
        # Iterate over movie list and print if any tags match
        for movie in lst.list:
            for movie_tag in movie.tags:
                if movie_tag in tags:
                    tmp_str = str(movie)
                    for movie_tag2 in movie.tags:
                        if movie_tag2 in tags:
                            tmp_str = tmp_str.replace(movie_tag2,
                                style_search_results + movie_tag2
                                + Style.RESET_ALL)
                    print(tmp_str)
                    break

