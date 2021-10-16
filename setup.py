#!/usr/bin/env python
import codecs
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with codecs.open(os.path.join(os.path.abspath(os.path.dirname(
        __file__)), 'aiosocks2', '__init__.py'), 'r', 'latin1') as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'\r?$",
                             fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


if sys.version_info < (3, 5, 3):
    raise RuntimeError("aiosocks2 requires Python 3.5.3+")


setup(
        name='aiosocks2',
        author='UltrafunkAmsterdam',
        author_email='info@blackhatsecurity.nl',
        version=version,
        license='Apache 2',
        url='https://github.com/ultrafunkamsterdam/aiosocks2',

        description='SOCKS proxy client for asyncio and aiohttp',
        long_description=open("README.rst").read(),
        classifiers=(
        ),
        packages=['aiosocks2'],
        install_requires=[
            'aiohttp>=3.4',
        ]
)
