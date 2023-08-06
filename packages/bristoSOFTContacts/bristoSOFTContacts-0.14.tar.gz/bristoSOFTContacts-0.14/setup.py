#!/usr/bin/python3
#
# Copyright 2016 Kirk A Jackson DBA bristoSOFT all rights reserved.  All methods,
# techniques, algorithms are confidential trade secrets under Ohio and U.S.
# Federal law owned by bristoSOFT.
#
# Kirk A Jackson dba bristoSOFT
# 4100 Executive Park Drive
# Suite 11
# Cincinnati, OH  45241
# Phone (513) 401-9114
# email jacksonkirka@bristosoft.com
#
# The trade name bristoSOFT is a registered trade name with the State of Ohio
# document No. 201607803210.
#
'''

setup.py is a python module that works with python setuptools for packaging and
distribution.

'''
from setuptools import setup, find_packages
setup(
    name="bristoSOFTContacts",
    version="0.14",
    description='bristoSOFT Contacts(tm) is a group oriented contacts managment system.',
    long_description='bristoSOFT Contacts is a group oreinted contact management \
    system.  Its stack is based MVC and includes Qt, Python and PostgreSQL. \
    Users can query groups of contacts by username and password.', 
    author="Kirk A Jackson",
    author_email="jacksonirka@bristosoft.org",
    url="https://bitbucket.org/bristolians/bristosoftcontacts/src/master/", 
    install_requires=[
                                'PyQt5', 
                                'psycopg2', 
                                'PyQt5-sip', 
                                'requests', 
                                'platform', 
                                ], 
    packages=find_packages(),
    classifiers=["Programming Language :: Python :: 3", 
                        "License :: OSI Approved :: MIT License", 
                        "Operating System :: OS Independent", 
                        ],
    keywords='contacts people sales cms friends groups', 
    python_requires='>=3.6', 
    scripts=['main.py'],
)

