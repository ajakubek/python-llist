#include <Python.h>
#include <structmember.h>

staticforward PyTypeObject SLListNodeType;
typedef struct
{
    PyObject_HEAD
    PyObject* value;
    PyObject* next;
} SLListNodeObject;

static void sllistnode_dealloc(SLListNodeObject* self)
{
    Py_DECREF(self->value);
    Py_DECREF(self->next);
    self->ob_type->tp_free((PyObject*)self);
}

static PyObject* sllistnode_new(PyTypeObject* type,
                                PyObject* args,
                                PyObject* kwds)
{
    SLListNodeObject* self;

    self = (SLListNodeObject*)type->tp_alloc(type, 0);
    if (self == NULL)
        return NULL;

    Py_INCREF(Py_None);
    self->value = Py_None;

    Py_INCREF(Py_None);
    self->next = Py_None;

    return (PyObject*)self;
}

static PyObject* sllistnode_call(PyObject* self,
                                 PyObject* args,
                                 PyObject* kw)
{
    SLListNodeObject* node = (SLListNodeObject*)self;

    Py_INCREF(node->value);
    return node->value;
}


static PyMemberDef SLListNodeMembers[] =
{
    { "value", T_OBJECT_EX, offsetof(SLListNodeObject, value), 0,
      "value" },
    { "next", T_OBJECT_EX, offsetof(SLListNodeObject, next), READONLY,
      "next node" },
    { NULL },   /* sentinel */
};


static PyTypeObject SLListNodeType =
{
    PyObject_HEAD_INIT(NULL)
    0,                              /* ob_size */
    "llist.SLListNode",             /* tp_name */
    sizeof(SLListNodeObject),       /* tp_basicsize */
    0,                              /* tp_itemsize */
    (destructor)sllistnode_dealloc, /* tp_dealloc */
    0,                              /* tp_print */
    0,                              /* tp_getattr */
    0,                              /* tp_setattr */
    0,                              /* tp_compare */
    0,                              /* tp_repr */
    0,                              /* tp_as_number */
    0,                              /* tp_as_sequence */
    0,                              /* tp_as_mapping */
    0,                              /* tp_hash */
    sllistnode_call,                /* tp_call */
    0,                              /* tp_str */
    0,                              /* tp_getattro */
    0,                              /* tp_setattro */
    0,                              /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,             /* tp_flags */
    "Singly linked list node",      /* tp_doc */
    0,                              /* tp_traverse */
    0,                              /* tp_clear */
    0,                              /* tp_richcompare */
    0,                              /* tp_weaklistoffset */
    0,                              /* tp_iter */
    0,                              /* tp_iternext */
    0,                              /* tp_methods */
    SLListNodeMembers,              /* tp_members */
    0,                              /* tp_getset */
    0,                              /* tp_base */
    0,                              /* tp_dict */
    0,                              /* tp_descr_get */
    0,                              /* tp_descr_set */
    0,                              /* tp_dictoffset */
    0,                              /* tp_init */
    0,                              /* tp_alloc */
    sllistnode_new,                 /* tp_new */
};



staticforward PyTypeObject SLListType;
typedef struct
{
    PyObject_HEAD
    PyObject* first;
    PyObject* last;
    Py_ssize_t size;
} SLListObject;


static void sllist_dealloc(SLListObject* self)
{
    Py_DECREF(self->last);
    Py_DECREF(self->first);
    Py_DECREF(self->size);

    self->ob_type->tp_free((PyObject*)self);
}

static PyObject* sllist_new(PyTypeObject* type,
                            PyObject* args,
                            PyObject* kwds)
{
    SLListObject* self;

    self = (SLListObject*)type->tp_alloc(type, 0);
    if (self == NULL)
        return NULL;

    Py_INCREF(Py_None);
    self->first = Py_None;

    Py_INCREF(Py_None);
    self->last = Py_None;

    self->size = 0;

    return (PyObject*)self;
}


static PyObject* sllist_appendleft(SLListObject* self, PyObject* arg)
{
    Py_RETURN_NONE;
}

static PyObject* sllist_append(SLListObject* self, PyObject* arg)
{

    SLListNodeObject* elem;
    elem = PyObject_New(SLListNodeObject, &SLListNodeType);

    elem->value = arg;
    elem->next = NULL;

    if(self->last == NULL) {
        self->first = (PyObject*)elem;
        self->last = (PyObject*)elem;
    } else {
        self->last = (PyObject*)elem;
        ((SLListNodeObject*)self->first)->next = (PyObject*)elem;
        self->last =  (PyObject*)elem;
    }
    return (PyObject*)self;
    /* Py_RETURN_NONE; */
}

static PyObject* sllist_insert(SLListObject* self, PyObject* args)
{
    Py_RETURN_NONE;
}

static PyObject* sllist_popleft(SLListObject* self)
{
    Py_RETURN_NONE;
}

static PyObject* sllist_pop(SLListObject* self)
{
    Py_RETURN_NONE;
}

static PyObject* sllist_remove(SLListObject* self, PyObject* arg)
{
    Py_RETURN_NONE;
}

static Py_ssize_t sllist_len(PyObject* self)
{
    SLListObject* list = (SLListObject*)self;
    return list->size;
}

static PyMethodDef SLListMethods[] =
{
    { "appendleft", (PyCFunction)sllist_appendleft, METH_O,
      "Append element at the beginning of the list" },
    { "append", (PyCFunction)sllist_append, METH_O,
      "Append element at the end of the list" },
    { "insert", (PyCFunction)sllist_insert, METH_VARARGS,
      "Inserts element before node" },
    { "popleft", (PyCFunction)sllist_popleft, METH_NOARGS,
      "Remove first element from the list and return it" },
    { "pop", (PyCFunction)sllist_pop, METH_NOARGS,
      "Remove last element from the list and return it" },
    { "remove", (PyCFunction)sllist_remove, METH_O,
      "Remove element from the list" },
    { NULL },   /* sentinel */
};


static PyMemberDef SLListMembers[] =
{
    { "first", T_OBJECT_EX, offsetof(SLListObject, first), READONLY,
      "First node" },
    { "last", T_OBJECT_EX, offsetof(SLListObject, last), READONLY,
      "Next node" },
    { NULL },   /* sentinel */
};

static PySequenceMethods SLListSequenceMethods =
{
    sllist_len,                 /* sq_length */
};

static PyTypeObject SLListType =
{
    PyObject_HEAD_INIT(NULL)
    0,                          /* ob_size */
    "llist.SLList",             /* tp_name */
    sizeof(SLListObject),       /* tp_basicsize */
    0,                          /* tp_itemsize */
    (destructor)sllist_dealloc, /* tp_dealloc */
    0,                          /* tp_print */
    0,                          /* tp_getattr */
    0,                          /* tp_setattr */
    0,                          /* tp_compare */
    0,                          /* tp_repr */
    0,                          /* tp_as_number */
    &SLListSequenceMethods,      /* tp_as_sequence */
    0,                          /* tp_as_mapping */
    0,                          /* tp_hash */
    0,                          /* tp_call */
    0,                          /* tp_str */
    0,                          /* tp_getattro */
    0,                          /* tp_setattro */
    0,                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,         /* tp_flags */
    "Singly linked list",       /* tp_doc */
    0,                          /* tp_traverse */
    0,                          /* tp_clear */
    0,                          /* tp_richcompare */
    0,                          /* tp_weaklistoffset */
    0,                          /* tp_iter */
    0,                          /* tp_iternext */
    SLListMethods,              /* tp_methods */
    SLListMembers,              /* tp_members */
    0,                          /* tp_getset */
    0,                          /* tp_base */
    0,                          /* tp_dict */
    0,                          /* tp_descr_get */
    0,                          /* tp_descr_set */
    0,                          /* tp_dictoffset */
    0,                          /* tp_init */
    0,                          /* tp_alloc */
    sllist_new,                 /* tp_new */
};


int sllist_init_type()
{
    SLListType.tp_new = PyType_GenericNew;
    SLListNodeType.tp_new = PyType_GenericNew;

    int sllistrv = (PyType_Ready(&SLListType) <= 0) ? 1 : 0;
    int sllistnoderv = (PyType_Ready(&SLListNodeType) <= 0) ? 1 : 0;
    return sllistrv + sllistnoderv;

}

void sllist_register(PyObject* module)
{
    Py_INCREF(&SLListType);
    Py_INCREF(&SLListNodeType);

    PyModule_AddObject(module, "SLList", (PyObject*)&SLListType);
    PyModule_AddObject(module, "SLListNode", (PyObject*)&SLListNodeType);

}

