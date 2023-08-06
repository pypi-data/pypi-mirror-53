from os import path
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = '0.9.91'
DISTNAME = 'sqlite_rx'
LICENSE = 'GNU GPLv3'
AUTHOR = 'Abhishek Singh'
MAINTAINER = 'Abhishek Singh'
MAINTAINER_EMAIL = 'aosingh@asu.edu'
DESCRIPTION = ('Python SQLite Client and Server')
URL = 'https://github.com/aosingh/sqlite_rx'

PACKAGES = ['sqlite_rx']

DEPENDENCIES = ['colorlog', 'msgpack-python', 'pyzmq', 'tornado']

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Education',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3.7',
    'Operating System :: POSIX :: Linux',
    'Operating System :: Unix',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS'
]
keywords = 'sqlite client server'


setup(
    name=DISTNAME,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=MAINTAINER_EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    description=DESCRIPTION,
    license=LICENSE,
    url=URL,
    version=VERSION,
    scripts=['bin/curve-keygen'],
    packages=find_packages(exclude=("tests",)),
    package_dir={'sqlite_rx': 'sqlite_rx'},
    install_requires=DEPENDENCIES,
    include_package_data=True,
    classifiers=classifiers,
    keywords=keywords,
)