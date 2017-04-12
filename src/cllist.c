/* Copyright (c) 2011-2013 Adam Jakubek, Rafał Gałczyński
 * Copyright (c) 2017 Timothy Savannah
 * Released under the MIT license (see attached LICENSE file).
 */

#include <Python.h>

#include "sllist.h"
#include "dllist.h"

static PyMethodDef cllist_methods[] =
{
    { NULL }    /* sentinel */
};

#ifndef PyMODINIT_FUNC  /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif

#define docstr ("C-extension providing single and double linked lists.")

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef cllist_moduledef = {
    PyModuleDef_HEAD_INIT,
    "cllist",                           /* m_name */
    docstr,                             /* m_doc */
    -1,                                 /* m_size */
    cllist_methods,                     /* m_methods */
    NULL,                               /* m_reload */
    NULL,                               /* m_traverse */
    NULL,                               /* m_clear */
    NULL,                               /* m_free */
};

PyMODINIT_FUNC
PyInit_cllist(void)
{
    PyObject* m;

    if (!sllist_init_type())
        return NULL;
    if (!dllist_init_type())
        return NULL;

    m = PyModule_Create(&cllist_moduledef);

    sllist_register(m);
    dllist_register(m);

    return m;
}

#else

PyMODINIT_FUNC
initcllist(void)
{
    PyObject* m;

    if (!sllist_init_type())
        return;
    if (!dllist_init_type())
        return;

    m = Py_InitModule3("cllist", cllist_methods,
                       docstr);

    sllist_register(m);
    dllist_register(m);
}

#endif /* PY_MAJOR_VERSION >= 3 */
