/* Copyright (c) 2017 Timothy Savannah
 * Released under the MIT license (see attached LICENSE file).
 */

#ifndef LLIST_TYPES_H
#define LLIST_TYPES_H

/* Common start to both dllist and sllist */
typedef struct
{
    PyObject_HEAD
    PyObject *list_weakref;
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


static inline PyObject *llistnode_make(PyTypeObject *llist_type, PyObject *llist, PyObject *value)
{
    LListNodeObject *ret;

    ret = (LListNodeObject *)llist_type->tp_alloc(llist_type, 0);
    if ( ret == NULL )
        return NULL;

    /* A single reference to Py_None is held for the whole
     * lifetime of a node. */
    Py_INCREF(Py_None);

    ret->value = value;

    Py_INCREF(ret->value);

    ret->list_weakref = PyWeakref_NewRef((PyObject *)llist, NULL);
    Py_INCREF(ret->list_weakref);

    return (PyObject *)ret;
}

#endif /* LLIST_TYPES_H */
