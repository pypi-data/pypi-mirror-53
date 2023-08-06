#!/usr/bin/env python

import setuptools


with open("README.rst") as f:
    long_description = f.read()

setuptools.setup(
    name="isic",
    version="1.0.4",
    description="A Python wrapper around the UN's ISIC definitions",
    long_description=long_description,
    author="Daniel Quinn",
    author_email="code@danielquinn.org",
    url="https://gitlab.com/workfinder/isic",
    py_modules=["isic"],
    include_package_data=True,
    license="GPL3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
