#!/usr/bin/env python

from setuptools import setup, find_packages

version = '0.1.0'

setup(
    name='invertransforms',
    version=version,
    description='A library which turns torchvision transformations invertible and replayable.',
    author='Gregunz',
    author_email='mail@gregunz.io',
    url='https://github.com/gregunz/invertransforms',
    packages=find_packages(),
    download_url='https://github.com/gregunz/invertransforms/archive/v{}.tar.gz'.format(version),
    keywords=['invertible', 'transforms', 'transformations', 'torchvision', 'data', 'augmentation',
              'replay', 'replayable', 'invertransforms'],
    install_requires=[
        'torch>=1.2.0',
        'torchvision>=0.4.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
    ],
)
