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
    /* Py_XDECREF(self->value); */
    /* Py_XDECREF(self->next); */
    /* self->ob_type->tp_free((PyObject*)self); */
    /* self->ob_type->tp_dealloc((PyObject*)self); */
    PyObject_Del(self);
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

/* static PyObject* sllistnode_call(PyObject* self, */
/*                                  PyObject* args, */
/*                                  PyObject* kw) */
/* { */
/*     SLListNodeObject* node = (SLListNodeObject*)self; */

/*     Py_INCREF(node->value); */
/*     return (PyObject*)node->value; */
/* } */


static int sllistnode_print(PyObject* self, FILE* fp, int flags)
{
    SLListNodeObject* node = (SLListNodeObject*)self;
    fprintf(fp, "%p", node);
    return 0;
}

PyObject* sllistnode_str(PyObject* self)
{
    return PyObject_Repr(self);
}

PyObject* sllistnode_repr(PyObject* self)
{
    SLListNodeObject* node = (SLListNodeObject*)self;
    return PyObject_Str(node->value);
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
        sllistnode_print,               /* tp_print          */
        0,                              /* tp_getattr        */
        0,                              /* tp_setattr        */
        0,                              /* tp_compare        */
        sllistnode_repr,                /* tp_repr           */
        0,                              /* tp_as_number      */
        0,                              /* tp_as_sequence    */
        0,                              /* tp_as_mapping     */
        0,                              /* tp_hash           */
        /* sllistnode_call,                /\* tp_call           *\/ */
        0,                              /* tp_call           */
        sllistnode_str,                 /* tp_str            */
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
    int size;
} SLListObject;


static void sllist_dealloc(SLListObject* self)
{
    /* Py_XDECREF(self->last); */
    /* Py_XDECREF(self->first); */
    /* Py_XDECREF(&self->size); */
    /* self->ob_type->tp_dealloc((PyObject*)self); */
    PyObject_Del(self);

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

/* static PyObject* sllistnode_call(PyObject* self, */
/*                                  PyObject* args, */
/*                                  PyObject* kw) */
/* { */
/*     SLListNodeObject* node = (SLListNodeObject*)self; */

/*     Py_INCREF(node->value); */
/*     return (PyObject*)node->value; */
/* } */


static PyObject* sllist_appendleft(SLListObject* self, PyObject* arg)
{
    if (!PyObject_TypeCheck(arg, &SLListNodeType)) {
        PyErr_SetString(PyExc_TypeError, "not a SLLNodeObject");
        return NULL;
    }

    SLListNodeObject* new_node;
    SLListObject* list = (SLListObject*)self;
    new_node = PyObject_New(SLListNodeObject, &SLListNodeType);
    new_node->value = ((SLListNodeObject*)arg)->value;
    new_node->next = list->first;
    list->first=(PyObject*)new_node;
    list->size++;
    return (PyObject*)list;

}

static PyObject* sllist_append(SLListObject* self, PyObject* arg)
{

    if (!PyObject_TypeCheck(arg, &SLListNodeType)) {
        PyErr_SetString(PyExc_TypeError, "not a SLLNodeObject");
        return NULL;
    }

    SLListObject* list = (SLListObject*)self;

    SLListNodeObject* new_node;
    SLListNodeObject* node;
    new_node = PyObject_New(SLListNodeObject, &SLListNodeType);

    new_node->value = ((SLListNodeObject*)arg)->value;
    new_node->next = Py_None;

    if(list->first == NULL) {
        list->first = (PyObject*)new_node;
        list->last = (PyObject*)new_node;
    } else {
        node = (SLListNodeObject*)list->last;
        node->next = (PyObject*)new_node;
        list->last = (PyObject*)new_node;
    }
    self->size++;
    return (PyObject*)list;
}


static PyObject* sllist_get_node_at(SLListObject* self, PyObject* arg)
{
    int pos;
    SLListObject* list = (SLListObject*)self;
    if (!PyInt_Check(arg)){
        PyErr_SetString(PyExc_TypeError, "Index should be integer");
        return NULL;
    }
    pos = PyInt_AsLong(arg);
    if(pos >= list->size || pos < 0){
        PyErr_SetString(PyExc_IndexError, "No such index");
        return NULL;
    }

    SLListNodeObject* node;
    node = (SLListNodeObject*)list->first;
    int counter = 0;
    for(;counter<pos;counter++){
        node = (SLListNodeObject*)node->next;
    }
    Py_INCREF(node);
    return (PyObject*)node;
}


static PyObject* sllist_get_item(PyObject* self, Py_ssize_t index)
{
    return (PyObject*)sllist_get_node_at((SLListObject*)self, Py_BuildValue("i", index));
}

static int sllist_set_item(PyObject* self, int index, PyObject* val)
{

    if (!PyObject_TypeCheck(val, &SLListNodeType)) {
        PyErr_SetString(PyExc_TypeError, "not a SLLNodeObject");
        return -1;
    }
    SLListNodeObject* node;
    node = (SLListNodeObject*)sllist_get_node_at((SLListObject*)self, Py_BuildValue("i", index));
    Py_XDECREF(node->value);
    node->value =((SLListNodeObject*)val)->value;
    return 0;
}

static PyObject* sllist_pop(SLListObject* self)
{
    PyObject* old_first;
    PyObject* new_first;
    SLListObject* list = (SLListObject*)self;
    if(list->size > 0) {
        old_first = list->first;
        new_first = ((SLListNodeObject*)list->first)->next;
        list->first = (PyObject*)new_first;
        list->size--;
        Py_XDECREF(old_first);
        return (PyObject*)old_first;
    }
    PyErr_SetString(PyExc_IndexError, "List is empty");
    return NULL;
}


static PyObject* sllist_popright(SLListObject* self)
{
    SLListObject* list = (SLListObject*)self;
    SLListNodeObject* temp_node;
    if(list->size<=1){
        PyErr_SetString(PyExc_IndexError, "List is empty");
        return NULL;
    }
    temp_node = ((SLListNodeObject*)sllist_get_node_at(self, Py_BuildValue("i", list->size - 2)));
    temp_node->next = Py_None;
    list->size--;
    Py_XDECREF(temp_node);
    return (PyObject*)temp_node;
}



static PyObject* sllist_remove(SLListObject* self, PyObject* arg)
{
    if (!PyObject_TypeCheck(arg, &SLListNodeType)) {
        PyErr_SetString(PyExc_TypeError, "Not a SLLNodeObject");
        return NULL;
    }
    Py_RETURN_NONE;
}


int sllist_print(PyObject* self, FILE* fp, int flags)
{
    SLListObject* list = (SLListObject*)self;
    fprintf(fp, "%d", list->size);
    return 0;
}

static PyObject* sllist_repr(PyObject* self)
{
    char tmp[20];
    sprintf(tmp, "SLList size: %d", ((SLListObject*)self)->size);
    return PyString_FromString(tmp);
}

static PyObject* sllist_str(PyObject* self)
{
    SLListObject* list = (SLListObject*)self;
    SLListNodeObject* node;
    int list_size = list->size;
    char buf[20*list_size];
    char tmp[20];
    if(list->first == Py_None){
        strcpy(buf, "[]");
    } else {
        strcpy(buf,"[");
        node = (SLListNodeObject*)list->first;
        while(node->next != Py_None) {
            sprintf(tmp, "%p, ", node);
            strcat(buf, tmp);
            node = (SLListNodeObject*)node->next;
        }
        strcat(buf, "]");
    }
    return PyString_FromString(buf);

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
        { "append", (PyCFunction)sllist_append, METH_O,
          "Append element at the end of the list" },

        { "insert", (PyCFunction)sllist_append, METH_O,
          "Inserts element before node" },

        { "pop", (PyCFunction)sllist_popright, METH_NOARGS,
          "Remove last element from the list and return it" },

        { "popleft", (PyCFunction)sllist_pop, METH_NOARGS,
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

static PySequenceMethods SLListSequenceMethods =
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
        sllist_print,                /* tp_print          */
        0,                           /* tp_getattr        */
        0,                           /* tp_setattr        */
        0,                           /* tp_compare        */
        sllist_repr,                 /* tp_repr           */
        0,                           /* tp_as_number      */
        &SLListSequenceMethods,      /* tp_as_sequence    */
        0,                           /* tp_as_mapping     */
        0,                           /* tp_hash           */
        0,                           /* tp_call           */
        sllist_str,                  /* tp_str            */
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

