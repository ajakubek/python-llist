from distutils.core import setup, Extension

sources=[ 'src/llist.c',
          'src/dllist.c',
          'src/sllist.c',
          ]

setup(name='llist',
      version='0.1',
      ext_modules=[ Extension('llist', sources) ]
      )
