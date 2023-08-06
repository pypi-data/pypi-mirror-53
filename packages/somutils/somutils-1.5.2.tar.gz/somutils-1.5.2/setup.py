#!/usr/bin/env python
#-*- coding: utf8 -*-

from setuptools import setup

readme = open("README.rst").read()

setup(
    name = "somutils",
    version = "1.5.2",
    description = "Tools we use at Somenergia and can be useful",
    author = "Cesar Lopez Ramirez",
    author_email = "cesar.lopez@somenergia.coop",
    url = 'https://github.com/Som-Energia/somenergia-utils',
    long_description = readme,
    license = 'GNU General Public License v3 or later (GPLv3+)',
    py_modules = [
        "sheetfetcher",
        "dbutils",
        "trace",
        ],
    packages=[
        'somutils',
        ],
    scripts=[
        'venv',
        'activate_wrapper.sh',
        'sql2csv.py',
        'enable_destructive_tests.py',
        ],
    install_requires=[
        'yamlns>=0.7',
        'psycopg2-binary',
        'consolemsg',
        'gspread==0.6.2',
        'oauth2client>=2.0',
        'PyOpenSSL',
        ],
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Environment :: Console',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],
)

