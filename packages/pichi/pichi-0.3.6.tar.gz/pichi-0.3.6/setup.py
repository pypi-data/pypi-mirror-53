#!/usr/bin/var python
# -*- coding: utf-8 -*-

from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


try:
    from pichi.version import __version__
except ImportError:
    pass

exec(open('pichi/version.py').read())


setup(
    name='pichi',
    version=__version__,
    description='A utility for generating simple pcap indexes',
    long_description=readme(),
    long_description_content_type='text/x-rst',
    author='c0nch0b4r',
    author_email='lp1.on.fire@gmail.com',
    packages=[
        'pichi'
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='pcap indexer',
    url='https://bitbucket.org/c0nch0b4r/pichi',
    download_url='https://bitbucket.org/c0nch0b4r/pichi/get/' + __version__ + '.tar.gz',
    project_urls={
        'Source': 'https://bitbucket.org/c0nch0b4r/pichi/src'
    },
    python_requires='>=3.6, <4',
    install_requires=[
        'typing'
    ],
    entry_points={
        'console_scripts': ['pichi=pichi.starter:main'],
    },
    include_package_data=True
)
