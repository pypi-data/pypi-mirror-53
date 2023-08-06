#!/usr/bin/env python3

"""Set up for the froglabs package."""

from setuptools import find_packages, setup

__copyright__ = 'Copyright 2019 Froglabs, Inc.'

requires = [
    'click',
    'dask',
    'netcdf4',
    'numpy>=1.12',
    'pandas>=0.19.2',
    'requests',
    'six',
    'toolz',
    'tqdm',
    'xarray>=0.12.3',
]

setup(
    name='froglabs',
    version='0.2.0',
    description='Froglabs Toolkit',
    author='Froglabs, Inc',
    author_email='team@froglabs.ai',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'froglabs = froglabs.cli:main',
        ]
    },
    install_requires=requires,
    zip_safe=True,
)
