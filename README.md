cllist - C-implemented Linked Lists for Python
==============================================

cllist is an extension module for CPython providing basic linked list
data structures.

Collections implemented in the llist module perform well in problems
which rely on fast insertions, pops, and removal of elements in
the middle of a sequence.

For this kind of workload, they can be significantly faster than
collections.deque or standard Python lists.


This project was forked from https://github.com/ajakubek/python-llist

and adds many features and enhancements to the original, under a new name "cllist".

The cllist version now lives at https://github.com/kata198/python-cllist

If you were using the previous module, you can change to this new module, it is completely backwards (but not forwards) compatible.



Single Linked List
------------------

Singly linked lists are provided by the "sllist" module. This is your basic single-linked list, and might be useful for some scenarios.

A single linked list is far less efficient at everything than the double-linked list implementation.


Double Linked List
------------------

A double-linked list is provided by the "dllist" module.

This provides great performance when doing pops and insertions at random (in the middle), or at either end.

This implementation has been enhanced by implementing a "middle" marker.

This "middle" marker is used when the list size exceeds 10 elements, and is used in all operations which involve walking the list,

which ensures that AT MOST N/4 elements will need to be walked (so the shortest distance from either start, middle, or end is calculated, and walked from there).

This additional feature makes this linked list much more efficient on larger data sets than a standard double-linked list implementation.


Why use a linked list?
----------------------

A linked list should be used when you are going to be adding or removing elements in the middle of the dataset. A standard python list forces the entire list
to be reallocated and copied when such happens, whereas this can do so without reallocating.


