/* Copyright (c) 2017 Timothy Savannah
 * Released under the MIT license (see attached LICENSE file).
 */

#ifndef DLLIST_TYPES_H
#define DLLIST_TYPES_H

extern PyTypeObject DLListType[];
extern PyTypeObject DLListNodeType[];
extern PyTypeObject DLListIteratorType[];


/* DLListNode */

typedef struct
{
    PyObject_HEAD
    PyObject *list_weakref;
    PyObject *value;
    PyObject *next;
    PyObject *prev;
} DLListNodeObject;

typedef struct
{
    PyObject_HEAD
    PyObject *first;
    PyObject *last;
    Py_ssize_t size;
    PyObject *weakref_list;
    PyObject *middle;
    Py_ssize_t middle_idx;
} DLListObject;


#endif /* DLLIST_TYPES_H */
