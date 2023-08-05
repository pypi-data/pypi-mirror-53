#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os
import sys
from shutil import rmtree
from setuptools import find_packages, setup, Command
from setuptools.command.test import test as TestCommand


# Package meta-data.
NAME = 'pylistmanager'
DESCRIPTION = 'Manager for various kinds of lists.'
URL = 'https://gitlab.com/sotirisp/pywatchlist'
EMAIL = 'sotirisp@protonmail.com'
AUTHOR = 'Sotiris Papatheodorou'
REQUIRES_PYTHON = '>=3.5'
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
    'xdg',
    'colorama',
]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

TESTS = [
    'pytest',
    'pytest-cov',
    'tox',
]

# ------------------------------------------------

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag -s v{0} -m "Version v{0}"'.format(about['__version__']))
        os.system('git push --tags')
        
        sys.exit()


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    entry_points={
        'console_scripts': ['movielist = pylistmanager.cli_movie:main'],
    },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    tests_require=TESTS,
    include_package_data=True,
    license='GPLv3',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
        'test': Tox,
    },
)

