'''
Author: Laurent Clévy <https://github.com/lclevy>
Created module from firepwd.py: Franz Geffke <m@f-a.nz>
'''

import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1'
PACKAGE_NAME = 'firepwd'

# This is a fork of https://github.com/lclevy/firepwd
URL = 'https://github.com/franzos/firepwd-package'

LICENSE = 'GPL-2.0'
DESCRIPTION = 'firepwd, an open source tool to decrypt Mozilla protected passwords'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = 'text/markdown'

INSTALL_REQUIRES = [
    'PyCryptodome>=3.9.0',
    'pyasn1>=0.4.8'
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    license=LICENSE,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    entry_points = {
        'console_scripts': ['firepwd=firepwd.main:main'],
    },
    packages=find_packages(),
    zip_safe=False
)
