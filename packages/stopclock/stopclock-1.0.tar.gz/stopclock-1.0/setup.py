#!/usr/bin/env python

# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

with open("README.rst", "r") as readme:
    long_description = readme.read()

install_requires = [
    'monotonic>=0.1',
]

setup(
    name='stopclock',
    version='1.0',
    description='A python package that a stopwatch/stopclock.',
    author="Joshua Harlow",
    author_email='harlowja@gmail.com',
    url='https://github.com/harlowja/stopclock',
    license="ASL 2.0",
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    long_description=long_description,
)
