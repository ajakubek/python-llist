.. llist documentation master file, created by
   sphinx-quickstart on Tue Dec 20 01:58:56 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

:mod:`llist` --- Linked list datatypes for Python
=================================================

.. module:: llist
   :synopsis: Linked list datatypes for Python

.. moduleauthor:: Adam Jakubek <ajakubek@gmail.com>
.. moduleauthor:: Rafał Gałczyński <rafal.galczynski@gmail.com>

This module implements linked list data structures.
Currently two types of lists are supported: a doubly linked :class:`dllist`
and a singly linked :class:`sllist`.

All data types defined in this module support efficient O(1)) insertion
and removal of elements (except removal in sllist).
Random access to elements using index is O(n). It does however cache the most
recently accessed node which allows O(1) access to consecutive indexes.

:class:`dllist` objects
-----------------------

.. class:: dllist([iterable])

   Return a new doubly linked list initialized with elements from *iterable*.
   If *iterable* is not specified, the new :class:`dllist` is empty.

   dllist objects provide the following attributes:

   .. attribute:: first

      First :class:`dllistnode` object in the list. `None` if list is empty.
      This attribute is read-only.

   .. attribute:: last

      Last :class:`dllistnode` object in the list. `None` if list is empty.
      This attribute is read-only.

   .. attribute:: size

      Number of elements in the list. 0 if list is empty.
      This attribute is read-only.

   dllist objects also support the following methods (all methods below have
   O(1) time complexity):

   .. method:: append(x)

      Add *x* to the right side of the list and return inserted
      :class:`dllistnode`.

      Argument *x* might be a :class:`dllistnode`. In that case a new
      node will be created and initialized with the value extracted from *x*.

   .. method:: appendleft(x)

      Add *x* to the left side of the list and return inserted
      :class:`dllistnode`.

      Argument *x* might be a :class:`dllistnode`. In that case a new
      node will be created and initialized with the value extracted from *x*.

   .. method:: appendright(x)

      Add *x* to the right side of the list and return inserted
      :class:`dllistnode` (synonymous with :meth:`append`).

      Argument *x* might be a :class:`dllistnode`. In that case a new
      node will be created and initialized with the value extracted from *x*.

   .. method:: insert(x, [before])

      Add *x* to the right side of the list if *before* is not specified,
      or insert *x* to the left side of :class:`dllistnode` *before*.
      Return inserted :class:`dllistnode`.

      Argument *x* might be a :class:`dllistnode`. In that case a new
      node will be created and initialized with the value extracted from *x*.

      Raises :exc:`TypeError` if *before* is not of type
      :class:`dllistnode`.

      Raises :exc:`ValueError` if *before* does not belong to *self*.

   .. method:: pop()

      Remove and return an element's value from the right side of the list.

   .. method:: popleft()

      Remove and return an element's value from the left side of the list.

   .. method:: popright()

      Remove and return an element's value from the right side of the list
      (synonymous with :meth:`pop`).

   .. method:: remove(node)

      Remove *node* from the list and return the element which was
      stored in it.

      Raises :exc:`TypeError` if *node* is not of type :class:`dllistnode`.

      Raises :exc:`ValueError` if *self* is empty, or *node* does
      not belong to *self*.


   In addition to these methods, dllist supports iteration, ``cmp(l1, l2)``,
   constant time ``len(l)``, and subscript references ``l[1234]`` for
   accessing elements by index.

   Indexed access has O(n) complexity, but most recently accessed node is
   cached, so that accessing its neighbours is O(1).
   Note that inserting/deleting a node in the middle of the list will
   invalidate this cache.

   Subscript references like ``n = l[1234]`` return a :class:`dllistnode`
   object, and not a value stored at that location.

   Example:

   .. doctest::

      >>> from llist import dllist, dllistnode

      >>> empty_lst = dllist()          # create an empty list
      >>> print empty_lst
      dllist()

      >>> print len(empty_lst)          # display length of the list
      0
      >>> print empty_lst.size
      0

      >>> print empty_lst.first         # display the first node (nonexistent)
      None
      >>> print empty_lst.last          # display the last node (nonexistent)
      None

      >>> lst = dllist([1, 2, 3])       # create and initialize a list
      >>> print lst                     # display elements in the list
      dllist([1, 2, 3])

      >>> print len(lst)                # display length of the list
      3
      >>> print lst.size
      3

      >>> print lst[0]                  # access nodes by index
      dllistnode(1)
      >>> print lst[1]
      dllistnode(2)
      >>> print lst[2]
      dllistnode(3)

      >>> node = lst.first              # get the first node (same as lst[0])
      >>> print node
      dllistnode(1)

      >>> print node.value              # get value of node
      1
      >>> print node()                  # get value of node
      1
      >>> print node.prev               # get the previous node (nonexistent)
      None
      >>> print node.next               # get the next node
      dllistnode(2)
      >>> print node.next.value         # get value of the next node
      2

      >>> lst.appendright(4)            # append value to the right side of the list
      <dllistnode(4)>
      >>> print lst
      dllist([1, 2, 3, 4])
      >>> new_node = dllistnode(5)
      >>> lst.appendright(new_node)     # append value from a node
      <dllistnode(5)>
      >>> print lst
      dllist([1, 2, 3, 4, 5])
      >>> lst.appendleft(0)             # append value to the left side of the list
      <dllistnode(0)>
      >>> print lst
      dllist([0, 1, 2, 3, 4, 5])

      >>> node = lst[2]
      >>> lst.insert(1.5, node)         # insert 1.5 before node
      <dllistnode(1.5)>
      >>> print lst
      dllist([0, 1, 1.5, 2, 3, 4, 5])
      >>> lst.insert(6)                 # append value to the right side of the list
      <dllistnode(6)>
      >>> print lst
      dllist([0, 1, 1.5, 2, 3, 4, 5, 6])

      >>> lst.popleft()                 # remove leftmost node from the list
      0
      >>> print lst
      dllist([1, 1.5, 2, 3, 4, 5, 6])
      >>> lst.popright()                # remove rightmost node from the list
      6
      >>> print lst
      dllist([1, 1.5, 2, 3, 4, 5])
      >>> node = lst[1]
      >>> lst.remove(node)              # remove 2nd node from the list
      1.5
      >>> print lst
      dllist([1, 2, 3, 4, 5])
      >>> foreign_node = dllistnode()   # create an unassigned node
      >>> lst.remove(foreign_node)      # try to remove node not present in the list
      Traceback (most recent call last):
        File "/usr/lib/python2.6/doctest.py", line 1253, in __run
          compileflags, 1) in test.globs
        File "<doctest default[39]>", line 1, in <module>
          lst.remove(foreign_node)
      ValueError: dllistnode belongs to another list

      >>> cmp(dllist(), dllist([]))     # list comparison (lexicographical order)
      0
      >>> cmp(dllist([1, 2, 3]), dllist([1, 3, 3]))
      -1
      >>> cmp(dllist([1, 2]), dllist([1, 2, 3]))
      -1
      >>> cmp(dllist([1, 2, 3]), dllist())
      1


:class:`dllistnode` objects
---------------------------

.. class:: dllistnode([value])

   Return a new doubly linked list node, initialized (optionally)
   with *value*.

   dllistnode objects provide the following attributes:

   .. attribute:: next

      Next node in the list. This attribute is read-only.

   .. attribute:: prev

      Previous node in the list. This attribute is read-only.

   .. attribute:: value

      Value stored in this node.

   Note that value stored in the node can also be obtained through
   the :meth:`__call__()` method (using standard ``node()`` syntax).


:class:`dllistiterator` objects
-------------------------------

.. class:: dllistiterator

   Return a new doubly linked list iterator.

   dllistiterator objects are not meant to be created by user.
   They are returned by the :meth:`dllist.__iter__()` method to hold
   iteration state.

   Note that iteration using :class:`dllistiterator` interface will
   directly yield values stored in nodes, not :class:`dllistnode`
   objects.

   Example:

   .. doctest::

      >>> from llist import dllist
      >>> lst = dllist([1, 2, 3])
      >>> for value in lst:
      ...     print value * 2,
      2 4 6


:class:`sllist` objects
-----------------------

.. class:: sllist([iterable])

   Return a new singly linked list initialized with elements from *iterable*.
   If *iterable* is not specified, the new :class:`sllist` is empty.

   sllist objects provide the following attributes:

   .. attribute:: first

      First :class:`sllistnode` object in the list. `None` if list is empty.
      This attribute is read-only.

   .. attribute:: last

      Last :class:`sllistnode` object in the list. `None` if list is empty.
      This attribute is read-only.

   .. attribute:: size

      Number of elements in the list. 0 if list is empty.
      This attribute is read-only.

   sllist objects also support the following methods:

   .. method:: append(x)

      Add *x* to the right side of the list and return inserted
      :class:`sllistnode`.

      Argument *x* might be a :class:`sllistnode`. In that case a new
      node will be created and initialized with the value extracted from *x*.

      This method has O(1) complexity.

   .. method:: appendleft(x)

      Add *x* to the left side of the list and return inserted
      :class:`sllistnode`.

      Argument *x* might be a :class:`sllistnode`. In that case a new
      node will be created and initialized with the value extracted from *x*.

      This method has O(1) complexity.

   .. method:: appendright(x)

      Add *x* to the right side of the list and return inserted
      :class:`sllistnode`.

      Argument *x* might be a :class:`sllistnode`. In that case a new
      node will be created and initialized with the value extracted from *x*.

      This method has O(1) complexity.

   .. method:: insert_after(x, node)

      Inserts *x* after *node* and return inserted :class:`sllistnode`.

      Argument *x* might be a :class:`sllistnode`. In that case a new
      node will be created and initialized with the value extracted from *x*.

      Raises :exc:`TypeError` if *node* is not of type :class:`sllistnode`.

      This method has O(1) complexity.

   .. method:: insert_before(x, node)

      Inserts *x* before *node* and return inserted :class:`sllistnode`.

      Argument *x* might be a :class:`sllistnode`. In that case a new
      node will be created and initialized with the value extracted from *x*.

      Raises :exc:`TypeError` if *node* is not of type :class:`sllistnode`.

      This method has O(n) complexity.

   .. method:: pop()

      Remove and return an element's value from the right side of the list.

      This method has O(n) time complexity.

   .. method:: popleft()

      Remove and return an element's value from the left side of the list.

      This method has O(1) time complexity.

   .. method:: popright()

      Remove and return an element's value from the right side of the list.

      This method has O(n) time complexity.

   .. method:: remove(node)

      Remove *node* from the list.

      Raises :exc:`TypeError` if *node* is not of type :class:`sllistnode`.

      Raises :exc:`ValueError` if *self* is empty, or *node* does
      not belong to *self*.

      This method has O(n) time complexity.


:class:`sllistnode` objects
---------------------------

.. class:: sllistnode([value])

   Return a new singly linked list node, initialized (optionally)
   with *value*.

   sllistnode objects provide the following attributes:

   .. attribute:: next

      Next node in the list. This attribute is read-only.

   .. attribute:: value

      Value stored in this node.

   Note that value stored in the node can also be obtained through
   the :meth:`__call__()` method (using standard ``node()`` syntax).


:class:`sllistiterator` objects
-------------------------------

.. class:: sllistiterator

   Return a new singly linked list iterator.

   sllistiterator objects are not meant to be created by user.
   They are returned by the :meth:`sllist.__iter__()` method to hold
   iteration state.

   Note that iteration using :class:`sllistiterator` interface will
   directly yield values stored in nodes, not :class:`sllistnode`
   objects.

   Example:

   .. doctest::

      >>> from llist import sllist
      >>> lst = sllist([1, 2, 3])
      >>> for value in lst:
      ...     print value * 2,
      2 4 6


Changes
=======

.. include:: ../CHANGES


Copyright
=========

This module is copyrighted by Adam Jakubek and Rafał Gałczyński.

It is distributed under the MIT license. Please see the LICENSE file
included in this package for more details.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

