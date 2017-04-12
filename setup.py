#!/usr/bin/env python
# -*- coding: utf-8 -*-

VERSION='1.0.0'

from distutils.core import setup, Extension

sources = ['src/cllist.c',
           'src/dllist.c',
           'src/sllist.c',
           ]

setup(name='llist',
      description='Linked list data structures for Python',
      long_description=open('README').read(),
      author='Timothy Savannah, Adam Jakubek, Rafał Gałczyński',
      author_email='kata198@gmail.com, ajakubek@gmail.com, rafal.galczynski@gmail.com',
      maintainer_email='kata198@gmail.com',
      version=VERSION,
      url='https://github.com/kata198/python-cllist',
      download_url='http://pypi.python.org/pypi/cllist/%s' % VERSION,
      license='MIT',
      keywords=['llist', 'linked', 'double', 'single', 'linked list'],
      ext_modules=[Extension('cllist', sources)],
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: C',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      )
