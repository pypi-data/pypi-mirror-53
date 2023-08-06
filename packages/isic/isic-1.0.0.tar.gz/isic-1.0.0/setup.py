#!/usr/bin/env python

import os
import sys

import setuptools


def publish():
    """
    A Shortcut for building the package and pushing it into PyPI.  This is
    lifted entirely from the requests library.
    """
    os.system("rm -vfr build dist")
    os.system("python setup.py build")
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    sys.exit()


# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

if sys.argv[-1] == "publish":
    publish()

setuptools.setup()
