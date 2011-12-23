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
Currently two types of lists are supported: a doubly linked :class:`DLList`
and a singly linked :class:`SLList`.

All data types defined in this module support efficient O(1)) insertion
and removal of elements (except removal in SLList).
Random access to elements using index is O(n). It does however cache the most
recently accessed node which allows O(1) access to consecutive indexes.

:class:`DLList` objects
-----------------------

.. class:: DLList([iterable])

   Return a new doubly linked list initialized with elements from *iterable*.
   If *iterable* is not specified, the new :class:`DLList` is empty.

   DLList objects provide the following attributes:

   .. attribute:: first

      First :class:`DLListNode` object in the list. `None` if list is empty.
      This attribute is read-only.

   .. attribute:: last

      Last :class:`DLListNode` object in the list. `None` if list is empty.
      This attribute is read-only.

   .. attribute:: size

      Number of elements in the list. 0 if list is empty.
      This attribute is read-only.

   DLList objects also support the following methods (all methods below have
   O(1) time complexity):

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

      Remove and return an element's value from the right side of the list.

   .. method:: popleft()

      Remove and return an element's value from the left side of the list.

   .. method:: popright()

      Remove and return an element's value from the right side of the list
      (synonymous with :meth:`pop`).

   .. method:: remove(node)

      Remove *node* from the list. Returns *node's* value.

      Raises :exc:`TypeError` if *node* is not of type :class:`DLListNode`.

      Raises :exc:`ValueError` if *self* is empty, or *node* does
      not belong to *self*.


   In addition to these methods, DLList supports iteration, ``cmp(l1, l2)``,
   constant time ``len(l)``, and subscript references ``l[1234]`` for
   accessing elements by index.

   Indexed access has O(n) complexity, but most recently accessed node is
   cached, so that accessing its neighbours is O(1).
   Note that inserting/deleting a node in the middle of the list will
   invalidate this cache.

   Subscript references like ``n = l[1234]`` return a :class:`DLListNode`
   object, and not a value stored at that location.

   Example:

   .. doctest::

      >>> from llist import DLList, DLListNode

      >>> empty_lst = DLList()          # create an empty list
      >>> print empty_lst
      DLList()

      >>> print len(empty_lst)          # display length of the list
      0
      >>> print empty_lst.size
      0

      >>> print empty_lst.first         # display the first node (nonexistent)
      None
      >>> print empty_lst.last          # display the last node (nonexistent)
      None

      >>> lst = DLList([1, 2, 3])       # create and initialize a list
      >>> print lst                     # display elements in the list
      DLList([1, 2, 3])

      >>> print len(lst)                # display length of the list
      3
      >>> print lst.size
      3

      >>> print lst[0]                  # access nodes by index
      DLListNode(1)
      >>> print lst[1]
      DLListNode(2)
      >>> print lst[2]
      DLListNode(3)

      >>> node = lst.first              # get the first node (same as lst[0])
      >>> print node
      DLListNode(1)

      >>> print node.value              # get value of node
      1
      >>> print node()                  # get value of node
      1
      >>> print node.prev               # get the previous node (nonexistent)
      None
      >>> print node.next               # get the next node
      DLListNode(2)
      >>> print node.next.value         # get value of the next node
      2

      >>> lst.appendright(4)            # append value to the right side of the list
      <DLListNode(4)>
      >>> print lst
      DLList([1, 2, 3, 4])
      >>> new_node = DLListNode(5)
      >>> lst.appendright(new_node)     # append value from a node
      <DLListNode(5)>
      >>> print lst
      DLList([1, 2, 3, 4, 5])
      >>> lst.appendleft(0)             # append value to the left side of the list
      <DLListNode(0)>
      >>> print lst
      DLList([0, 1, 2, 3, 4, 5])

      >>> node = lst[2]
      >>> lst.insert(1.5, node)         # insert 1.5 before node
      <DLListNode(1.5)>
      >>> print lst
      DLList([0, 1, 1.5, 2, 3, 4, 5])
      >>> lst.insert(6)                 # append value to the right side of the list
      <DLListNode(6)>
      >>> print lst
      DLList([0, 1, 1.5, 2, 3, 4, 5, 6])

      >>> lst.popleft()                 # remove leftmost node from the list
      <DLListNode(0)>
      >>> print lst
      DLList([1, 1.5, 2, 3, 4, 5, 6])
      >>> lst.popright()                # remove rightmost node from the list
      <DLListNode(6)>
      >>> print lst
      DLList([1, 1.5, 2, 3, 4, 5])
      >>> node = lst[1]
      >>> lst.remove(node)              # remove 2nd node from the list
      <DLListNode(1.5)>
      >>> print lst
      DLList([1, 2, 3, 4, 5])
      >>> foreign_node = DLListNode()   # create an unassigned node
      >>> lst.remove(foreign_node)      # try to remove node not present in the list
      Traceback (most recent call last):
        File "/usr/lib/python2.6/doctest.py", line 1253, in __run
          compileflags, 1) in test.globs
        File "<doctest default[39]>", line 1, in <module>
          lst.remove(foreign_node)
      ValueError: DLListNode belongs to another list

      >>> cmp(DLList(), DLList([]))     # list comparison (lexicographical order)
      0
      >>> cmp(DLList([1, 2, 3]), DLList([1, 3, 3]))
      -1
      >>> cmp(DLList([1, 2]), DLList([1, 2, 3]))
      -1
      >>> cmp(DLList([1, 2, 3]), DLList())
      1


:class:`DLListNode` objects
---------------------------

.. class:: DLListNode([value])

   Return a new doubly linked list node, initialized (optionally)
   with *value*.

   DLListNode objects provide the following attributes:

   .. attribute:: next

      Next node in the list. This attribute is read-only.

   .. attribute:: prev

      Previous node in the list. This attribute is read-only.

   .. attribute:: value

      Value stored in this node.

   Note that value stored in the node can also be obtained through
   the :meth:`__call__()` method (using standard ``node()`` syntax).


:class:`DLListIterator` objects
-------------------------------

.. class:: DLListIterator

   Return a new doubly linked list iterator.

   DLListIterator objects are not meant to be created by user.
   They are returned by the :meth:`DLList.__iter__()` method to hold
   iteration state.

   Note that iteration using :class:`DLListIterator` interface will
   directly yield values stored in nodes, not :class:`DLListNode`
   objects.

   Example:

   .. doctest::

      >>> from llist import DLList
      >>> lst = DLList([1, 2, 3])
      >>> for value in lst:
      ...     print value * 2,
      2 4 6


:class:`SLList` objects
-----------------------

.. class:: SLList([iterable])

   Return a new singly linked list initialized with elements from *iterable*.
   If *iterable* is not specified, the new :class:`SLList` is empty.

   SLList objects provide the following attributes:

   .. attribute:: first

      First :class:`SLListNode` object in the list. `None` if list is empty.
      This attribute is read-only.

   .. attribute:: last

      Last :class:`SLListNode` object in the list. `None` if list is empty.
      This attribute is read-only.

   .. attribute:: size

      Number of elements in the list. 0 if list is empty.
      This attribute is read-only.

   SLList objects also support the following methods:

   .. method:: append(x)

      Add *x* to the right side of the list and return inserted
      :class:`SLListNode`.

      Argument *x* might be a :class:`SLListNode`. In that case a new
      node will be created and initialized with the value extracted from *x*.

      This method has O(1) complexity.

   .. method:: appendleft(x)

      Add *x* to the left side of the list and return inserted
      :class:`SLListNode`.

      Argument *x* might be a :class:`SLListNode`. In that case a new
      node will be created and initialized with the value extracted from *x*.

      This method has O(1) complexity.

   .. method:: appendright(x)

      Add *x* to the right side of the list and return inserted
      :class:`SLListNode`.

      Argument *x* might be a :class:`SLListNode`. In that case a new
      node will be created and initialized with the value extracted from *x*.

      This method has O(1) complexity.

   .. method:: insert_after(x, node)

      Inserts *x* after *node* and return inserted :class:`SLListNode`.

      Argument *x* might be a :class:`SLListNode`. In that case a new
      node will be created and initialized with the value extracted from *x*.

      Raises :exc:`TypeError` if *node* is not of type :class:`SLListNode`.

      This method has O(1) complexity.

   .. method:: insert_before(x, node)

      Inserts *x* before *node* and return inserted :class:`SLListNode`.

      Argument *x* might be a :class:`SLListNode`. In that case a new
      node will be created and initialized with the value extracted from *x*.

      Raises :exc:`TypeError` if *node* is not of type :class:`SLListNode`.

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

      Raises :exc:`TypeError` if *node* is not of type :class:`SLListNode`.

      Raises :exc:`ValueError` if *self* is empty, or *node* does
      not belong to *self*.

      This method has O(n) time complexity.


:class:`SLListNode` objects
---------------------------

.. class:: SLListNode([value])

   Return a new singly linked list node, initialized (optionally)
   with *value*.

   SLListNode objects provide the following attributes:

   .. attribute:: next

      Next node in the list. This attribute is read-only.

   .. attribute:: value

      Value stored in this node.

   Note that value stored in the node can also be obtained through
   the :meth:`__call__()` method (using standard ``node()`` syntax).


:class:`SLListIterator` objects
-------------------------------

.. class:: SLListIterator

   Return a new singly linked list iterator.

   SLListIterator objects are not meant to be created by user.
   They are returned by the :meth:`SLList.__iter__()` method to hold
   iteration state.

   Note that iteration using :class:`SLListIterator` interface will
   directly yield values stored in nodes, not :class:`SLListNode`
   objects.

   Example:

   .. doctest::

      >>> from llist import SLList
      >>> lst = SLList([1, 2, 3])
      >>> for value in lst:
      ...     print value * 2,
      2 4 6


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

