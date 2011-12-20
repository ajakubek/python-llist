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

   Returns a new doubly linked list initialized with elements from *iterable*.
   If *iterable* is not specified, the new :class:`DLList` is empty.

   DLList objects support the following methods:

   .. method:: append(x)

      Add *x* to the right side of the list and return inserted
      :class:`DLListNode`.

      Argument *x* might be a :class:`DLListNode`. In that case a new
      node will be created and initialized with the value extracted from *x*.

   .. method:: appendleft(x)

      Add *x* to the left side of the list and return inserted
      :class:`DLListNode`.

      Argument *x* might be a :class:`DLListNode`. In that case a new
      node will be created and initialized with the value extracted from *x*.

   .. method:: appendright(x)

      Add *x* to the right side of the list and return inserted
      :class:`DLListNode` (synonymous with :meth:`append`).

      Argument *x* might be a :class:`DLListNode`. In that case a new
      node will be created and initialized with the value extracted from *x*.

   .. method:: insert(x, [before])

      Add *x* to the right side of the list if *before* is not specified,
      or insert *x* to the left side of :class:`DLListNode` *before*.
      Return inserted :class:`DLListNode`.

      Argument *x* might be a :class:`DLListNode`. In that case a new
      node will be created and initialized with the value extracted from *x*.

      Raises :exc:`TypeError` if *before* is not of type
      :class:`DLListNode`.

      Raises :exc:`ValueError` if *before* does not belong to *self*.

   .. method:: pop()

      Remove and return an element from the right side of the list.

   .. method:: popleft()

      Remove and return an element from the left side of the list.

   .. method:: popright()

      Remove and return an element from the right side of the list
      (synonymous with :meth:`pop`).

   .. method:: remove(node)

      Remove *node* from the list.

      Raises :exc:`TypeError` if *node* is not of type :class:`DLListNode`.

      Raises :exc:`ValueError` if *self* is empty, or *node* does
      not belong to *self*.


   In addition to these methods, DLList supports iteration, ``cmp(l1, l2)``,
   constant time ``len(l)``, and subscript references ``l[1234]``.

   Indexed access has O(n) complexity, but most recently accessed node is
   cached, so that accessing its neighbours is O(1).
   Note that inserting/deleting a node in the middle of the list will
   invalidate this cache.

   Subscript references like ``n = l[1234]`` return a :class:`DLListNode`
   object, and not a value stored at that location.


:class:`DLListNode` objects
---------------------------

.. class:: DLListNode([value])


:class:`DLListIterator` objects
-------------------------------

.. class:: DLListIterator


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

