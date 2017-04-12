/* Copyright (c) 2017 Timothy Savannah
 * Released under the MIT license (see attached LICENSE file).
 */

#ifndef SLLIST_TYPES_H
#define SLLIST_TYPES_H

int  sllist_init_type(void);
void sllist_register(PyObject* module);

extern PyTypeObject SLListType[];
extern PyTypeObject SLListNodeType[];
extern PyTypeObject SLListIteratorType[];


/* SLListNode */

typedef struct
{
    PyObject_HEAD
    PyObject *list_weakref;
    PyObject *value;
    PyObject *next;
} SLListNodeObject;

typedef struct
{
    PyObject_HEAD
    PyObject *first;
    PyObject *last;
    Py_ssize_t size;
    PyObject *weakref_list;
} SLListObject;

#endif /* SLLIST_TYPES_H */
