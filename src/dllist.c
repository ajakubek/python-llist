#include <Python.h>
#include <structmember.h>

/* DLListNode */

typedef struct
{
    PyObject_HEAD
    PyObject* value;
    PyObject* prev;
    PyObject* next;
} DLListNodeObject;

static void dllistnode_dealloc(DLListNodeObject* self)
{
    Py_DECREF(self->next);
    Py_DECREF(self->prev);
    Py_DECREF(self->value);

    self->ob_type->tp_free((PyObject*)self);
}

static PyObject* dllistnode_new(PyTypeObject* type,
                                PyObject* args,
                                PyObject* kwds)
{
    DLListNodeObject* self;

    self = (DLListNodeObject*)type->tp_alloc(type, 0);
    if (self == NULL)
        return NULL;

    Py_INCREF(Py_None);
    self->value = Py_None;

    Py_INCREF(Py_None);
    self->prev = Py_None;

    Py_INCREF(Py_None);
    self->next = Py_None;

    return (PyObject*)self;
}

static PyObject* dllistnode_call(PyObject* self,
                                 PyObject* args,
                                 PyObject* kw)
{
    DLListNodeObject* node = (DLListNodeObject*)self;

    Py_INCREF(node->value);
    return node->value;
}

static PyMemberDef DLListNodeMembers[] =
{
    { "value", T_OBJECT_EX, offsetof(DLListNodeObject, value), 0,
      "Value stored in node" },
    { "prev", T_OBJECT_EX, offsetof(DLListNodeObject, prev), READONLY,
      "Previous node" },
    { "next", T_OBJECT_EX, offsetof(DLListNodeObject, next), READONLY,
      "Next node" },
    { NULL },   /* sentinel */
};

static PyTypeObject DLListNodeType =
{
    PyObject_HEAD_INIT(NULL)
    0,                              /* ob_size */
    "llist.DLListNode",             /* tp_name */
    sizeof(DLListNodeObject),       /* tp_basicsize */
    0,                              /* tp_itemsize */
    (destructor)dllistnode_dealloc, /* tp_dealloc */
    0,                              /* tp_print */
    0,                              /* tp_getattr */
    0,                              /* tp_setattr */
    0,                              /* tp_compare */
    0,                              /* tp_repr */
    0,                              /* tp_as_number */
    0,                              /* tp_as_sequence */
    0,                              /* tp_as_mapping */
    0,                              /* tp_hash */
    dllistnode_call,                /* tp_call */
    0,                              /* tp_str */
    0,                              /* tp_getattro */
    0,                              /* tp_setattro */
    0,                              /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,             /* tp_flags */
    "Doubly linked list node",      /* tp_doc */
    0,                              /* tp_traverse */
    0,                              /* tp_clear */
    0,                              /* tp_richcompare */
    0,                              /* tp_weaklistoffset */
    0,                              /* tp_iter */
    0,                              /* tp_iternext */
    0,                              /* tp_methods */
    DLListNodeMembers,              /* tp_members */
    0,                              /* tp_getset */
    0,                              /* tp_base */
    0,                              /* tp_dict */
    0,                              /* tp_descr_get */
    0,                              /* tp_descr_set */
    0,                              /* tp_dictoffset */
    0,                              /* tp_init */
    0,                              /* tp_alloc */
    dllistnode_new,                 /* tp_new */
};


/* DLList */

typedef struct
{
    PyObject_HEAD
    PyObject* first;
    PyObject* last;
    Py_ssize_t size;
} DLListObject;

static void dllist_dealloc(DLListObject* self)
{
    Py_DECREF(self->last);
    Py_DECREF(self->first);

    self->ob_type->tp_free((PyObject*)self);
}

static PyObject* dllist_new(PyTypeObject* type,
                            PyObject* args,
                            PyObject* kwds)
{
    DLListObject* self;

    self = (DLListObject*)type->tp_alloc(type, 0);
    if (self == NULL)
        return NULL;

    Py_INCREF(Py_None);
    self->first = Py_None;

    Py_INCREF(Py_None);
    self->last = Py_None;

    self->size = 0;

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

static Py_ssize_t dllist_len(PyObject* self) 
{ 
    DLListObject* list = (DLListObject*)self;
    return list->size;
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

static PyMemberDef DLListMembers[] =
{
    { "first", T_OBJECT_EX, offsetof(DLListObject, first), READONLY,
      "First node" },
    { "last", T_OBJECT_EX, offsetof(DLListObject, last), READONLY,
      "Next node" },
    { NULL },   /* sentinel */
};

static PySequenceMethods DLListSequenceMethods[] =
{
    dllist_len,                 /* sq_length */
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
    DLListSequenceMethods,      /* tp_as_sequence */
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
    DLListMembers,              /* tp_members */
    0,                          /* tp_getset */
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
    return (PyType_Ready(&DLListType) == 0) ? 1 : 0;
}

void dllist_register(PyObject* module)
{
    Py_INCREF(&DLListType);
    PyModule_AddObject(module, "DLList", (PyObject*)&DLListType);
}
