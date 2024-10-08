llist - linked lists for CPython
================================

llist is an extension module for CPython providing basic linked list
data structures.
Collections implemented in the llist module perform well in problems
which rely on fast insertions and/or deletions of elements in
the middle of a sequence.
For this kind of workload, they can be significantly faster than
collections.deque or standard Python lists.

This extension requires CPython 2.7 or newer (3.x is supported).
If you are looking for an implementation of linked lists in pure Python,
visit http://github.com/rgsoda/pypy-llist/
The pypy-llist module has the same API as this extension, but is
significantly slower in CPython.

Currently llist provides the following types of linked lists:
 - dllist - a doubly linked list
 - sllist - a singly linked list

Full documentation of these classes is available at:
https://ajakubek.github.io/python-llist/index.html

To install this package, run "pip install llist".
Alternatively you can also download it manually from http://pypi.python.org/pypi, unpack into a directory and build/install with the following commands:
```
python -m build
pip install .
```
The instruction assumes that the 'build' frontend is already available in site-packages.

The most current development version is available at:
https://github.com/ajakubek/python-llist/

Bugs can be reported at:
https://github.com/ajakubek/python-llist/issues

This software is distributed under the MIT license.
Please see the LICENSE file included in the package for details.

[![Build Status](https://github.com/ajakubek/python-llist/actions/workflows/python-package.yml/badge.svg?branch=master)](https://github.com/ajakubek/python-llist/actions/workflows/python-package.yml?query=branch%3Amaster)
