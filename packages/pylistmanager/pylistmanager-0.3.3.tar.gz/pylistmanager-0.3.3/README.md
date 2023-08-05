# pylistmanager

[![build](https://gitlab.com/sotirisp/pylistmanager/badges/master/build.svg)](https://gitlab.com/sotirisp/pylistmanager/commits/master)
[![coverage](https://gitlab.com/sotirisp/pylistmanager/badges/master/coverage.svg)](https://gitlab.com/sotirisp/pylistmanager/commits/master)

Manage various kinds of lists saved as `.csv` files. So far the only type of
lists implemented are movie lists, managed by movielist. Other types of lists
are planned for the future.

<img src="https://gitlab.com/sotirisp/pylistmanager/raw/master/misc/media/movielist_list.png" width="60%">


## Installation
pylistmanager requires Python 3 and has been tested with Python 3.5+. Test
results with earlier versions of Python are welcome. You can install all the
list managers contained in pylistmanager using pip.
```
pip3 install pylistmanager
```


## movielist 
movielist is a program to manage...movie lists. Movies and their metadata are
saved in a `.csv` file. movielist allows editing and printing that `.csv` file.

### Features
- Ability to store the name, release year, rating, tags and date watched for
  movies in a `.csv` file.
- Display list contents with pretty formatting.
- Add/edit/remove movie entries from a `.csv` file.
- Display only movies matching certain tags.
- Import of movie lists from Letterboxd `.csv` files.
- Automatic generation of Letterboxd/Rotten Tomatoes URLs for each movie
  (experimental).

### Usage
You can see the available commands by running
```
movielist -h
```

To list all movies contained in a file run
```
movielist list
```
The default file is `XDG_DATA_HOME/pymovielist/movies.csv` (usually
`~/.local/share/pymovielist/movies.csv`). You can specify a different file
using the `-f` option.

To add/edit/remove a movie run
```
movielist add
movielist edit
movielist remove
```
respectively. You will then be prompted to select a movie and/or enter the
movie details.

To convert a Letterboxd format `.csv` file into the native `.csv` format run
```
movielist -f /path/to/letterboxd.csv convert
```
CAUTION: the file will be converted in-place, overwriting the previous
contents.


## License
Copyright © 2018 Sotiris Papatheodorou
<br>
<br>
This program is Free Software: You can use, study share and improve it at your
will. Specifically you can redistribute and/or modify it under the terms of the
[GNU General Public License](https://www.gnu.org/licenses/gpl.html) as
published by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

