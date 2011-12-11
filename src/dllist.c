#include <Python.h>

/* Implementation of doubly-linked list */

typedef struct
{
    void* value;
    struct dllist_node_t* prev;
    struct dllist_node_t* next;
} dllist_node_t;

typedef struct
{
    dllist_node_t* first;
    dllist_node_t* last;
} dllist_t;


/* Python objects */

/* DLListNode */

typedef struct
{
    PyObject_HEAD
    dllist_node_t* node;
} DLLListNodeObject;


/* DLList */

typedef struct
{
    PyObject_HEAD
    dllist_t* list;
} DLListObject;

static void dllist_dealloc(DLListObject* self)
{
    /* delete list */
    delete_list(self->list);

    self->ob_type->tp_free((PyObject*)self);
}

static PyObject* dllist_new(PyTypeObject* type,
                            PyObject* args,
                            PyObject* kwds)
{
    DLListObject* self;

    self = (DLListObject*)type->tp_alloc(type, 0);
    self->list = NULL;

    return (PyObject*)self;
}

static PyObject* dllist_appendleft(DLListObject* self, PyObject* arg)
{
    Py_RETURN_NONE;
}

static PyObject* dllist_append(DLListObject* self, PyObject* arg)
{
    Py_RETURN_NONE;
}

static PyObject* dllist_insert(DLListObject* self, PyObject* args)
{
    Py_RETURN_NONE;
}

static PyObject* dllist_popleft(DLListObject* self)
{
    Py_RETURN_NONE;
}

static PyObject* dllist_pop(DLListObject* self)
{
    Py_RETURN_NONE;
}

static PyObject* dllist_remove(DLListObject* self, PyObject* arg)
{
    Py_RETURN_NONE;
}

static PyObject* dllist_get_first(DLListObject* self)
{
    Py_RETURN_NONE;
}

static PyObject* dllist_get_last(DLListObject* self)
{
    Py_RETURN_NONE;
}

static PyMethodDef DLListMethods[] =
{
    { "appendleft", (PyCFunction)dllist_appendleft, METH_O,
      "Append element at the beginning of the list" },
    { "append", (PyCFunction)dllist_append, METH_O,
      "Append element at the end of the list" },
    { "insert", (PyCFunction)dllist_insert, METH_VARARGS,
      "Inserts element before node" },
    { "popleft", (PyCFunction)dllist_popleft, METH_NOARGS,
      "Remove first element from the list and return it" },
    { "pop", (PyCFunction)dllist_pop, METH_NOARGS,
      "Remove last element from the list and return it" },
    { "remove", (PyCFunction)dllist_remove, METH_O,
      "Remove element from the list" },
    { NULL },   /* sentinel */
};

static PyGetSetDef DLListGetSetters[] =
{
    { "first", (getter)dllist_get_first, NULL,
      "first node", NULL },
    { "last", (getter)dllist_get_last, NULL,
      "last_node", NULL },
    { NULL },   /* sentinel */
};

static PyTypeObject DLListType =
{
    PyObject_HEAD_INIT(NULL)
    0,                          /* ob_size */
    "llist.DLList",             /* tp_name */
    sizeof(DLListObject),       /* tp_basicsize */
    0,                          /* tp_itemsize */
    (destructor)dllist_dealloc, /* tp_dealloc */
    0,                          /* tp_print */
    0,                          /* tp_getattr */
    0,                          /* tp_setattr */
    0,                          /* tp_compare */
    0,                          /* tp_repr */
    0,                          /* tp_as_number */
    0,                          /* tp_as_sequence */
    0,                          /* tp_as_mapping */
    0,                          /* tp_hash */
    0,                          /* tp_call */
    0,                          /* tp_str */
    0,                          /* tp_getattro */
    0,                          /* tp_setattro */
    0,                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,         /* tp_flags */
    "Doubly linked list",       /* tp_doc */
    0,                          /* tp_traverse */
    0,                          /* tp_clear */
    0,                          /* tp_richcompare */
    0,                          /* tp_weaklistoffset */
    0,                          /* tp_iter */
    0,                          /* tp_iternext */
    DLListMethods,              /* tp_methods */
    0,                          /* tp_members */
    DLListGetSetters,           /* tp_getset */
    0,                          /* tp_base */
    0,                          /* tp_dict */
    0,                          /* tp_descr_get */
    0,                          /* tp_descr_set */
    0,                          /* tp_dictoffset */
    0,                          /* tp_init */
    0,                          /* tp_alloc */
    dllist_new,                 /* tp_new */
};

int dllist_init_type()
{
    DLListType.tp_new = PyType_GenericNew;
    return (PyType_Ready(&DLListType) < 0) ? 1 : 0;
}

void dllist_register(PyObject* module)
{
    Py_INCREF(&DLListType);
    PyModule_AddObject(module, "DLList", (PyObject*)&DLListType);
}
