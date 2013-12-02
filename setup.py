#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import abspath, dirname
from setuptools import find_packages, setup

with open(dirname(abspath(__file__)) + "/VERSION") as f:
    version = f.read().strip()

setup (
    name="aps",
    version=version,
    url='http://git.corp.anjuke.com/_aps/pyaps',
    author = "Anjuke Inc.",
    anthor_email='webmaster@anjuke.com',
    packages=['aps'],
    platforms='any',
    description = "Python APS client libarary",
    install_requires=[
        'pyzmq==14.0.0',
        'msgpack-python==0.3.0'
    ],
)
