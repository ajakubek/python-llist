/* Copyright (c) 2017 Timothy Savannah
 * Released under the MIT license (see attached LICENSE file).
 */

#ifndef LLIST_TYPES_H
#define LLIST_TYPES_H

/* Common start to both dllist and sllist */
typedef struct
{
    PyObject_HEAD
    PyObject *value;
    PyObject *next;
} LListNodeObject;

typedef struct
{
    PyObject_HEAD
    PyObject *first;
    PyObject *last;
    Py_ssize_t size;
} LListObject;

#endif /* LLIST_TYPES_H */
