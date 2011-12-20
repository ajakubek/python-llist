.. llist documentation master file, created by
   sphinx-quickstart on Tue Dec 20 01:58:56 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to llist's documentation!
=================================

Contents:

.. toctree::
   :maxdepth: 2

:mod:`llist` --- Linked list datatypes for Python
=================================================

.. module:: llist
   :synopsis: Linked list datatypes for Python

.. moduleauthor:: Adam Jakubek <ajakubek@gmail.com>
.. moduleauthor:: Rafał Gałczyński <>

This module implements linked list data structures.
Currently two types of lists are supported: a doubly linked :class:`DLList`
and a singly linked :class:`SLList`.

All data types defined in this module support efficient O(1)) insertion
and removal of elements.
Random access to elements using index is O(n). We do however cache the most
recently accessed node which allows O(1) access to consecutive indexes.

:class:`DLList` objects
-----------------------

.. class:: DLList([iterable])

   Returns a new doubly linked list, optionally initialized with elements from
   *iterable*.

   DLList objects support the following methods:

   .. method:: append(x)

      Add *x* to the right side of the list and return inserted
      :class:`DLListNode`.

   .. method:: appendleft(x)

      Add *x* to the left side of the list and return inserted
      :class:`DLListNode`.

   .. method:: appendright(x)

      Add *x* to the right side of the list and return inserted
      :class `DLListNode` (synonymous with :meth:`append`).

   .. method:: insert(x, [before])

      Add *x* to the right side of the list if *before* is not specified,
      or insert *x* to the left side of :class:`DLListNode` *before*.

      Raises :exc:`TypeError` if *before* is not of type
      :class:`DLListNode`.

      Raises :exc:`ValueError` if *before* does not belong to *self*.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

