#include <Python.h>

typedef struct
{
    PyObject_HEAD
} llist_DLListObject;

static PyTypeObject llist_DLListType =
{
    PyObject_HEAD_INIT(NULL)
    0,                          /*ob_size*/
    "llist.DLList",             /*tp_name*/
    sizeof(llist_DLListObject), /*tp_basicsize*/
    0,                          /*tp_itemsize*/
    0,                          /*tp_dealloc*/
    0,                          /*tp_print*/
    0,                          /*tp_getattr*/
    0,                          /*tp_setattr*/
    0,                          /*tp_compare*/
    0,                          /*tp_repr*/
    0,                          /*tp_as_number*/
    0,                          /*tp_as_sequence*/
    0,                          /*tp_as_mapping*/
    0,                          /*tp_hash */
    0,                          /*tp_call*/
    0,                          /*tp_str*/
    0,                          /*tp_getattro*/
    0,                          /*tp_setattro*/
    0,                          /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT,         /*tp_flags*/
    "Doubly linked list",       /*tp_doc*/
};

int dllist_init_type()
{
    llist_DLListType.tp_new = PyType_GenericNew;
    return (PyType_Ready(&llist_DLListType) < 0) ? 1 : 0;
}

void dllist_register(PyObject* module)
{
    Py_INCREF(&llist_DLListType);
    PyModule_AddObject(module, "DLList", (PyObject*)&llist_DLListType);
}
