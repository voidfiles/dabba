#!/usr/bin/env python

import os
import sys

import dabba

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'dabba',
]

requires = open('requirements.txt').read().split('\n')

setup(
    name='dabba',
    version=dabba.__version__,
    description='Python Proccessing Pipeline',
    long_description=open('README.md').read() + '\n\n' +
                     open('HISTORY.md').read(),
    author='Alex Kessinger',
    author_email='voidfiles@gmail.com',
    url='http://developers.app.net',
    packages=packages,
    package_data={'': ['LICENSE', 'NOTICE'], 'requests': ['*.pem']},
    package_dir={'dabba': 'dabba'},
    include_package_data=True,
    install_requires=requires,
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