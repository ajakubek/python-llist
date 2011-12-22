#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup, Extension

sources=[ 'src/llist.c',
          'src/dllist.c',
          'src/sllist.c',
          ]

setup(name='llist',
      description='Linked list data structures for Python',
      author=u'Adam Jakubek <ajakubek@gmail.com>, ' \
             u'Rafał Gałczyński <rafal.galczynski@gmail.com>',
      version='0.1',
      url='https://github.com/ajakubek/python-llist',
      license='MIT',
      ext_modules=[ Extension('llist', sources) ],
      classifiers=[
        'Development Status :: 3 - Alpha'
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: C',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
      )
