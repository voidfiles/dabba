#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

APP_NAME = 'dabba'
APP_SCRIPT = './legit_r'
VERSION = '0.0.1'


# Grab requirments.
with open('requirements.txt') as f:
    required = f.readlines()

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    APP_NAME,
]

setup(
    name=APP_NAME,
    version=VERSION,
    description='Python Proccessing Pipeline',
    long_description=open('README.md').read() + '\n\n' +
                     open('HISTORY.md').read(),
    author='Alex Kessinger',
    author_email='voidfiles@gmail.com',
    url='http://developers.app.net',
    packages=packages,
    package_data={'': ['LICENSE', 'NOTICE'], 'requests': ['*.pem']},
    package_dir={APP_NAME: APP_NAME},
    include_package_data=True,
    install_requires=required,
    license=open('LICENSE').read(),
    zip_safe=False,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
)