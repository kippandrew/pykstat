#!/usr/bin/env python

import os
import platform

if os.environ.get('USE_SETUPTOOLS'):
    from setuptools import setup
    setup_kwargs = dict(zip_safe=0)
else:
    from distutils.core import setup
    setup_kwargs = dict()

setup(
    name            = 'kstat',
    version         = '0.0.1',
    url             = 'https://github.com/kippandrew/pykstat',
    author          = 'Andy Kipp',
    author_email    = 'akipp@brightcove.com',
    license         = 'MIT License',
    description     = 'libkstat bindings for Python',
    packages        = ['kstat', 'kstat.stats'],
    **setup_kwargs
)
