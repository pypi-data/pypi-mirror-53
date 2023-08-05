# !/usr/bin/env python
# coding: utf-8

from setuptools import find_packages
from setuptools import setup

install_requires = [
    'pampy',
    'blinker'
]

setup(
    name='flask_simple_token',
    version='0.0.1',
    description="flask_token generate and verify.",
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
)

