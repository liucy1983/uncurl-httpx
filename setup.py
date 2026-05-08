#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='uncurl-httpx',
    version='0.1.0',
    description='uncurl for httpx, fork from uncurl-requests',
    author='cyliu',
    author_email='liucy1983@gmail.com',
    url='https://github.com/liucy1983/uncurl-httpx',
    entry_points={
        'console_scripts': [
            'uncurl = uncurl.bin:main',
        ],
    },
    install_requires=['pyperclip>=1.9.0'],
    packages=find_packages(exclude=("tests", "tests.*")),
)
