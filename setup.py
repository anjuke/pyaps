#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import abspath, dirname
from setuptools import find_packages, setup

with open(dirname(abspath(__file__)) + "/VERSION") as f:
    version = f.read().strip()

setup (
    name = "aps",
    version = version,

    package_dir = {"": "src"},
    packages = find_packages("src"),

    install_requires = [
        'pyzmq==13.1.0',
        'msgpack-python==0.3.0'
    ],

    author = "Anjuke Inc.",
    description = "Python APS client libarary",
    url = "http://git.corp.anjuke.com/_aps/pyaps"
)
