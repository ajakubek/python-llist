llist - linked lists for CPython
================================

llist is an extension module for CPython providing basic linked list
data structures.
Collections implemented in the llist module perform well in problems
which rely on fast insertions and/or deletions of elements in
the middle of a sequence.
For this kind of workload, they can be significantly faster than
collections.deque or standard Python lists.

This extension requires CPython 2.5 or newer (3.x is supported).
If you are looking for an implementation of linked lists in pure Python,
visit http://github.com/rgsoda/pypy-llist/
The pypy-llist module has the same API as this extension, but is
significantly slower in CPython.

Understanding Linked Lists
Linked lists are an ordered collection of objects. So what makes them different from normal lists? Linked lists differ from lists in the way that they store elements in memory. While lists use a contiguous memory block to store references to their data, linked lists store references as part of their own elements.

Currently llist provides the following types of linked lists:
 - dllist - a doubly linked list
 - sllist - a singly linked list
 
 Practical Applications:
Linked lists serve a variety of purposes in the real world. They can be used to implement (spoiler alert!) queues or stacks as well as graphs. They’re also useful for much more complex tasks, such as lifecycle management for an operating system application.

Full documentation of these classes is available at:
https://ajakubek.github.io/python-llist/index.html

To install this package, either run "pip install llist",
or download it manually from http://pypi.python.org/pypi
then unpack the sources and compile them with "python setup.py install".

The most current development version is available at:
https://github.com/ajakubek/python-llist/

Bugs can be reported at:
https://github.com/ajakubek/python-llist/issues

This software is distributed under the MIT license.
Please see the LICENSE file included in the package for details.

[![Build Status](https://travis-ci.org/ajakubek/python-llist.svg?branch=master)](https://travis-ci.org/ajakubek/python-llist)
