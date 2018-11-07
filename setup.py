"""
Setuptools configuration file

(C) 2018 Qualcomm Technologies, Inc.  All rights reserved.

This file based on the example from the PyPA sample project, whose copyright is
included below:

Copyright (c) 2016 The Python Packaging Authority (PyPA)

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
import re
import sys
from os import path
from codecs import open  # i do redefined open pylint: disable=redefined-builtin
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))


# check the supported interpreter version
if sys.version_info[0] != 3:
    sys.exit('Error, only Python 3.x supported')

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as descp_file:
    long_description = descp_file.read()


# read file with given name
def read(*names):
    with open(path.join(here, *names), encoding='utf-8') as fp:
        return fp.read()


def find_version(*file_paths):
    """Method to find current source code version."""
    version_file = read(*file_paths)
    version_match = re.search(r"^version = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


README = open(path.join(here, 'README.md')).read()

setup(
    name='DRS',
    version=find_version("app/", "metadata.py"),
    description='Device Registration System',
    long_description=long_description,

    # project home page
    url='https://github.com/CACF/dirbs_intl_drs_api',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages('app'),
    package_dir={'': 'app'},

    # Do not place third-party / open source dependencies in here. Please
    # place them in requirements.txt. This is to ensure that
    # our package installation doesn't download or install any opensource
    # packages without the cosent of the end user.
    install_requires=[],

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        '': [
            'scripts/*.py',
            'scripts/db/*.py'
        ]
    },

    include_package_data=True,
    zip_safe=False,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    # },
)
