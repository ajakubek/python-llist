/* Copyright (c) 2011-2013 Adam Jakubek, Rafał Gałczyński
 * Copyright (c) 2017 Timothy Savannah
 * Released under the MIT license (see attached LICENSE file).
 */

#include <Python.h>

#include "llist.h"
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
#define PyString_FromString PyUnicode_FromString
#endif

static PyObject *get_version_tuple_object(long major, long minor, long patch)
{

    PyObject *majorO, *minorO, *patchO;
    PyObject *versionTupleObj;

    majorO = PyLong_FromLong(major);
    minorO = PyLong_FromLong(minor);
    patchO = PyLong_FromLong(patch);

    Py_INCREF(majorO);
    Py_INCREF(minorO);
    Py_INCREF(patchO);

    versionTupleObj = PyTuple_New(3);

    PyTuple_SetItem(versionTupleObj, 0, majorO);
    PyTuple_SetItem(versionTupleObj, 1, minorO);
    PyTuple_SetItem(versionTupleObj, 2, patchO);

    Py_INCREF(versionTupleObj);

    return versionTupleObj;
}

static PyObject *get_version_object(const char *versionStr)
{
    PyObject *versionObj;

    versionObj = PyString_FromString(versionStr);

    Py_INCREF(versionObj);

    return versionObj;
}


static void free_version_tuple_object(PyObject *versionTupleObj)
{
    PyObject *majorO, *minorO, *patchO;
    
    majorO = PyTuple_GetItem(versionTupleObj, 0);
    minorO = PyTuple_GetItem(versionTupleObj, 1);
    patchO = PyTuple_GetItem(versionTupleObj, 2);

    Py_DECREF(majorO);
    Py_DECREF(minorO);
    Py_DECREF(patchO);

    Py_DECREF(versionTupleObj);

}

static void free_version_object(PyObject *versionObj)
{

    Py_DECREF(versionObj);
}

PyObject *mod_version_tuple;
PyObject *mod_version;



static void cllist_setup_module(PyObject *mod)
{
    mod_version_tuple = get_version_tuple_object(LLIST_VERSION_MAJOR, LLIST_VERSION_MINOR, LLIST_VERSION_PATCH);
    mod_version = get_version_object(LLIST_VERSION_STR);

    PyModule_AddObject(mod, "__version_tuple__", mod_version_tuple);
    PyModule_AddObject(mod, "__version__", mod_version);

}

static void cllist_free(void *modPtr)
{
    free_version_object(mod_version);
    free_version_tuple_object(mod_version_tuple);
}


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
    cllist_free,                        /* m_free */
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

    cllist_setup_module(m);

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

    cllist_setup_module(m);
    sllist_register(m);
    dllist_register(m);
}

#endif /* PY_MAJOR_VERSION >= 3 */
