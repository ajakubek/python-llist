/* Copyright (c) 2011-2012 Adam Jakubek, Rafał Gałczyński
 * Released under the MIT license (see attached LICENSE file).
 */

#include <Python.h>
#include <structmember.h>

staticforward PyTypeObject SLListType;
staticforward PyTypeObject SLListNodeType;
staticforward PyTypeObject SLListIteratorType;

typedef struct
{
    PyObject_HEAD
    PyObject* value;
    PyObject* next;
    PyObject* list_weakref;
} SLListNodeObject;


static SLListNodeObject* sllistnode_create(PyObject* next,
                                           PyObject* value,
                                           PyObject* owner_list)
{
    SLListNodeObject *node;
    PyObject* args = NULL;

    assert(value != NULL);
    assert(owner_list != NULL);
    assert(owner_list != Py_None);

    if (value != Py_None)
    {
        args = PyTuple_New(1);
        if (args == NULL)
        {
            PyErr_SetString(PyExc_RuntimeError,
                "Failed to create argument tuple");
            return NULL;
        }

        Py_INCREF(value);
        if (PyTuple_SetItem(args, 0, value) != 0)
        {
            PyErr_SetString(PyExc_RuntimeError,
                "Failed to initialize argument tuple");
            return NULL;
        }
    }

    node = (SLListNodeObject*)PyObject_CallObject(
        (PyObject*)&SLListNodeType, args);

    Py_XDECREF(args);

    /* next is initialized to Py_None by default
     * (by sllistnode_new) */
    if (next != NULL && next != Py_None)
        node->next = next;

    Py_DECREF(node->list_weakref);
    node->list_weakref = PyWeakref_NewRef(owner_list, NULL);

    return node;
}


static void sllistnode_dealloc(SLListNodeObject* self)
{
    Py_DECREF(self->list_weakref);
    Py_DECREF(self->value);
    Py_DECREF(Py_None);

    self->ob_type->tp_free((PyObject*)self);
}

static int sllistnode_init(SLListNodeObject* self,
                           PyObject* args,
                           PyObject* kwds)
{
    PyObject* value = NULL;

    if (!PyArg_UnpackTuple(args, "__init__", 0, 1, &value))
        return -1;

    if (value == NULL)
        return 0;

    /* initialize node using passed value */
    Py_DECREF(self->value);
    Py_INCREF(value);
    self->value = value;

    return 0;
}



static PyObject* sllistnode_new(PyTypeObject* type,
                                PyObject* args,
                                PyObject* kwds)
{
    SLListNodeObject* self;

    self = (SLListNodeObject*)type->tp_alloc(type, 0);
    if (self == NULL)
        return NULL;

    /* A single reference to Py_None is held for the whole
     * lifetime of a node. */
    Py_INCREF(Py_None);

    self->next = Py_None;
    self->value = Py_None;
    self->list_weakref = Py_None;

    Py_INCREF(self->value);
    Py_INCREF(self->list_weakref);

    return (PyObject*)self;
}



static PyObject* sllistnode_repr(SLListNodeObject* self)
{
    PyObject* str = NULL;
    PyObject* tmp_str;

    str = PyString_FromString("<sllistnode(");
    if (str == NULL)
        goto str_alloc_error;

    tmp_str = PyObject_Repr(self->value);
    if (tmp_str == NULL)
        goto str_alloc_error;
    PyString_ConcatAndDel(&str, tmp_str);

    tmp_str = PyString_FromString(")>");
    if (tmp_str == NULL)
        goto str_alloc_error;
    PyString_ConcatAndDel(&str, tmp_str);

    return str;

str_alloc_error:
    Py_XDECREF(str);
    PyErr_SetString(PyExc_RuntimeError, "Failed to create string");
    return NULL;
}

static PyObject* sllistnode_str(SLListNodeObject* self)
{
    PyObject* str = NULL;
    PyObject* tmp_str;

    str = PyString_FromString("sllistnode(");
    if (str == NULL)
        goto str_alloc_error;

    tmp_str = PyObject_Str(self->value);
    if (tmp_str == NULL)
        goto str_alloc_error;
    PyString_ConcatAndDel(&str, tmp_str);

    tmp_str = PyString_FromString(")");
    if (tmp_str == NULL)
        goto str_alloc_error;
    PyString_ConcatAndDel(&str, tmp_str);

    return str;

str_alloc_error:
    Py_XDECREF(str);
    PyErr_SetString(PyExc_RuntimeError, "Failed to create string");
    return NULL;
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
    "llist.sllistnode",             /* tp_name           */
    sizeof(SLListNodeObject),       /* tp_basicsize      */
    0,                              /* tp_itemsize       */
    (destructor)sllistnode_dealloc, /* tp_dealloc        */
    0,                              /* tp_print          */
    0,                              /* tp_getattr        */
    0,                              /* tp_setattr        */
    0,                              /* tp_compare        */
    (reprfunc)sllistnode_repr,      /* tp_repr           */
    0,                              /* tp_as_number      */
    0,                              /* tp_as_sequence    */
    0,                              /* tp_as_mapping     */
    0,                              /* tp_hash           */
    (ternaryfunc)sllistnode_call,   /* tp_call           */
    (reprfunc)sllistnode_str,       /* tp_str            */
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
    (initproc)sllistnode_init,      /* tp_init           */
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
    PyObject* weakref_list;
} SLListObject;


static void sllist_dealloc(SLListObject* self)
{
    PyObject* node = self->first;

    if (self->weakref_list != NULL)
        PyObject_ClearWeakRefs((PyObject*)self);

    while (node != Py_None)
    {
        PyObject* next_node = ((SLListNodeObject*)node)->next;
        ((SLListNodeObject*)node)->next = Py_None;
        Py_DECREF(node);
        node = next_node;
    }

    Py_DECREF(Py_None);

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

    /* A single reference to Py_None is held for the whole
     * lifetime of a list. */
    Py_INCREF(Py_None);

    self->first = Py_None;
    self->last = Py_None;
    self->weakref_list = NULL;
    self->size = 0;

    return (PyObject*)self;
}

static int sllist_extend_internal(SLListObject* self, PyObject* sequence)
{
    Py_ssize_t i;
    Py_ssize_t sequence_len;

    if (PyObject_TypeCheck(sequence, &SLListType))
    {
        /* Special path for extending with a SLList.
         * It's not strictly required but it will maintain
         * the last accessed item. */
        PyObject* iter_node_obj = ((SLListObject *)sequence)->first;
        PyObject* last_node_obj = self->last;

        while (iter_node_obj != Py_None)
        {
            SLListNodeObject* iter_node = (SLListNodeObject*)iter_node_obj;
            PyObject* new_node;

            new_node = (PyObject*)sllistnode_create(
                Py_None, iter_node->value, (PyObject*)self);

            if (self->last != Py_None)
                ((SLListNodeObject*)self->last)->next = new_node;

            if (self->first == Py_None)
                self->first = new_node;
            self->last = new_node;

            if (iter_node_obj == last_node_obj)
            {
                /* This is needed to terminate loop if self == sequence. */
                break;
            }

            iter_node_obj = iter_node->next;
        }

        self->size += ((SLListObject*)sequence)->size;

        return 1;
    }

    sequence_len = PySequence_Length(sequence);
    if (sequence_len == -1)
    {
        PyErr_SetString(PyExc_ValueError, "Invalid sequence");
        return 0;
    }

    for (i = 0; i < sequence_len; ++i)
    {
        PyObject* item;
        PyObject* new_node;

        item = PySequence_GetItem(sequence, i);
        if (item == NULL)
        {
            PyErr_SetString(PyExc_ValueError,
                            "Failed to get element from sequence");
            return 0;
        }

        new_node = (PyObject*)sllistnode_create(Py_None,
                                                item,
                                                (PyObject*)self);


        if(self->first == Py_None)
            self->first = new_node;
        else
            ((SLListNodeObject*)self->last)->next = new_node;

        self->last = new_node;

        ++self->size;

        Py_DECREF(item);
    }

    return 1;
}



static int sllist_init(SLListObject* self, PyObject* args, PyObject* kwds)
{
    PyObject* sequence = NULL;

    if (!PyArg_UnpackTuple(args, "__init__", 0, 1, &sequence))
        return -1;

    if (sequence == NULL)
        return 0;

    /* initialize list using passed sequence */
    if (!PySequence_Check(sequence))
    {
        PyErr_SetString(PyExc_TypeError, "Argument must be a sequence");
        return -1;
    }

    return sllist_extend_internal(self, sequence) ? 0 : -1;
}


static int sllist_compare(SLListObject* self, SLListObject* other)
{
    SLListNodeObject* self_node = (SLListNodeObject*)self->first;
    SLListNodeObject* other_node = (SLListNodeObject*)other->first;
    int result = 0;

    while (result == 0)
    {
        if ((PyObject*)self_node == Py_None ||
            (PyObject*)other_node == Py_None)
        {
            if ((PyObject*)self_node == Py_None)
                return ((PyObject*)other_node == Py_None) ? 0 : -1;
            else
                return ((PyObject*)other_node == Py_None) ? 1 : 0;
        }

        result = PyObject_Compare(self_node->value, other_node->value);
        if (PyErr_Occurred())
            return 0;

        self_node = (SLListNodeObject*)self_node->next;
        other_node = (SLListNodeObject*)other_node->next;
    }

    return result;
}



static SLListNodeObject* sllist_get_prev(SLListObject* self,
                                         SLListNodeObject* next)
{
    SLListNodeObject* prev = NULL;

    SLListNodeObject* node = (SLListNodeObject*)self->first;

    if (!PyObject_TypeCheck(next, &SLListNodeType))
    {
        PyErr_SetString(PyExc_TypeError, "Argument is not an sllistnode");
        return NULL;
    }

    if (self->first == Py_None)
    {
        PyErr_SetString(PyExc_RuntimeError, "List is empty");
        return NULL;
    }


    /* TODO: Think this over once more */
    if (self->first == (PyObject*)next)
    {
        return NULL;
    }

    if(self->first != Py_None)
    {
        while((PyObject*)node != Py_None && node != next)
        {
            prev = node;
            node = (SLListNodeObject*)node->next;
        }
        return (SLListNodeObject*)prev;
    }
    return NULL;

}


static PyObject* sllist_appendleft(SLListObject* self, PyObject* arg)
{
    SLListNodeObject* new_node;

    if (PyObject_TypeCheck(arg, &SLListNodeType))
        arg = ((SLListNodeObject*)arg)->value;

    new_node = sllistnode_create(self->first,
                                 arg,
                                 (PyObject*)self);
    /* setting head as new node */
    self->first  = (PyObject*)new_node;

    /* setting tail as new node (appending to empty list)*/
    if(self->last == Py_None)
        self->last = (PyObject*)new_node;

    ++self->size;

    Py_INCREF((PyObject*)new_node);
    return (PyObject*)new_node;
}

static PyObject* sllist_appendright(SLListObject* self, PyObject* arg)
{
    SLListNodeObject* new_node;

    if (PyObject_TypeCheck(arg, &SLListNodeType))
        arg = ((SLListNodeObject*)arg)->value;

    new_node = sllistnode_create(Py_None,
                                 arg,
                                 (PyObject*)self);

    /* appending to empty list */
    if(self->first == Py_None)
        self->first = (PyObject*)new_node;
    /* setting next of last element as new node */
    else
        ((SLListNodeObject*)self->last)->next = (PyObject*)new_node;

    /* allways set last node to new node */
    self->last = (PyObject*)new_node;

    ++self->size;
    Py_INCREF((PyObject*)new_node);
    return (PyObject*)new_node;
}

static PyObject* sllist_insertafter(SLListObject* self, PyObject* arg)
{

    PyObject* value = NULL;
    PyObject* before = NULL;
    PyObject* list_ref;
    SLListNodeObject* new_node;

    if (!PyArg_UnpackTuple(arg, "insertafter", 2, 2, &value, &before))
        return NULL;

    if (!PyObject_TypeCheck(before, &SLListNodeType))
    {
        PyErr_SetString(PyExc_TypeError, "Argument is not an sllistnode");
        return NULL;
    }

    if (PyObject_TypeCheck(value, &SLListNodeType))
        value = ((SLListNodeObject*)value)->value;

    if (((SLListNodeObject*)before)->list_weakref == Py_None)
    {
        PyErr_SetString(PyExc_ValueError,
            "sllistnode does not belong to a list");
        return NULL;
    }

    list_ref = PyWeakref_GetObject(
        ((SLListNodeObject*)before)->list_weakref);
    if (list_ref != (PyObject*)self)
    {
        PyErr_SetString(PyExc_ValueError,
            "sllistnode belongs to another list");
        return NULL;
    }

    new_node = sllistnode_create(Py_None,
                                 value,
                                 (PyObject*)self);

    /* putting new node in created gap */
    new_node->next = ((SLListNodeObject*)before)->next;
    ((SLListNodeObject*)before)->next = (PyObject*)new_node;

    if (self->last == before)
        self->last = (PyObject*)new_node;

    ++self->size;
    Py_INCREF((PyObject*)new_node);
    return (PyObject*)new_node;
}

static PyObject* sllist_insertbefore(SLListObject* self, PyObject* arg)
{

    PyObject* value = NULL;
    PyObject* after = NULL;
    PyObject* list_ref;

    SLListNodeObject* new_node;
    SLListNodeObject* prev;

    if (!PyArg_UnpackTuple(arg, "insertbefore", 2, 2, &value, &after))
        return NULL;

    if (!PyObject_TypeCheck(after, &SLListNodeType))
    {
        PyErr_SetString(PyExc_TypeError, "Argument is not an sllistnode");
        return NULL;
    }
    if (PyObject_TypeCheck(value, &SLListNodeType))
        value = ((SLListNodeObject*)value)->value;

    if (after == Py_None)
    {
        PyErr_SetString(PyExc_ValueError,
            "sllistnode does not belong to a list");
        return NULL;
    }

    list_ref = PyWeakref_GetObject(
        ((SLListNodeObject*)after)->list_weakref);
    if (list_ref != (PyObject*)self)
    {
        PyErr_SetString(PyExc_ValueError,
            "sllistnode belongs to another list");
        return NULL;
    }
    new_node = sllistnode_create(Py_None,
                                 value,
                                 (PyObject*)self);

    /* getting prev node for this from arg*/
    prev = sllist_get_prev(self, (SLListNodeObject*)after);

    /* putting new node in created gap, not first and exists */
    if((PyObject*)prev != Py_None && prev != NULL)
    {
        ((SLListNodeObject*)prev)->next = (PyObject*)new_node;
        new_node->next = after;
    }
    else
    {
        new_node->next = after;
        self->first = (PyObject*)new_node;
    }
    /* new_node->next = ((SLListNodeObject*)after)->next; */
    /* ((SLListNodeObject*)before)->next = (PyObject*)new_node; */
    ++self->size;
    Py_INCREF((PyObject*)new_node);
    return (PyObject*)new_node;
}


static PyObject* sllist_extendleft(SLListObject* self, PyObject* sequence)
{
    Py_ssize_t i;
    Py_ssize_t sequence_len;

    if (PyObject_TypeCheck(sequence, &SLListType))
    {
        /* Special path for extending with a SLList.
         * It's not strictly required but it will maintain
         * the last accessed item. */
        PyObject* iter_node_obj = ((SLListObject*)sequence)->first;
        PyObject* last_node_obj = ((SLListObject*)sequence)->last;

        while (iter_node_obj != Py_None)
        {
            SLListNodeObject* iter_node = (SLListNodeObject*)iter_node_obj;
            PyObject* new_node;

            new_node = (PyObject*)sllistnode_create(
                self->first, iter_node->value, (PyObject*)self);

            self->first = new_node;
            if (self->last == Py_None)
                self->last = new_node;

            if (iter_node_obj == last_node_obj)
            {
                /* This is needed to terminate loop if self == sequence. */
                break;
            }

            iter_node_obj = iter_node->next;
        }

        self->size += ((SLListObject*)sequence)->size;

        Py_RETURN_NONE;
    }

    sequence_len = PySequence_Length(sequence);
    if (sequence_len == -1)
    {
        PyErr_SetString(PyExc_ValueError, "Invalid sequence");
        return NULL;
    }

    for (i = 0; i < sequence_len; ++i)
    {
        PyObject* item;
        PyObject* new_node;

        item = PySequence_GetItem(sequence, i);
        if (item == NULL)
        {
            PyErr_SetString(PyExc_ValueError,
                            "Failed to get element from sequence");
            return NULL;
        }

        new_node = (PyObject*)sllistnode_create(self->first,
                                                item,
                                                (PyObject*)self);

        self->first = new_node;
        if (self->last == Py_None)
            self->last = new_node;

        ++self->size;

        Py_DECREF(item);
    }

    Py_RETURN_NONE;
}


static PyObject* sllist_extendright(SLListObject* self, PyObject* arg)
{
    if (!sllist_extend_internal(self, arg))
        return NULL;

    Py_RETURN_NONE;
}


static SLListNodeObject* sllist_get_node_internal(SLListObject* self,
                                                  Py_ssize_t pos)
{
    SLListNodeObject* node;
    Py_ssize_t counter;

    if (pos < 0 || pos >= self->size)
    {
        PyErr_SetString(PyExc_IndexError, "Index out of range");
        return NULL;
    }
    /* taking head */
    node = (SLListNodeObject*)self->first;
    assert((PyObject*)node != Py_None);
    /* iterate to given index */
    for (counter = 0; counter < pos; ++counter)
        node = (SLListNodeObject*)node->next;

    return node;
}


static PyObject* sllist_node_at(PyObject* self, PyObject* indexObject)
{
    SLListNodeObject* node;
    Py_ssize_t index;

    if (!PyInt_Check(indexObject))
    {
        PyErr_SetString(PyExc_TypeError, "Index must be an integer");
        return NULL;
    }

    index = PyInt_AsSsize_t(indexObject);

    if (index < 0)
        index = ((SLListObject*)self)->size + index;

    node = sllist_get_node_internal((SLListObject*)self, index);
    Py_XINCREF(node);

    return (PyObject*)node;
}


static PyObject* sllist_remove(SLListObject* self, PyObject* arg)
{
    SLListNodeObject* del_node;
    SLListNodeObject* prev;
    PyObject* list_ref;
    PyObject* value;

    if (!PyObject_TypeCheck(arg, &SLListNodeType))
    {
        PyErr_SetString(PyExc_TypeError, "Argument is not an sllistnode");
        return NULL;
    }

    if (self->first == Py_None)
    {
        PyErr_SetString(PyExc_ValueError, "List is empty");
        return NULL;
    }

    del_node = (SLListNodeObject*)arg;

    if (del_node->list_weakref == Py_None)
    {
        PyErr_SetString(PyExc_ValueError,
            "sllistnode does not belong to a list");
        return NULL;
    }

    list_ref = PyWeakref_GetObject(del_node->list_weakref);
    if (list_ref != (PyObject*)self)
    {
        PyErr_SetString(PyExc_ValueError,
            "sllistnode belongs to another list");
        return NULL;
    }

    /* remove first node case */
    if(self->first == arg) {
        self->first = del_node->next;
        if (self->last == arg)
            self->last = Py_None;
    }
    /* we are sure that we have more than 1 node */
    else
    {
        /* making gap */
        prev = sllist_get_prev(self, del_node);
        prev->next = del_node->next;

        if (self->last == arg)
            self->last = (PyObject*)prev;
    }

    --self->size;

    value = del_node->value;
    Py_INCREF(value);

    /* unlink from parent list */
    Py_DECREF(del_node->list_weakref);
    Py_INCREF(Py_None);
    del_node->list_weakref = Py_None;

    del_node->next = Py_None;
    Py_DECREF(arg);

    return value;

}


static PyObject* sllist_rotate(SLListObject* self, PyObject* nObject)
{
    Py_ssize_t n;
    Py_ssize_t split_idx;
    Py_ssize_t n_mod;
    SLListNodeObject* new_first;
    SLListNodeObject* new_last;

    if (self->size <= 1)
        Py_RETURN_NONE;

    if (!PyInt_Check(nObject))
    {
        PyErr_SetString(PyExc_TypeError, "n must be an integer");
        return NULL;
    }

    n = PyInt_AsSsize_t(nObject);
    n_mod = (n >= 0 ? n : -n) % self->size;

    if (n_mod == 0)
        Py_RETURN_NONE; /* no-op */

    if (n > 0)
        split_idx = self->size - n_mod; /* rotate right */
    else
        split_idx = n_mod;  /* rotate left */

    new_last = sllist_get_node_internal(self, split_idx - 1);
    assert(new_last != NULL);
    new_first = (SLListNodeObject*)new_last->next;

    ((SLListNodeObject*)self->last)->next = self->first;

    new_last->next = Py_None;

    self->first = (PyObject*)new_first;
    self->last = (PyObject*)new_last;

    Py_RETURN_NONE;
}


static PyObject* sllist_concat(PyObject* self, PyObject* other)
{
    SLListObject* new_list;

    new_list = (SLListObject*)PyObject_CallObject(
        (PyObject*)&SLListType, NULL);

    if (!sllist_extend_internal(new_list, self) ||
        !sllist_extend_internal(new_list, other))
    {
        Py_DECREF(new_list);
        return NULL;
    }

    return (PyObject*)new_list;
}


static PyObject* sllist_inplace_concat(PyObject* self, PyObject* other)
{
    if (!sllist_extend_internal((SLListObject*)self, other))
        return NULL;

    Py_INCREF(self);
    return self;
}


static PyObject* sllist_repeat(PyObject* self, Py_ssize_t count)
{
    SLListObject* new_list;
    Py_ssize_t i;

    new_list = (SLListObject*)PyObject_CallObject(
        (PyObject*)&SLListType, NULL);

    for (i = 0; i < count; ++i)
    {
        if (!sllist_extend_internal(new_list, self))
        {
            Py_DECREF(new_list);
            return NULL;
        }
    }

    return (PyObject*)new_list;
}


static PyObject* sllist_get_item(PyObject* self, Py_ssize_t index)
{
    SLListNodeObject* node;

    node = sllist_get_node_internal((SLListObject*)self, index);
    if (node != NULL)
    {
        PyObject* value = node->value;

        Py_XINCREF(value);
        return value;
    }

    return NULL;
}

static int sllist_set_item(PyObject* self, Py_ssize_t index, PyObject* val)
{
    SLListObject* list = (SLListObject*)self;
    SLListNodeObject* node;
    PyObject* oldval;

    /* setting fist node */
    if(index==0)
        node = (SLListNodeObject*)list->first;
    /* setting last node */
    else if(index==list->size-1)
        node = (SLListNodeObject*)list->last;
    /* setting nth node,  */
    else
        /* get_node_internal will rise error for index out of scale */
        node = (SLListNodeObject*)sllist_get_node_internal(list, index);

    if (node == NULL)
        return -1;

    /* Here is a tricky (and undocumented) part of sequence protocol.
     * Python will pass NULL as item value when item is deleted with:
     * del list[index] */
    if (val == NULL)
    {
        PyObject* result = sllist_remove(list, (PyObject*)node);

        Py_XDECREF(result);

        return (result != NULL) ? 0 : -1;
    }

    /* The rest of this function handles normal assignment:
     * list[index] = item */
    if (!PyObject_TypeCheck(val, &SLListNodeType)) {
        PyErr_SetString(PyExc_TypeError, "Argument is not an sllistnode");
        return -1;
    }

    /* nice played, migu :) */
    val = ((SLListNodeObject*)val)->value;

    oldval = node->value;

    Py_INCREF(val);
    node->value = val;
    Py_DECREF(oldval);

    return 0;
}

static PyObject* sllist_clear(SLListObject* self)
{
    PyObject* iter_node_obj = self->first;

    while (iter_node_obj != Py_None)
    {
        SLListNodeObject* iter_node = (SLListNodeObject*)iter_node_obj;

        iter_node_obj = iter_node->next;

        iter_node->next = Py_None;
        Py_DECREF((PyObject*)iter_node);
    }

    self->first = Py_None;
    self->last = Py_None;
    self->size = 0;

    Py_RETURN_NONE;
}

static PyObject* sllist_popleft(SLListObject* self)
{
    SLListNodeObject* del_node;
    PyObject* value;

    if (self->first == Py_None)
    {
        PyErr_SetString(PyExc_ValueError, "List is empty");
        return NULL;
    }

    del_node = (SLListNodeObject*)self->first;

    /* setting the first node to next of removed one*/
    self->first = del_node->next;
    /* removeing last node */
    if (self->last == (PyObject*)del_node)
        self->last = Py_None;

    --self->size;

    Py_INCREF(del_node->value);
    value = del_node->value;

    del_node->next = Py_None;
    Py_DECREF((PyObject*)del_node);

    return value;
}


static PyObject* sllist_popright(SLListObject* self)
{
    SLListNodeObject* del_node;
    SLListNodeObject* prev;
    PyObject* value;

    if (self->last == Py_None)
    {
        PyErr_SetString(PyExc_ValueError, "List is empty");
        return NULL;
    }

    del_node = (SLListNodeObject*)self->last;
    /* only one node in list */
    if (self->first == (PyObject*)del_node){
        self->last = Py_None;
        self->first = Py_None;
    }
    /* more than one node */
    else
    {
        prev = sllist_get_prev(self, del_node);
        prev->next = Py_None;
        self->last = (PyObject*)prev;
    }

    --self->size;

    Py_INCREF(del_node->value);
    value = del_node->value;

    del_node->next = Py_None;
    Py_DECREF((PyObject*)del_node);

    return value;
}


static PyObject* sllist_iter(PyObject* self)
{
    PyObject* args;
    PyObject* result;

    args = PyTuple_New(1);
    if (args == NULL)
    {
        PyErr_SetString(PyExc_RuntimeError,
            "Failed to create argument tuple");
        return NULL;
    }

    Py_INCREF(self);
    if (PyTuple_SetItem(args, 0, self) != 0)
    {
        PyErr_SetString(PyExc_RuntimeError,
            "Failed to initialize argument tuple");
        return NULL;
    }

    result = PyObject_CallObject((PyObject*)&SLListIteratorType, args);

    Py_DECREF(args);

    return result;
}



static PyObject* sllist_to_string(SLListObject* self,
                                  reprfunc fmt_func)
{
    PyObject* str = NULL;
    PyObject* comma_str = NULL;
    PyObject* tmp_str;
    SLListNodeObject* node = (SLListNodeObject*)self->first;

    assert(fmt_func != NULL);

    if (self->first == Py_None)
    {
        str = PyString_FromString("sllist()");
        if (str == NULL)
            goto str_alloc_error;
        return str;
    }

    str = PyString_FromString("sllist([");
    if (str == NULL)
        goto str_alloc_error;

    comma_str = PyString_FromString(", ");
    if (comma_str == NULL)
        goto str_alloc_error;

    while ((PyObject*)node != Py_None)
    {
        if (node != (SLListNodeObject*)self->first)
            PyString_Concat(&str, comma_str);

        tmp_str = fmt_func(node->value);
        if (tmp_str == NULL)
            goto str_alloc_error;
        PyString_ConcatAndDel(&str, tmp_str);

        node = (SLListNodeObject*)node->next;
    }

    Py_DECREF(comma_str);
    comma_str = NULL;

    tmp_str = PyString_FromString("])");
    if (tmp_str == NULL)
        goto str_alloc_error;
    PyString_ConcatAndDel(&str, tmp_str);

    return str;

str_alloc_error:
    Py_XDECREF(str);
    Py_XDECREF(comma_str);
    PyErr_SetString(PyExc_RuntimeError, "Failed to create string");
    return NULL;
}


static PyObject* sllist_repr(SLListObject* self)
{
    return sllist_to_string(self, PyObject_Repr);
}


static PyObject* sllist_str(SLListObject* self)
{
    return sllist_to_string(self, PyObject_Str);
}


static Py_ssize_t sllist_len(PyObject* self)
{
    return ((SLListObject*)self)->size;
}


static long sllist_hash(SLListObject* self)
{
    long hash = 0;
    PyObject* iter_node_obj = self->first;

    while (iter_node_obj != Py_None)
    {
        long obj_hash;
        SLListNodeObject* iter_node = (SLListNodeObject*)iter_node_obj;

        obj_hash = PyObject_Hash(iter_node->value);
        if (obj_hash == -1)
            return -1;

        hash ^= obj_hash;
        iter_node_obj = iter_node->next;
    }

    return hash;
}


static PyMethodDef SLListMethods[] =
{
    { "appendleft", (PyCFunction)sllist_appendleft, METH_O,
      "Append element at the beginning of the list" },

    { "appendright", (PyCFunction)sllist_appendright, METH_O,
      "Append element at the end of the list" },

    { "append", (PyCFunction)sllist_appendright, METH_O,
      "Append element at the end of the list" },

    { "clear", (PyCFunction)sllist_clear, METH_NOARGS,
      "Remove all elements from the list" },

    { "extend", (PyCFunction)sllist_extendright, METH_O,
      "Append elements from iterable at the right side of the list" },

    { "extendleft", (PyCFunction)sllist_extendleft, METH_O,
      "Append elements from iterable at the left side of the list" },

    { "extendright", (PyCFunction)sllist_extendright, METH_O,
      "Append elements from iterable at the right side of the list" },

    { "insertafter", (PyCFunction)sllist_insertafter, METH_VARARGS,
      "Inserts element after node" },

    { "insertbefore", (PyCFunction)sllist_insertbefore, METH_VARARGS,
      "Inserts element before node" },

    { "nodeat", (PyCFunction)sllist_node_at, METH_O,
      "Return node at index" },

    { "pop", (PyCFunction)sllist_popright, METH_NOARGS,
      "Remove last element from the list and return it" },

    { "popleft", (PyCFunction)sllist_popleft, METH_NOARGS,
      "Remove first element from the list and return it" },

    { "popright", (PyCFunction)sllist_popright, METH_NOARGS,
      "Remove last element from the list and return it" },

    { "remove", (PyCFunction)sllist_remove, METH_O,
      "Remove element from the list" },

    { "rotate", (PyCFunction)sllist_rotate, METH_O,
      "Rotate the list n steps to the right" },

    { NULL },   /* sentinel */
};


static PyMemberDef SLListMembers[] =
{
    { "first", T_OBJECT_EX, offsetof(SLListObject, first), READONLY,
      "First node" },
    { "last", T_OBJECT_EX, offsetof(SLListObject, last), READONLY,
      "Next node" },
    { "size", T_INT, offsetof(SLListObject, size), READONLY,
      "size" },

    { NULL },   /* sentinel */
};

static PySequenceMethods SLListSequenceMethods =
{
    sllist_len,                  /* sq_length         */
    sllist_concat,               /* sq_concat         */
    sllist_repeat,               /* sq_repeat         */
    sllist_get_item,             /* sq_item           */
    0,                           /* sq_slice;         */
    sllist_set_item,             /* sq_ass_item       */
    0,                           /* sq_ass_slice      */
    0,                           /* sq_contains       */
    sllist_inplace_concat,       /* sq_inplace_concat */
    0,                           /* sq_inplace_repeat */
};

static PyTypeObject SLListType =
{
    PyObject_HEAD_INIT(NULL)
    0,                           /* ob_size           */
    "llist.sllist",              /* tp_name           */
    sizeof(SLListObject),        /* tp_basicsize      */
    0,                           /* tp_itemsize       */
    (destructor)sllist_dealloc,  /* tp_dealloc        */
    0,                           /* tp_print          */
    0,                           /* tp_getattr        */
    0,                           /* tp_setattr        */
    (cmpfunc)sllist_compare,     /* tp_compare        */
    (reprfunc)sllist_repr,       /* tp_repr           */
    0,                           /* tp_as_number      */
    &SLListSequenceMethods,      /* tp_as_sequence    */
    0,                           /* tp_as_mapping     */
    (hashfunc)sllist_hash,       /* tp_hash           */
    0,                           /* tp_call           */
    (reprfunc)sllist_str,        /* tp_str            */
    0,                           /* tp_getattro       */
    0,                           /* tp_setattro       */
    0,                           /* tp_as_buffer      */
    Py_TPFLAGS_DEFAULT,          /* tp_flags          */
    "Singly linked list",        /* tp_doc            */
    0,                           /* tp_traverse       */
    0,                           /* tp_clear          */
    0,                           /* tp_richcompare    */
    offsetof(SLListObject, weakref_list),
                                 /* tp_weaklistoffset */
    sllist_iter,                 /* tp_iter           */
    0,                           /* tp_iternext       */
    SLListMethods,               /* tp_methods        */
    SLListMembers,               /* tp_members        */
    0,                           /* tp_getset         */
    0,                           /* tp_base           */
    0,                           /* tp_dict           */
    0,                           /* tp_descr_get      */
    0,                           /* tp_descr_set      */
    0,                           /* tp_dictoffset     */
    (initproc)sllist_init,       /* tp_init           */
    0,                           /* tp_alloc          */
    sllist_new,                  /* tp_new            */
};


typedef struct
{
    PyObject_HEAD
    SLListObject* list;
    PyObject* current_node;
} SLListIteratorObject;

static void sllistiterator_dealloc(SLListIteratorObject* self)
{
    Py_XDECREF(self->current_node);
    Py_DECREF(self->list);

    self->ob_type->tp_free((PyObject*)self);
}

static PyObject* sllistiterator_new(PyTypeObject* type,
                                    PyObject* args,
                                    PyObject* kwds)
{
    SLListIteratorObject* self;
    PyObject* owner_list = NULL;

    if (!PyArg_UnpackTuple(args, "__new__", 1, 1, &owner_list))
        return NULL;

    if (!PyObject_TypeCheck(owner_list, &SLListType))
    {
        PyErr_SetString(PyExc_TypeError, "sllist argument expected");
        return NULL;
    }

    self = (SLListIteratorObject*)type->tp_alloc(type, 0);
    if (self == NULL)
        return NULL;

    self->list = (SLListObject*)owner_list;
    self->current_node = self->list->first;

    Py_INCREF(self->list);
    Py_INCREF(self->current_node);

    return (PyObject*)self;
}


static PyObject* sllistiterator_iternext(PyObject* self)
{
    SLListIteratorObject* iter_self = (SLListIteratorObject*)self;
    PyObject* value;
    PyObject* next_node;

    if (iter_self->current_node == NULL || iter_self->current_node == Py_None)
    {
        Py_XDECREF(iter_self->current_node);
        iter_self->current_node = NULL;
        PyErr_SetNone(PyExc_StopIteration);
        return NULL;
    }

    value = ((SLListNodeObject*)iter_self->current_node)->value;
    Py_INCREF(value);

    next_node = ((SLListNodeObject*)iter_self->current_node)->next;
    Py_INCREF(next_node);
    Py_DECREF(iter_self->current_node);
    iter_self->current_node = next_node;

    return value;
}



static PyTypeObject SLListIteratorType =
{
    PyObject_HEAD_INIT(NULL)
    0,                                  /* ob_size           */
    "llist.sllistiterator",             /* tp_name           */
    sizeof(SLListIteratorObject),       /* tp_basicsize      */
    0,                                  /* tp_itemsize       */
    (destructor)sllistiterator_dealloc, /* tp_dealloc        */
    0,                                  /* tp_print          */
    0,                                  /* tp_getattr        */
    0,                                  /* tp_setattr        */
    0,                                  /* tp_compare        */
    0,                                  /* tp_repr           */
    0,                                  /* tp_as_number      */
    0,                                  /* tp_as_sequence    */
    0,                                  /* tp_as_mapping     */
    0,                                  /* tp_hash           */
    0,                                  /* tp_call           */
    0,                                  /* tp_str            */
    0,                                  /* tp_getattro       */
    0,                                  /* tp_setattro       */
    0,                                  /* tp_as_buffer      */
    Py_TPFLAGS_DEFAULT,                 /* tp_flags          */
    "Singly linked list iterator",      /* tp_doc            */
    0,                                  /* tp_traverse       */
    0,                                  /* tp_clear          */
    0,                                  /* tp_richcompare    */
    0,                                  /* tp_weaklistoffset */
    0,                                  /* tp_iter           */
    sllistiterator_iternext,            /* tp_iternext       */
    0,                                  /* tp_methods        */
    0,                                  /* tp_members        */
    0,                                  /* tp_getset         */
    0,                                  /* tp_base           */
    0,                                  /* tp_dict           */
    0,                                  /* tp_descr_get      */
    0,                                  /* tp_descr_set      */
    0,                                  /* tp_dictoffset     */
    0,                                  /* tp_init           */
    0,                                  /* tp_alloc          */
    sllistiterator_new,                 /* tp_new            */
};



int sllist_init_type(void)
{
    return
        ((PyType_Ready(&SLListType) == 0) &&
         (PyType_Ready(&SLListNodeType) == 0) &&
         (PyType_Ready(&SLListIteratorType) == 0))
        ? 1 : 0;
}

void sllist_register(PyObject* module)
{
    Py_INCREF(&SLListType);
    Py_INCREF(&SLListNodeType);
    Py_INCREF(&SLListIteratorType);

    PyModule_AddObject(module, "sllist", (PyObject*)&SLListType);
    PyModule_AddObject(module, "sllistnode", (PyObject*)&SLListNodeType);
    PyModule_AddObject(module, "sllistiterator", (PyObject*)&SLListIteratorType);
}
