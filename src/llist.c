/* Copyright (c) 2011-2012 Adam Jakubek, Rafał Gałczyński
 * Released under the MIT license (see attached LICENSE file).
 */

#include <Python.h>

#include "sllist.h"
#include "dllist.h"

static PyMethodDef llist_methods[] =
{
    { NULL }    /* sentinel */
};

#ifndef PyMODINIT_FUNC  /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif

PyMODINIT_FUNC
initllist(void) 
{
    PyObject* m;

    if (!sllist_init_type())
        return;
    if (!dllist_init_type())
        return;

    m = Py_InitModule3("llist", llist_methods,
                       "Singly and doubly linked lists.");

    sllist_register(m);
    dllist_register(m);
}
