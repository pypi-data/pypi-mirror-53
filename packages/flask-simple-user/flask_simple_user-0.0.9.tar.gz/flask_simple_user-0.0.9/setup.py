# !/usr/bin/env python
# coding: utf-8

from setuptools import find_packages
from setuptools import setup

install_requires = [
    'nezha',
    'sqlalchemy'
]

setup(
    name='flask_simple_user',
    version='0.0.9',
    description="flask_user use sqlalchemy.",
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
)

