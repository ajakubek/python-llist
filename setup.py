#!/usr/bin/python
# -*- coding: utf-8 -*-

VERSION='0.1'

from distutils.core import setup, Extension

sources=[ 'src/llist.c',
          'src/dllist.c',
          'src/sllist.c',
          ]

setup(name='llist',
      description='Linked list data structures for Python',
      long_description=open('README').read(),
      author=u'Adam Jakubek <ajakubek@gmail.com>, ' \
             u'Rafał Gałczyński <rafal.galczynski@gmail.com>',
      version=VERSION,
      url='https://github.com/ajakubek/python-llist',
      download_url='http://pypi.python.org/pypi/llist/%s' % VERSION,
      license='MIT',
      keywords='linked list, list',
      ext_modules=[ Extension('llist', sources) ],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: C',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      )
