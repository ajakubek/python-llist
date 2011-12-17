#include <Python.h>
#include <structmember.h>

staticforward PyTypeObject SLListNodeType;
typedef struct
{
    PyObject_HEAD
    PyObject* value;
    PyObject* next;
} SLListNodeObject;


static SLListNodeObject* sllistnode_create(PyObject* next,
                                           PyObject* value)
{
    SLListNodeObject* node;
    assert(value != NULL);

    node = (SLListNodeObject*)PyObject_CallObject(
        (PyObject*)&SLListNodeType, NULL);

    if (next != NULL && next != Py_None)
        node->next = next;

    assert(node->value == Py_None);

    Py_INCREF(value);
    node->value = value;

    return node;
}

static void dllistnode_delete(SLListNodeObject* node)
{
    Py_DECREF((PyObject*)node);
}


static void sllistnode_dealloc(SLListNodeObject* self)
{
    Py_DECREF(Py_None);
    Py_DECREF(self->value);
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
        0,                              /* ob_size           */
        "llist.SLListNode",             /* tp_name           */
        sizeof(SLListNodeObject),       /* tp_basicsize      */
        0,                              /* tp_itemsize       */
        (destructor)sllistnode_dealloc, /* tp_dealloc        */
        0,                              /* tp_print          */
        0,                              /* tp_getattr        */
        0,                              /* tp_setattr        */
        0,                              /* tp_compare        */
        0,                              /* tp_repr           */
        0,                              /* tp_as_number      */
        0,                              /* tp_as_sequence    */
        0,                              /* tp_as_mapping     */
        0,                              /* tp_hash           */
        sllistnode_call,                /* tp_call           */
        0,                              /* tp_str            */
        0,                              /* tp_getattro       */
        0,                              /* tp_setattro       */
        0,                              /* tp_as_buffer      */
        Py_TPFLAGS_DEFAULT,             /* tp_flags          */
        "Singly linked list node",      /* tp_doc            */
        0,                              /* tp_traverse       */
        0,                              /* tp_clear          */
        0,                              /* tp_richcompare    */
        0,                              /* tp_weaklistoffset */
        0,                              /* tp_iter           */
        0,                              /* tp_iternext       */
        0,                              /* tp_methods        */
        SLListNodeMembers,              /* tp_members        */
        0,                              /* tp_getset         */
        0,                              /* tp_base           */
        0,                              /* tp_dict           */
        0,                              /* tp_descr_get      */
        0,                              /* tp_descr_set      */
        0,                              /* tp_dictoffset     */
        0,                              /* tp_init           */
        0,                              /* tp_alloc          */
        sllistnode_new,                 /* tp_new            */
    };




/* ****************************************************************************** */
/*                                      SLLIST                                    */
/* ****************************************************************************** */

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
    Py_XDECREF(self->last);
    Py_XDECREF(self->first);

    self->ob_type->tp_free((PyObject*)self);

}



static void sllistnode_delete(SLListNodeObject* node)
{
    Py_DECREF((PyObject*)node);
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
    self->last = Py_None;
    self->size = 0;

    return (PyObject*)self;
}


static PyObject* sllist_appendleft(SLListObject* self, PyObject* arg)
{
    if (!PyObject_TypeCheck(arg, &SLListNodeType)) {
        PyErr_SetString(PyExc_TypeError, "not a SLLNodeObject");
        return NULL;
    }

    SLListNodeObject* new_node;
    new_node = sllistnode_create(self->first, arg);

    self->first=(PyObject*)new_node;

    if(self->last == Py_None)
        self->last = (PyObject*)new_node;

    ++self->size;

    Py_INCREF((PyObject*)new_node);
    return (PyObject*)new_node;
}

static PyObject* sllist_appendright(SLListObject* self, PyObject* arg)
{

    if (!PyObject_TypeCheck(arg, &SLListNodeType)) {
        PyErr_SetString(PyExc_TypeError, "not a SLLNodeObject");
        return NULL;
    }
    SLListNodeObject* new_node;
    new_node = sllistnode_create(NULL, arg);

    if(self->first == Py_None)
        self->first = (PyObject*)new_node;
    else
        ((SLListNodeObject*)self->last)->next = (PyObject*)new_node;

    self->last = (PyObject*)new_node;

    ++self->size;
    Py_INCREF((PyObject*)new_node);
    return (PyObject*)new_node;
}


static PyObject* sllist_get_node_at(SLListObject* self,
                                    PyObject* arg)
{
    int pos = PyInt_AsLong(arg);
    if (!PyInt_Check(arg)){
        PyErr_SetString(PyExc_TypeError, "Index should be integer");
        return NULL;
    }
    if(pos >= self->size || pos < 0){
        PyErr_SetString(PyExc_IndexError, "No such index");
        return NULL;
    }
    SLListNodeObject* node;
    node = (SLListNodeObject*)self->first;
    int counter = 0;
    for(;counter<pos;counter++){
      node = (SLListNodeObject*)node->next;
    }

    return (PyObject*)node;
}


static PyObject* sllist_get_item(PyObject* self, Py_ssize_t index)
{
    SLListObject* list = (SLListObject*)self;
    return (PyObject*)sllist_get_node_at(list, Py_BuildValue("i", index));
}

static int sllist_set_item(PyObject* self, Py_ssize_t index, PyObject* val)
{
    SLListObject* list = (SLListObject*)self;

    if (!PyObject_TypeCheck(val, &SLListNodeType)) {
        PyErr_SetString(PyExc_TypeError, "Not a SLLNodeObject");
        return -1;
    }
    SLListNodeObject* node;
    if(index==0)
        node = (SLListNodeObject*)list->first;
    else if(index==list->size-1)
        node = (SLListNodeObject*)list->last;
    else
        node = (SLListNodeObject*)sllist_get_node_at(list, Py_BuildValue("i", index));
    Py_XDECREF(node->value);
    node->value =((SLListNodeObject*)val)->value;
    return 0;
}

static PyObject* sllist_popleft(SLListObject* self)
{
    SLListNodeObject* del_node;

    if (self->first == Py_None)
    {
        PyErr_SetString(PyExc_RuntimeError, "List is empty");
        return NULL;
    }

    del_node = (SLListNodeObject*)self->first;
    self->first = del_node->next;
    if (self->last == (PyObject*)del_node)
        self->last = Py_None;

    --self->size;

    /* Py_DECREF(del_node); */
    return (PyObject*)del_node;

}


static PyObject* sllist_popright(SLListObject* self)
{

    SLListNodeObject* del_node;

    if (self->last == Py_None)
    {
        PyErr_SetString(PyExc_RuntimeError, "List is empty");
        return NULL;
    }

    del_node = (SLListNodeObject*)self->last;
    self->last = Py_None;

    if (self->first == (PyObject*)del_node)
        self->first = Py_None;

    --self->size;

    /* Py_DECREF((PyObject*)del_node); */
    return (PyObject*) del_node;
}



static PyObject* sllist_remove(SLListObject* self, PyObject* arg)
{
    if (!PyObject_TypeCheck(arg, &SLListNodeType)) {
        PyErr_SetString(PyExc_TypeError, "Not a SLLNodeObject");
        return NULL;
    }

    SLListNodeObject* node = (SLListNodeObject*)self->first;
    SLListNodeObject* prev = Py_None;
    SLListNodeObject* to_delete = (SLListNodeObject*)arg;

    while(node != Py_None && node != to_delete){
        prev = node;
        node = (SLListNodeObject*)node->next;
    }
    if(node == Py_None) {
        PyErr_SetString(PyExc_RuntimeError, "Item not found");
        return NULL;
    }
    if(node == (SLListNodeObject*)self->first)
        self->first = node->next;
    else
        prev->next = node->next;
    if(node == (SLListNodeObject*)self->last)
        self->last = (PyObject*)prev;
    --self->size;

    sllistnode_delete(to_delete);

    Py_RETURN_NONE;
}


static int sllist_len(PyObject* self)
{
    SLListObject* list = (SLListObject*)self;
    return list->size;
}

static PyMethodDef SLListMethods[] =
    {
        { "appendleft", (PyCFunction)sllist_appendleft, METH_O,
          "Append element at the beginning of the list" },
        { "append", (PyCFunction)sllist_appendright, METH_O,
          "Append element at the end of the list" },

        { "insert", (PyCFunction)sllist_appendright, METH_O,
          "Inserts element before node" },

        { "pop", (PyCFunction)sllist_popleft, METH_NOARGS,
          "Remove last element from the list and return it" },

        { "popleft", (PyCFunction)sllist_popleft, METH_NOARGS,
          "Remove first element from the list and return it" },

        { "popright", (PyCFunction)sllist_popright, METH_NOARGS,
          "Remove last element from the list and return it" },

        /* { "len", (PyCFunction)sllist_len, METH_NOARGS, */
        /*   "Returns size of SSList object" }, */

        { "remove", (PyCFunction)sllist_remove, METH_O,
          "Remove element from the list" },

        { "get_node_at", (PyCFunction)sllist_get_node_at, METH_O,
          "Return node at given position" },
        { NULL },   /* sentinel */
    };


static PyMemberDef SLListMembers[] =
    {
        { "first", T_OBJECT_EX, offsetof(SLListObject, first), READONLY,
          "First node" },
        { "last", T_OBJECT_EX, offsetof(SLListObject, last), READONLY,
          "Next node" },
        { "size", T_INT, offsetof(SLListObject, size), 0,
          "size" },

        { NULL },   /* sentinel */
    };

static PySequenceMethods SLListSequenceMethods[] =
    {
        sllist_len,                  /* sq_length         */
        0,                           /* sq_concat         */
        0,                           /* sq_repeat         */
        sllist_get_item,             /* sq_item           */
        0,                           /* sq_slice;         */
        sllist_set_item,             /* sq_ass_item       */
        0                            /* sq_ass_slice      */
    };

static PyTypeObject SLListType =
    {
        PyObject_HEAD_INIT(NULL)
        0,                           /* ob_size           */
        "llist.SLList",              /* tp_name           */
        sizeof(SLListObject),        /* tp_basicsize      */
        0,                           /* tp_itemsize       */
        (destructor)sllist_dealloc,  /* tp_dealloc        */
        0,                           /* tp_print          */
        0,                           /* tp_getattr        */
        0,                           /* tp_setattr        */
        0,                           /* tp_compare        */
        0,                           /* tp_repr           */
        0,                           /* tp_as_number      */
        SLListSequenceMethods,       /* tp_as_sequence    */
        0,                           /* tp_as_mapping     */
        0,                           /* tp_hash           */
        0,                           /* tp_call           */
        0,                           /* tp_str            */
        0,                           /* tp_getattro       */
        0,                           /* tp_setattro       */
        0,                           /* tp_as_buffer      */
        Py_TPFLAGS_DEFAULT,          /* tp_flags          */
        "Singly linked list",        /* tp_doc            */
        0,                           /* tp_traverse       */
        0,                           /* tp_clear          */
        0,                           /* tp_richcompare    */
        0,                           /* tp_weaklistoffset */
        0,                           /* tp_iter           */
        0,                           /* tp_iternext       */
        SLListMethods,               /* tp_methods        */
        SLListMembers,               /* tp_members        */
        0,                           /* tp_getset         */
        0,                           /* tp_base           */
        0,                           /* tp_dict           */
        0,                           /* tp_descr_get      */
        0,                           /* tp_descr_set      */
        0,                           /* tp_dictoffset     */
        0,                           /* tp_init           */
        0,                           /* tp_alloc          */
        sllist_new,                  /* tp_new            */
    };


int sllist_init_type()
{

    return
        ((PyType_Ready(&SLListType) == 0) &&
         (PyType_Ready(&SLListNodeType) == 0))
        ? 1 : 0;

}

void sllist_register(PyObject* module)
{
    Py_INCREF(&SLListType);
    Py_INCREF(&SLListNodeType);

    PyModule_AddObject(module, "SLList", (PyObject*)&SLListType);
    PyModule_AddObject(module, "SLListNode", (PyObject*)&SLListNodeType);

}

