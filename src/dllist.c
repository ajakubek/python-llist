/* Copyright (c) 2011-2013 Adam Jakubek, Rafał Gałczyński
 * Copyright (c) 2017 Timothy Savannah
 * Released under the MIT license (see attached LICENSE file).
 */

#include <Python.h>
#include <structmember.h>
#include "py23macros.h"
#include "llist.h"
#include "llist_types.h"
#include "dllist_types.h"
#include "sllist_types.h"

#ifndef PyVarObject_HEAD_INIT
    #define PyVarObject_HEAD_INIT(type, size) \
        PyObject_HEAD_INIT(type) size,
#endif

#include <limits.h>

#include <stdarg.h>

#define START_MIDDLE_AFTER 10




/* Convenience function for creating list nodes.
 * Automatically update pointers in neigbours.
 */
static DLListNodeObject* dllistnode_create(PyObject* prev,
                                           PyObject* next,
                                           PyObject* value,
                                           PyObject* owner_list)
{
    DLListNodeObject *node;
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

    node = (DLListNodeObject*)PyObject_CallObject(
        (PyObject*)DLListNodeType, args);

    Py_XDECREF(args);

    /* prev is initialized to Py_None by default
     * (by dllistnode_new) */
    if (prev != NULL && prev != Py_None)
    {
        node->prev = prev;
        ((DLListNodeObject*)prev)->next = (PyObject*)node;
    }

    /* next is initialized to Py_None by default
     * (by dllistnode_new) */
    if (next != NULL && next != Py_None)
    {
        node->next = next;
        ((DLListNodeObject*)next)->prev = (PyObject*)node;
    }

    Py_DECREF(node->list_weakref);
    node->list_weakref = PyWeakref_NewRef(owner_list, NULL);

    return node;
}

/* Convenience function for deleting list nodes.
 * Automatically updates pointers in neigbours.
 */
static void dllistnode_delete(DLListNodeObject* node)
{
    if (node->prev != Py_None)
    {
        DLListNodeObject* prev = (DLListNodeObject*)node->prev;
        prev->next = node->next;
    }

    if (node->next != Py_None)
    {
        DLListNodeObject* next = (DLListNodeObject*)node->next;
        next->prev = node->prev;
    }

    node->prev = Py_None;
    node->next = Py_None;

    Py_DECREF((PyObject*)node);
}

/* Convenience function for formatting list node to a string.
 * Pass PyObject_Repr or PyObject_Str in the fmt_func argument. */
static PyObject* dllistnode_to_string(DLListNodeObject* self,
                                      reprfunc fmt_func,
                                      const char* prefix,
                                      const char* suffix)
{
    PyObject* str = NULL;
    PyObject* tmp_str;

    assert(fmt_func != NULL);

    str = Py23String_FromString(prefix);
    if (str == NULL)
        goto str_alloc_error;

    tmp_str = fmt_func(self->value);
    if (tmp_str == NULL)
        goto str_alloc_error;
    Py23String_ConcatAndDel(&str, tmp_str);

    tmp_str = Py23String_FromString(suffix);
    if (tmp_str == NULL)
        goto str_alloc_error;
    Py23String_ConcatAndDel(&str, tmp_str);

    return str;

str_alloc_error:
    Py_XDECREF(str);
    PyErr_SetString(PyExc_RuntimeError, "Failed to create string");
    return NULL;
}

static void dllistnode_dealloc(DLListNodeObject* self)
{
    Py_DECREF(self->list_weakref);
    Py_DECREF(self->value);
    Py_DECREF(Py_None);

    PyObject_Del((PyObject*)self);
}

static PyObject* dllistnode_new(PyTypeObject* type,
                                PyObject* args,
                                PyObject* kwds)
{
    DLListNodeObject* self;

    self = (DLListNodeObject*)type->tp_alloc(type, 0);
    if (self == NULL)
        return NULL;

    /* A single reference to Py_None is held for the whole
     * lifetime of a node. */
    Py_INCREF(Py_None);

    self->value = Py_None;
    self->prev = Py_None;
    self->next = Py_None;
    self->list_weakref = Py_None;

    Py_INCREF(self->value);
    Py_INCREF(self->list_weakref);

    return (PyObject*)self;
}

static int dllistnode_init(DLListNodeObject* self,
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

/*
 *  dllistnode_make - A slightly cheaper version that doesn't set next or prev
 */
static inline DLListNodeObject *dllistnode_make(DLListObject *dllist, PyObject *value)
{
    return (DLListNodeObject *)llistnode_make(DLListNodeType, (PyObject *)dllist, value);
}


static PyObject* dllistnode_call(DLListNodeObject* self,
                                 PyObject* args,
                                 PyObject* kw)
{
    Py_INCREF(self->value);
    return self->value;
}

static PyObject* dllistnode_repr(DLListNodeObject* self)
{
    return dllistnode_to_string(self, PyObject_Repr, "<dllistnode(", ")>");
}

static PyObject* dllistnode_str(DLListNodeObject* self)
{
    return dllistnode_to_string(self, PyObject_Str, "dllistnode(", ")");
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

PyTypeObject DLListNodeType[] = {
{
    PyVarObject_HEAD_INIT(NULL, 0)
    "llist.dllistnode",             /* tp_name */
    sizeof(DLListNodeObject),       /* tp_basicsize */
    0,                              /* tp_itemsize */
    (destructor)dllistnode_dealloc, /* tp_dealloc */
    0,                              /* tp_print */
    0,                              /* tp_getattr */
    0,                              /* tp_setattr */
    0,                              /* tp_compare */
    (reprfunc)dllistnode_repr,      /* tp_repr */
    0,                              /* tp_as_number */
    0,                              /* tp_as_sequence */
    0,                              /* tp_as_mapping */
    0,                              /* tp_hash */
    (ternaryfunc)dllistnode_call,   /* tp_call */
    (reprfunc)dllistnode_str,       /* tp_str */
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
    (initproc)dllistnode_init,      /* tp_init */
    0,                              /* tp_alloc */
    dllistnode_new,                 /* tp_new */
}
};


/* DLList */

static PyObject* dllist_node_at(PyObject* self, PyObject* indexObject);
static DLListNodeObject* dllist_get_node_internal(DLListObject* self, Py_ssize_t index);


/****************
**** Middle functions
********************
***/


/* _middle_do_recalc - 
 *    Do a recalulation of middle 
 */
static inline void _middle_do_recalc(DLListObject *self)
{
    Py_ssize_t midIdx;

    midIdx = self->size / 2;
    /* Set middle_idx to -1 so we don't use it on the lookup */

    self->middle_idx = -1;
    self->middle = (PyObject *) dllist_get_node_internal(self, midIdx);

    self->middle_idx = midIdx;
}

/* _middle_postappend_adjust -
 *     Do an adjustment after a move
 *
 *    sizeAdjust:   If called before size is incremented/decremented, pass the difference here
 */
static inline void _middle_postappend_adjust(DLListObject *self, int sizeAdjust)
{
    Py_ssize_t midpoint;

    midpoint = ( (self->size) + sizeAdjust) / 2;

    if ( self->middle_idx < midpoint )
    {
        /* We move at least one, then see if we need to move more */
        for( ; self->middle_idx < midpoint; self->middle_idx++ )
        {
            self->middle = ((DLListNodeObject*)self->middle)->next;
        }
    }
    else if ( self->middle_idx > midpoint )
    {
        for( ; self->middle_idx > midpoint ; self->middle_idx-- )
        {
            self->middle = ((DLListNodeObject*)self->middle)->prev;
        }
    }
 
}
    
/**
 *  _middle_popped_left_of_middle - When left-of-middle is popped,
 *     call this to adjust the middle index
 */
static inline void _middle_popped_left_of_middle(DLListObject *self)
{
    if ( self->middle != Py_None ) {
        self->middle_idx -= 1;
    }
}

/**
 * _middle_check_recalc -
      Do a recalc if we are past START_MIDDLE_AFTER
 */
static inline void _middle_check_recalc(DLListObject *self)
{
    if( self->size > START_MIDDLE_AFTER ) {
        _middle_do_recalc(self);
    }
}

/**
 *   _middle_check_adjust_or_recalc -
         Check if we are past START_MIDDLE_AFTER, and if so, update middle or recalc
 */
static inline void _middle_check_adjust_or_recalc(DLListObject *self)
{
    if ( self->size > START_MIDDLE_AFTER )
    {
        if ( self->middle != Py_None)
        {
            _middle_postappend_adjust(self, 0);
        }
        else
        {
            _middle_do_recalc(self);
        }
    }
}


/**
 *   _middle_check_on_shrink 
         After shrinking the list, check if we are small enough that we should clear middle,
           and do so if we are.

         return - 1 if middle was cleared, otherwise 0
*/
static inline int _middle_check_on_shrink(DLListObject *self)
{
    if ( self->size <= START_MIDDLE_AFTER )
    {
        self->middle = Py_None;
        self->middle_idx = -1;
        return 1;
    }
    return 0;
}

/* Convenience function for locating list nodes using index. */
static DLListNodeObject* dllist_get_node_internal(DLListObject* self,
                                                  Py_ssize_t index)
{
    Py_ssize_t i;
    Py_ssize_t midpoint = self->size / 2;
    DLListNodeObject* node;
    Py_ssize_t start_pos;
    int reverse_dir;

    if (index >= self->size || index < 0)
    {
        PyErr_SetString(PyExc_IndexError, "Index out of range");
        return NULL;
    }
    /* pick the closest base node */
    if (index <= midpoint)
    {
        if ( self->middle_idx != -1 && self->middle_idx - index < index )
        {
            node = (DLListNodeObject*)self->middle;
            start_pos = self->middle_idx;
            reverse_dir = 1;
        }
        else
        {
            node = (DLListNodeObject*)self->first;
            start_pos = 0;
            reverse_dir = 0;
        }
    }
    else
    {
        if ( self->middle_idx != -1 && index - self->middle_idx < self->size - index )
        {
            node = (DLListNodeObject*)self->middle;
            start_pos = self->middle_idx;
            reverse_dir = 0;
            
        }
        else
        {
            node = (DLListNodeObject*)self->last;
            start_pos = self->size - 1;
            reverse_dir = 1;
        }
    }

    assert((PyObject*)node != Py_None);

    if (!reverse_dir)
    {
        /* forward scan */
        for (i = start_pos; i < index; ++i)
            node = (DLListNodeObject*)node->next;
    }
    else
    {
        /* backward scan */
        for (i = start_pos; i > index; --i)
            node = (DLListNodeObject*)node->prev;
    }

    return node;
}

/* Convenience function for extending (concatenating in-place)
 * the list with elements from a sequence. */
static int dllist_extend_internal(DLListObject* self, PyObject* sequence)
{
    Py_ssize_t i = 0;
    Py_ssize_t sequence_len;

    if (PyObject_TypeCheck(sequence, DLListType) || PyObject_TypeCheck(sequence, SLListType))
    {
        /* Special path for extending with a LList (double or single)
         * It's not strictly required but greatly improves performance
         */
        PyObject *iter_node_obj = ((LListObject*)sequence)->first;
        LListNodeObject *iter_node;
        PyObject *new_node;

        sequence_len = ((LListObject*)sequence)->size;

        if ( unlikely(sequence_len == 0) )
            return 1;
        
        self->size += sequence_len;

        if ( self->size == sequence_len )
        {
            iter_node = (LListNodeObject*)iter_node_obj;

            new_node = (PyObject *)dllistnode_make(self, iter_node->value);
            self->first = new_node;
            self->last = new_node;
            ((DLListNodeObject *)new_node)->prev = Py_None;

            iter_node_obj = iter_node->next;
            sequence_len -= 1;
        }

        while (sequence_len-- > 0)
        {
            iter_node = (LListNodeObject*)iter_node_obj;

            new_node = (PyObject *)dllistnode_make(self, iter_node->value);

            ((DLListNodeObject *)self->last)->next = new_node;
            ((DLListNodeObject *)new_node)->prev = self->last;
            self->last = new_node;


            iter_node_obj = iter_node->next;
        }
        if( likely( self->last != Py_None) )
            ((DLListNodeObject *)self->last)->next = Py_None;

    }
    else
    {
        sequence_len = PySequence_Length(sequence);
        if ( unlikely(sequence_len == -1) )
        {
            PyErr_SetString(PyExc_ValueError, "Invalid sequence");
            return 0;
        }
        if ( unlikely(sequence_len == 0) )
            return 1;

        PyObject *item;
        PyObject *new_node;

        self->size += sequence_len;

        if ( self->size == sequence_len )
        {

            item = PySequence_GetItem(sequence, 0);
            if ( unlikely(item == NULL) )
            {
                PyErr_SetString(PyExc_ValueError,
                    "Failed to get element from sequence");
                return 0;
            }

            new_node = (PyObject *)dllistnode_make(self, item);
            self->first = new_node;
            self->last = new_node;
            ((DLListNodeObject *)new_node)->prev = Py_None;

            Py_DECREF(item);

            i = 1;
        }

        for(; i < sequence_len; i++)
        {

            item = PySequence_GetItem(sequence, i);
            if ( unlikely(item == NULL) )
            {
                PyErr_SetString(PyExc_ValueError,
                    "Failed to get element from sequence");
                return 0;
            }

            new_node = (PyObject *)dllistnode_make(self, item);

            ((DLListNodeObject *)self->last)->next = new_node;
            ((DLListNodeObject *)new_node)->prev = self->last;
            self->last = new_node;


            Py_DECREF(item);
        }

        if(self->last != Py_None)
            ((DLListNodeObject *)self->last)->next = Py_None;

    }

    _middle_check_adjust_or_recalc(self);

    return 1;
}

/* Convenience function for formatting list to a string.
 * Pass PyObject_Repr or PyObject_Str in the fmt_func argument. */
static PyObject* dllist_to_string(DLListObject* self,
                                  reprfunc fmt_func)
{
    PyObject* str = NULL;
    PyObject* comma_str = NULL;
    PyObject* tmp_str;
    DLListNodeObject* node = (DLListNodeObject*)self->first;

    assert(fmt_func != NULL);

    if (self->first == Py_None)
    {
        str = Py23String_FromString("dllist()");
        if (str == NULL)
            goto str_alloc_error;
        return str;
    }

    str = Py23String_FromString("dllist([");
    if (str == NULL)
        goto str_alloc_error;

    comma_str = Py23String_FromString(", ");
    if (comma_str == NULL)
        goto str_alloc_error;

    while ((PyObject*)node != Py_None)
    {
        if (node != (DLListNodeObject*)self->first)
            Py23String_Concat(&str, comma_str);

        tmp_str = fmt_func(node->value);
        if (tmp_str == NULL)
            goto str_alloc_error;
        Py23String_ConcatAndDel(&str, tmp_str);

        node = (DLListNodeObject*)node->next;
    }

    Py_DECREF(comma_str);
    comma_str = NULL;

    tmp_str = Py23String_FromString("])");
    if (tmp_str == NULL)
        goto str_alloc_error;
    Py23String_ConcatAndDel(&str, tmp_str);

    return str;

str_alloc_error:
    Py_XDECREF(str);
    Py_XDECREF(comma_str);
    PyErr_SetString(PyExc_RuntimeError, "Failed to create string");
    return NULL;
}

static void dllist_dealloc(DLListObject* self)
{
    PyObject* node = self->first;

    if (self->weakref_list != NULL)
        PyObject_ClearWeakRefs((PyObject*)self);

    while (node != Py_None)
    {
        PyObject* next_node = ((DLListNodeObject*)node)->next;
        dllistnode_delete((DLListNodeObject*)node);
        node = next_node;
    }

    Py_DECREF(Py_None);

    PyObject_Del((PyObject*)self);
}

static PyObject* dllist_new(PyTypeObject* type,
                            PyObject* args,
                            PyObject* kwds)
{
    DLListObject* self;

    self = (DLListObject*)type->tp_alloc(type, 0);
    if (self == NULL)
        return NULL;

    /* A single reference to Py_None is held for the whole
     * lifetime of a list. */
    Py_INCREF(Py_None);

    self->first = Py_None;
    self->last = Py_None;
    self->middle = Py_None;
    self->middle_idx = -1;
    self->size = 0;
    self->weakref_list = NULL;

    return (PyObject*)self;
}

static int dllist_init(DLListObject* self, PyObject* args, PyObject* kwds)
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

    return dllist_extend_internal(self, sequence) ? 0 : -1;
}

static PyObject* dllist_node_at(PyObject* self, PyObject* indexObject)
{
    DLListNodeObject* node;
    Py_ssize_t index;

    if (!Py23Int_Check(indexObject))
    {
        PyErr_SetString(PyExc_TypeError, "Index must be an integer");
        return NULL;
    }

    index = Py23Int_AsSsize_t(indexObject);

    if (index < 0)
        index = ((DLListObject*)self)->size + index;

    node = dllist_get_node_internal((DLListObject*)self, index);
    if ( node != NULL )
        Py_INCREF(node);

    return (PyObject*)node;
}

static PyObject* dllist_repr(DLListObject* self)
{
    return dllist_to_string(self, PyObject_Repr);
}

static PyObject* dllist_str(DLListObject* self)
{
    return dllist_to_string(self, PyObject_Str);
}

/* NOTE - THIS FUNCTION DOES NOT WORK!!
*
*   dllist([1, 5, 9]) has the SAME hash as dllist([5, 1, 9])
*     and thus it is NOT a hash function
*/
#if 0
static long dllist_hash(DLListObject* self)
{

    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;

    long hash = 0;
    PyObject* iter_node_obj = self->first;

    while (iter_node_obj != Py_None)
    {
        long obj_hash;
        DLListNodeObject* iter_node = (DLListNodeObject*)iter_node_obj;

        obj_hash = PyObject_Hash(iter_node->value);
        if (obj_hash == -1)
            return -1;

        hash ^= obj_hash;
        iter_node_obj = iter_node->next;
    }

    return hash;
}
#endif

static PyObject* dllist_richcompare(DLListObject* self,
                                    DLListObject* other,
                                    int op)
{
    DLListNodeObject* self_node;
    DLListNodeObject* other_node;
    int satisfied = 1;

    if (!PyObject_TypeCheck(other, DLListType))
    {
        Py_INCREF(Py_NotImplemented);
        return Py_NotImplemented;
    }

    if (self == other &&
        (op == Py_EQ || op == Py_LE || op == Py_GE))
        Py_RETURN_TRUE;

    if (self->size != other->size)
    {
        if (op == Py_EQ)
            Py_RETURN_FALSE;
        else if (op == Py_NE)
            Py_RETURN_TRUE;
    }

    /* Scan through sequences' items as long as they are equal. */
    self_node = (DLListNodeObject*)self->first;
    other_node = (DLListNodeObject*)other->first;

    while ((PyObject*)self_node != Py_None &&
            (PyObject*)other_node != Py_None)
    {
        satisfied = PyObject_RichCompareBool(
            self_node->value, other_node->value, Py_EQ);

        if (satisfied == 0)
            break;

        if (satisfied == -1)
            return NULL;

        self_node = (DLListNodeObject*)self_node->next;
        other_node = (DLListNodeObject*)other_node->next;
    }

    /* Compare last item */
    if (satisfied)
    {
        /* At least one of operands has been fully traversed.
         * Either self_node or other_node is equal to Py_None. */
        switch (op)
        {
        case Py_EQ:
            satisfied = (self_node == other_node);
            break;
        case Py_NE:
            satisfied = (self_node != other_node);
            break;
        case Py_LT:
            satisfied = ((PyObject*)other_node != Py_None);
            break;
        case Py_GT:
            satisfied = ((PyObject*)self_node != Py_None);
            break;
        case Py_LE:
            satisfied = ((PyObject*)self_node == Py_None);
            break;
        case Py_GE:
            satisfied = ((PyObject*)other_node == Py_None);
            break;
        default:
            assert(0 && "Invalid rich compare operator");
            PyErr_SetString(PyExc_ValueError, "Invalid rich compare operator");
            return NULL;
        }
    }
    else if (op != Py_EQ)
    {
        /* Both nodes are valid, but not equal */
        satisfied = PyObject_RichCompareBool(
            self_node->value, other_node->value, op);
    }

    if (satisfied)
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
}

static PyObject* dllist_appendleft(DLListObject* self, PyObject* arg)
{
    DLListNodeObject* new_node;

    if (PyObject_TypeCheck(arg, DLListNodeType))
        arg = ((DLListNodeObject*)arg)->value;

    new_node = dllistnode_create(NULL, self->first, arg, (PyObject*)self);

    self->first = (PyObject*)new_node;

    if (self->last == Py_None) {
        self->last = (PyObject*)new_node;
    }

    ++self->size;

    _middle_check_adjust_or_recalc(self);

    Py_INCREF((PyObject*)new_node);
    return (PyObject*)new_node;
}

static PyObject* dllist_appendright(DLListObject* self, PyObject* arg)
{
    DLListNodeObject* new_node;

    if (PyObject_TypeCheck(arg, DLListNodeType))
        arg = ((DLListNodeObject*)arg)->value;

    new_node = dllistnode_create(self->last, NULL, arg, (PyObject*)self);

    self->last = (PyObject*)new_node;

    if (self->first == Py_None)
        self->first = (PyObject*)new_node;

    ++self->size;

    _middle_check_adjust_or_recalc(self);

    Py_INCREF((PyObject*)new_node);
    return (PyObject*)new_node;
}

static PyObject* dllist_insert(DLListObject* self, PyObject* args)
{
    PyObject* val = NULL;
    PyObject* ref_node = NULL;
    DLListNodeObject* new_node;

    if (!PyArg_UnpackTuple(args, "insert", 1, 2, &val, &ref_node))
        return NULL;

    if (PyObject_TypeCheck(val, DLListNodeType))
        val = ((DLListNodeObject*)val)->value;

    if (ref_node == NULL || ref_node == Py_None)
    {
        /* append item at the end of the list */
        new_node = dllistnode_create(self->last, NULL, val, (PyObject*)self);

        self->last = (PyObject*)new_node;

        if (self->first == Py_None)
            self->first = (PyObject*)new_node;
    }
    else
    {
        PyObject* list_ref;

        /* insert item before ref_node */
        if (!PyObject_TypeCheck(ref_node, DLListNodeType))
        {
            PyErr_SetString(PyExc_TypeError,
                "ref_node argument must be a dllistnode");
            return NULL;
        }

        if (((DLListNodeObject*)ref_node)->list_weakref == Py_None)
        {
            PyErr_SetString(PyExc_ValueError,
                "dllistnode does not belong to a list");
            return NULL;
        }

        list_ref = PyWeakref_GetObject(
            ((DLListNodeObject*)ref_node)->list_weakref);
        if (list_ref != (PyObject*)self)
        {
            PyErr_SetString(PyExc_ValueError,
                "dllistnode belongs to another list");
            return NULL;
        }

        new_node = dllistnode_create(
            ((DLListNodeObject*)ref_node)->prev,
            ref_node, val, (PyObject*)self);

        if (ref_node == self->first)
            self->first = (PyObject*)new_node;

        if (self->last == Py_None)
            self->last = (PyObject*)new_node;

    }

    ++self->size;
    if( self->size > START_MIDDLE_AFTER ) {
        /* TODO: Optimize by direction?
            We can after the "insert" function is changed to support integer index,
            but not with element insert
        */
        _middle_do_recalc(self);
    }


    Py_INCREF((PyObject*)new_node);
    return (PyObject*)new_node;
}

static PyObject* dllist_extendleft(DLListObject* self, PyObject* sequence)
{
    Py_ssize_t i = 0;
    Py_ssize_t sequence_len;

    if (PyObject_TypeCheck(sequence, DLListType) || PyObject_TypeCheck(sequence, SLListType))
    {
        /* Special path for extending with a LList. Better performance. */
        PyObject* iter_node_obj = ((LListObject*)sequence)->first;
        LListNodeObject *iter_node;
        PyObject *new_node;

        sequence_len = ((LListObject*)sequence)->size;
        if ( unlikely(sequence_len == 0) )
            Py_RETURN_NONE;

        self->size += sequence_len;

        if ( self->size == sequence_len )
        {
            iter_node = (LListNodeObject*)iter_node_obj;

            new_node = (PyObject *)dllistnode_make(self, iter_node->value);
            self->first = new_node;
            self->last = new_node;
            ((DLListNodeObject *)new_node)->next = Py_None;

            iter_node_obj = iter_node->next;

            sequence_len -= 1;
        }

        while (sequence_len-- > 0)
        {
            iter_node = (LListNodeObject*)iter_node_obj;

            new_node = (PyObject *)dllistnode_make(self, iter_node->value);

            ((DLListNodeObject *)self->first)->prev = new_node;
            ((DLListNodeObject *)new_node)->next = self->first;
            self->first = new_node;


            iter_node_obj = iter_node->next;
        }
        if ( likely(self->first != Py_None) )
            ((DLListNodeObject*)self->first)->prev = Py_None;


    }
    else
    {

        sequence_len = PySequence_Length(sequence);
        if ( unlikely(sequence_len == -1) )
        {
            PyErr_SetString(PyExc_ValueError, "Invalid sequence");
            return NULL;
        }

        if ( unlikely(sequence_len == 0) )
            Py_RETURN_NONE;

        PyObject *item;
        PyObject *new_node;
        DLListNodeObject *first;

        if ( self->size == 0 )
        {
            item = PySequence_GetItem(sequence, 0);
            if ( unlikely(item == NULL) )
            {
                PyErr_SetString(PyExc_ValueError,
                    "Failed to get element from sequence");
                return NULL;
            }

            new_node = (PyObject *)dllistnode_make(self, item);
            self->first = new_node;
            self->last = new_node;
            ((DLListNodeObject *)new_node)->next = Py_None;

            Py_DECREF(item);
            i = 1;
        }

        self->size += sequence_len;

        first = (DLListNodeObject *)self->first;
        for (; i < sequence_len; ++i)
        {

            item = PySequence_GetItem(sequence, i);
            if ( unlikely(item == NULL) )
            {
                PyErr_SetString(PyExc_ValueError,
                    "Failed to get element from sequence");
                return NULL;
            }

            new_node = (PyObject *)dllistnode_make(self, item);

            first->prev = new_node;
            ((DLListNodeObject *)new_node)->next = (PyObject *)first;
            self->first = new_node;
            first = (DLListNodeObject *)new_node;


            Py_DECREF(item);
        }
        if ( likely( (PyObject *)first != Py_None) )
            first->prev = Py_None;
    }


    _middle_check_adjust_or_recalc(self);

    Py_RETURN_NONE;
}

static PyObject* dllist_extendright(DLListObject* self, PyObject* arg)
{
    if (!dllist_extend_internal(self, arg))
        return NULL;

    Py_RETURN_NONE;
}

static PyObject* dllist_clear(DLListObject* self)
{
    PyObject* iter_node_obj = self->first;

    while (iter_node_obj != Py_None)
    {
        DLListNodeObject* iter_node = (DLListNodeObject*)iter_node_obj;

        iter_node_obj = iter_node->next;
        dllistnode_delete(iter_node);
    }

    self->first = Py_None;
    self->last = Py_None;
    self->middle = Py_None;
    self->middle_idx = -1;
    self->size = 0;

    Py_RETURN_NONE;
}

static PyObject* dllist_popleft(DLListObject* self)
{
    DLListNodeObject* del_node;
    PyObject* value;

    if (self->first == Py_None)
    {
        PyErr_SetString(PyExc_ValueError, "List is empty");
        return NULL;
    }

    del_node = (DLListNodeObject*)self->first;

    self->first = del_node->next;
    if (self->last == (PyObject*)del_node)
        self->last = Py_None;

    --self->size;
    if ( ! _middle_check_on_shrink(self) )
    {
        self->middle_idx -= 1;
        _middle_postappend_adjust(self, 0);
    }

    Py_INCREF(del_node->value);
    value = del_node->value;

    dllistnode_delete(del_node);

    return value;
}

static PyObject* dllist_popright(DLListObject* self)
{
    DLListNodeObject* del_node;
    PyObject* value;

    if (self->last == Py_None)
    {
        PyErr_SetString(PyExc_ValueError, "List is empty");
        return NULL;
    }

    del_node = (DLListNodeObject*)self->last;

    self->last = del_node->prev;
    if (self->first == (PyObject*)del_node)
        self->first = Py_None;

    --self->size;
    if( ! _middle_check_on_shrink(self) )
    {
        _middle_postappend_adjust(self, 0);
    }


    Py_INCREF(del_node->value);
    value = del_node->value;

    dllistnode_delete(del_node);

    return value;
}


static PyObject* dllist_pop(DLListObject* self, PyObject *arg)
{
    DLListNodeObject *del_node;

    PyObject *value;
    PyObject *indexObject = NULL;

    Py_ssize_t index;
    Py_ssize_t i;

    if (!PyArg_UnpackTuple(arg, "pop", 0, 1, &indexObject))
    {
        return NULL;
    }

    /* If we did not get passed the "index" arg, just return popright */
    if ( indexObject == NULL )
    {
        return dllist_popright( self );
    }

    if (!Py23Int_Check(indexObject))
    {
        PyErr_SetString(PyExc_TypeError, "Index must be an integer");
        return NULL;
    }

    index = Py23Int_AsSsize_t(indexObject);


    /* Negative index */
    if (index < 0)
        index = ((DLListObject*)self)->size + index;

    /* If index is 0, popleft */
    if ( index == 0 )
    {
        return dllist_popleft( self );
    }
    else if ( index + 1 == ((DLListObject*)self)->size )
    {
        return dllist_popright(self);
    }

    if ( (PyObject*)self->first == Py_None)
    {
        PyErr_SetString(PyExc_ValueError, "List is empty");
        return NULL;
    }

    /* Either a negative greater than index size, or a positive greater than size */
    if ( index < 0 || index >= ((DLListObject*)self)->size )
    {
        PyErr_SetString(PyExc_IndexError, "Index out of range");
        return NULL;
    }

    if ( index == self->middle_idx )
    {
        del_node = (DLListNodeObject*)self->middle;
    }
    else if ( index < ((DLListObject*)self)->size / 2 )
    {
        if ( self->middle_idx != -1 && self->middle_idx - index < index )
        {
            del_node = (DLListNodeObject*) ((DLListNodeObject*) self->middle)->prev;
            for(i=1; i < self->middle_idx - index; i++) {
                del_node = (DLListNodeObject*)del_node->prev;
            }
        }
        else
        {
            /* Start at first node, and walk to the one we will pop */
            del_node = (DLListNodeObject*) ((DLListNodeObject*) self->first)->next;
            for(i=1; i < index; i++) {
                del_node = (DLListNodeObject*)del_node->next;
            }
        }
        _middle_popped_left_of_middle(self);
        
    }
    else
    {
        if ( self->middle_idx != -1 && index - self->middle_idx < self->size - index )
        {
            del_node = (DLListNodeObject*) ((DLListNodeObject*) self->middle)->next;
            for(i=1; i < index - self->middle_idx; i++) {
                del_node = (DLListNodeObject*)del_node->next;
            }
        }
        else
        {
            /* Start at last node, and walk back to the one we will pop */
            del_node = (DLListNodeObject*) ((DLListNodeObject*) self->last)->prev;
            for(i=((DLListObject*)self)->size - 2; i > index; i--) {
                del_node = (DLListNodeObject*)del_node->prev;
            }
        }
    }


    --self->size;


    Py_INCREF(del_node->value);
    value = del_node->value;

    dllistnode_delete(del_node);

    if ( ! _middle_check_on_shrink(self) )
    {
        if ( index != self->middle_idx )
        {
            _middle_postappend_adjust(self, 0);
        }
        else
        {
            _middle_check_recalc(self);
        }
    }

    return value;
}

static PyObject* dllist_remove(DLListObject* self, PyObject* arg)
{
    DLListNodeObject* del_node;
    PyObject* list_ref;
    PyObject* value;

    if (!PyObject_TypeCheck(arg, DLListNodeType))
    {
        PyErr_SetString(PyExc_TypeError, "Argument must be a dllistnode");
        return NULL;
    }

    if (self->first == Py_None)
    {
        PyErr_SetString(PyExc_ValueError, "List is empty");
        return NULL;
    }

    del_node = (DLListNodeObject*)arg;

    if (del_node->list_weakref == Py_None)
    {
        PyErr_SetString(PyExc_ValueError,
            "dllistnode does not belong to a list");
        return NULL;
    }

    list_ref = PyWeakref_GetObject(del_node->list_weakref);
    if (list_ref != (PyObject*)self)
    {
        PyErr_SetString(PyExc_ValueError,
            "dllistnode belongs to another list");
        return NULL;
    }

    if (self->first == arg)
        self->first = del_node->next;
    if (self->last == arg)
        self->last = del_node->prev;

    --self->size;
    if ( ! _middle_check_on_shrink(self) )
    {
        /* TODO: Optimize direction */
        _middle_do_recalc(self);
    }

    Py_INCREF(del_node->value);
    value = del_node->value;

    /* unlink from parent list */
    Py_DECREF(del_node->list_weakref);
    Py_INCREF(Py_None);
    del_node->list_weakref = Py_None;

    dllistnode_delete(del_node);

    return value;
}

static PyObject* dllist_rotate(DLListObject* self, PyObject* nObject)
{
    Py_ssize_t n;
    Py_ssize_t split_idx;
    Py_ssize_t n_mod;
    DLListNodeObject* new_first;
    DLListNodeObject* new_last;

    if (self->size <= 1)
        Py_RETURN_NONE;

    if (!Py23Int_Check(nObject))
    {
        PyErr_SetString(PyExc_TypeError, "n must be an integer");
        return NULL;
    }

    n = Py23Int_AsSsize_t(nObject);
    n_mod = py_ssize_t_abs(n) % self->size;

    if (n_mod == 0)
        Py_RETURN_NONE; /* no-op */

    if (n > 0)
        split_idx = self->size - n_mod; /* rotate right */
    else
        split_idx = n_mod;  /* rotate left */

    new_last = dllist_get_node_internal(self, split_idx - 1);
    assert(new_last != NULL);
    new_first = (DLListNodeObject*)new_last->next;

    ((DLListNodeObject*)self->first)->prev = self->last;
    ((DLListNodeObject*)self->last)->next = self->first;

    new_first->prev = Py_None;
    new_last->next = Py_None;

    self->first = (PyObject*)new_first;
    self->last = (PyObject*)new_last;

    _middle_check_recalc(self);

    Py_RETURN_NONE;
}

static PyObject* dllist_iter(PyObject* self)
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

    result = PyObject_CallObject((PyObject*)DLListIteratorType, args);

    Py_DECREF(args);

    return result;
}

static Py_ssize_t dllist_len(PyObject* self)
{
    DLListObject* list = (DLListObject*)self;
    return list->size;
}

static PyObject* dllist_concat(PyObject* self, PyObject* other)
{
    DLListObject* new_list;

    new_list = (DLListObject*)PyObject_CallObject(
        (PyObject*)DLListType, NULL);

    if (!dllist_extend_internal(new_list, self) ||
        !dllist_extend_internal(new_list, other))
    {
        Py_DECREF(new_list);
        return NULL;
    }

    return (PyObject*)new_list;
}

static PyObject* dllist_inplace_concat(PyObject* self, PyObject* other)
{
    if (!dllist_extend_internal((DLListObject*)self, other))
        return NULL;

    Py_INCREF(self);
    return self;
}

static PyObject* dllist_repeat(PyObject* self, Py_ssize_t count)
{
    DLListObject* new_list;
    Py_ssize_t i;

    new_list = (DLListObject*)PyObject_CallObject(
        (PyObject*)DLListType, NULL);

    for (i = 0; i < count; ++i)
    {
        if (!dllist_extend_internal(new_list, self))
        {
            Py_DECREF(new_list);
            return NULL;
        }
    }

    return (PyObject*)new_list;
}

static PyObject* dllist_get_item(PyObject* self, Py_ssize_t index)
{
    DLListNodeObject* node;

    node = dllist_get_node_internal((DLListObject*)self, index);
    if (node != NULL)
    {
        PyObject* value = node->value;

        Py_XINCREF(value);

        return value;
    }

    return NULL;
}

static int dllist_set_item(PyObject* self, Py_ssize_t index, PyObject* val)
{
    DLListObject* list = (DLListObject*)self;
    DLListNodeObject* node;
    PyObject* oldval;

    node = dllist_get_node_internal(list, index);
    if (node == NULL)
        return -1;

    /* Here is a tricky (and undocumented) part of sequence protocol.
     * Python will pass NULL as item value when item is deleted with:
     * del list[index] */
    if (val == NULL)
    {
        PyObject* result;

        result = dllist_remove(list, (PyObject*)node);

        Py_XDECREF(result);

        return (result != NULL) ? 0 : -1;
    }

    /* The rest of this function handles normal assignment:
     * list[index] = item */
    if (PyObject_TypeCheck(val, DLListNodeType))
        val = ((DLListNodeObject*)val)->value;

    oldval = node->value;

    Py_INCREF(val);
    node->value = val;
    Py_DECREF(oldval);

    return 0;
}


static int dllist_contains(PyObject *self, PyObject *value)
{
    DLListNodeObject *node;

    node = (DLListNodeObject *) ((DLListObject*)self)->first;

    while ( (PyObject *)node != Py_None )
    {
        if( node->value == value )
            return 1;

        node = (DLListNodeObject *)node->next;
    }

    return 0;
}



static PyObject* dllist_index(DLListObject *self, PyObject *value)
{

    DLListNodeObject *node;
    Py_ssize_t idx;

    node = (DLListNodeObject *) self->first;
    idx = 0;

    while ( (PyObject*)node != Py_None )
    {
        if( node->value == value )
            return PyLong_FromSsize_t(idx);

        node = (DLListNodeObject *)node->next;
        idx += 1;
    }
    PyErr_Format(PyExc_ValueError, "No such value in list");
    return NULL;
}

static PyObject* dllist_rindex(DLListObject *self, PyObject *value)
{

    DLListNodeObject *node;
    Py_ssize_t idx;

    node = (DLListNodeObject *) self->last;
    idx = self->size - 1;

    while ( (PyObject*)node != Py_None )
    {
        if( node->value == value )
            return PyLong_FromSsize_t(idx);

        node = (DLListNodeObject *)node->prev;
        idx -= 1;
    }
    PyErr_Format(PyExc_ValueError, "No such value in list");
    return NULL;
}

/*
 *   dllist_slice - Slice function assuming normalized indexes. 
 *
 *     For potentially non-normalized, use dllist_simpleslice
 *       or call _normalize_indexes
 *
 *    self - DLList to slice from
 *    start_idx    - Start of slicing (normalized)
 *    end_idx      - End of slicing (normalized)
 *    step         - Slice step
 *    sliceLength  - Length of resulting slice. Pass -1 to calculate.
 */
static PyObject *dllist_slice(DLListObject *self, Py_ssize_t start_idx, Py_ssize_t end_idx, Py_ssize_t step, Py_ssize_t sliceLength)
{
    DLListObject *ret;
    DLListNodeObject *cur;
    DLListNodeObject *new_node;
    Py_ssize_t i;
    Py_ssize_t remaining;
    int direction = 0;
    int pre_walk_direction;

    Py_ssize_t stepI;

    Py_ssize_t diff_start_left;
    Py_ssize_t diff_end_right;

    ret = (DLListObject *)dllist_new(DLListType, Py_None, Py_None);

    if ( sliceLength == -1 )
    {
        sliceLength = end_idx - start_idx; /* Reusing end_idx as max */
        if(step > 1 )
        {
            sliceLength = sliceLength / step + ( end_idx % step ? 1 : 0 );
        }
    }


    if ( step > 1 )
    {
        Py_ssize_t tmp_slice_resize;
        tmp_slice_resize = start_idx + (step * sliceLength);
        if ( tmp_slice_resize < end_idx )
            end_idx = tmp_slice_resize;
    }



    if ( sliceLength == 0 )
        return (PyObject *)ret;


    diff_start_left = start_idx;
    diff_end_right = self->size - 1 - end_idx;

    remaining = py_ssize_min(diff_start_left, diff_end_right);
    if (self->middle_idx != -1 )
    {
        Py_ssize_t diff_mid_left;
        Py_ssize_t diff_mid_right;

        diff_mid_left = py_ssize_t_abs( self->middle_idx - start_idx );
        diff_mid_right = py_ssize_t_abs ( end_idx - self->middle_idx );

        remaining = py_ssize_min(remaining, diff_mid_left);
        remaining = py_ssize_min(remaining, diff_mid_right);

        if ( remaining == diff_mid_left )
        {
            direction = 1;
            if ( start_idx < self->middle_idx )
            {
                pre_walk_direction = -1;
            }
            else
            {
                pre_walk_direction = 1;
            }

            cur = (DLListNodeObject *)self->middle;
        }
        else if( remaining == diff_mid_right )
        {
            direction = -1;
            if ( end_idx < self->middle_idx )
            {
                pre_walk_direction = -1;
                remaining += calc_end_difference_step(start_idx, end_idx, step);
            }
            else if ( end_idx > self->middle_idx )
            {
                pre_walk_direction = 1;
                remaining -= calc_end_difference_step(start_idx, end_idx, step);
                if ( remaining < 0 )
                {
                    /* If here, we had to change direction because of step-end */
                    pre_walk_direction = -1;
                    remaining *= -1;
                }
            }
            else
            {
                pre_walk_direction = -1;
                remaining += calc_end_difference_step(start_idx, end_idx, step);

            }

            cur = (DLListNodeObject *)self->middle;
        }
    }
    
    if ( direction == 0 )
    {
        if ( remaining == diff_start_left )
        {
            direction = 1;
            pre_walk_direction = 1;
            cur = (DLListNodeObject *)self->first;
        }
        else /* diff_end_right */
        {
            direction = -1;
            pre_walk_direction = -1;
            remaining += calc_end_difference_step(start_idx, end_idx, step);
            cur = (DLListNodeObject *)self->last;
        }
    }


    if ( pre_walk_direction == 1 )
    {
        for(i=0; i < remaining; i++)
            cur = (DLListNodeObject*)cur->next;
    }
    else
    {
        for(i=remaining; i > 0; i--)
            cur = (DLListNodeObject*)cur->prev;
    }
    
    new_node = dllistnode_make(self, cur->value);
    new_node->prev = new_node->next = Py_None;

    ret->first = ret->last = (PyObject *)new_node;
    ret->size = 1;


    if ( direction == 1 )
    {
        DLListNodeObject *prev;
        prev = new_node;


        while ( ret->size < sliceLength )
        {
            stepI = step;
            while(stepI--)
                cur = (DLListNodeObject*)cur->next;

            new_node = dllistnode_make(self, cur->value);

            new_node->prev = (PyObject *)prev;
            prev->next = (PyObject *)new_node;
            prev = new_node;

            ret->last = (PyObject *)new_node;

            ret->size += 1;

            
        }
        ((DLListNodeObject*)ret->last)->next = Py_None;

    }
    else
    {
        DLListNodeObject *next;

        next = new_node;


        while ( ret->size < sliceLength )
        {
            stepI = step;
            while(stepI--)
                cur = (DLListNodeObject*)cur->prev;

            new_node = dllistnode_make(self, cur->value);

            new_node->next = (PyObject *)next;
            next->prev = (PyObject *)new_node;
            next = new_node;

            ret->first = (PyObject *)new_node;

            ret->size += 1;

        }
        ((DLListNodeObject*)ret->last)->next = Py_None;
        ((DLListNodeObject*)ret->first)->prev = Py_None;

    }

    _middle_check_recalc(ret);

    return (PyObject*) ret;

}

/*
 *   dllist_simpleslice - Simple (PySequence) slices. Can take non-normalized indexes (like negatives)
 */
static PyObject *dllist_simpleslice(DLListObject *self, Py_ssize_t idx_start, Py_ssize_t idx_end)
{
    debugmsg("Calling simpleslice: %p %ld %ld\n", self, idx_start, idx_end);
    if( !_normalize_indexes(self->size, &idx_start, &idx_end) )
    {
        DLListObject *ret = (DLListObject *)dllist_new(DLListType, NULL, NULL);
        return (PyObject *)ret;
    }

    return dllist_slice(self, idx_start, idx_end, 1, -1);
}

static PyObject *dllist_subscript(DLListObject *self, PyObject *item)
{
    
    if ( PyIndex_Check(item) )
    {
        Py_ssize_t i;

        i = PyNumber_AsSsize_t(item, PyExc_IndexError);

        if ( i == -1 && PyErr_Occurred() )
            return NULL;

        if ( i < 0 )
            i += self->size;

        return dllist_get_item((PyObject *)self, i);
    }
    
    if ( PySlice_Check(item) )
    {
        Py_ssize_t start, stop, step, sliceLength;

        if ( PySlice_GetIndicesEx( (GET_INDICES_TYPE *)item, self->size, &start, &stop, &step, &sliceLength ) )
            return NULL; /* Error */

        return dllist_slice(self, start, stop, step, sliceLength);
    }
    else
    {
        
        PyErr_Format(PyExc_TypeError, "Indices must be integers, not %s", item->ob_type->tp_name);
        return NULL;
    }

}



static PyMethodDef DLListMethods[] =
{
    { "appendleft", (PyCFunction)dllist_appendleft, METH_O,
      "Append element at the beginning of the list" },
    { "append", (PyCFunction)dllist_appendright, METH_O,
      "Append element at the end of the list" },
    { "appendright", (PyCFunction)dllist_appendright, METH_O,
      "Append element at the end of the list" },
    { "clear", (PyCFunction)dllist_clear, METH_NOARGS,
      "Remove all elements from the list" },
    { "extend", (PyCFunction)dllist_extendright, METH_O,
      "Append elements from iterable at the right side of the list" },
    { "extendleft", (PyCFunction)dllist_extendleft, METH_O,
      "Append elements from iterable at the left side of the list" },
    { "extendright", (PyCFunction)dllist_extendright, METH_O,
      "Append elements from iterable at the right side of the list" },
    { "insert", (PyCFunction)dllist_insert, METH_VARARGS,
      "Inserts element before node" },
    { "index", (PyCFunction)dllist_index, METH_O,
      "Returns the first index of a value" },
    { "rindex", (PyCFunction)dllist_rindex, METH_O,
      "Returns the last index of a value" },
    { "nodeat", (PyCFunction)dllist_node_at, METH_O,
      "Return node at index" },
    { "popleft", (PyCFunction)dllist_popleft, METH_NOARGS,
      "Remove first element from the list and return it" },
    { "pop", (PyCFunction)dllist_pop, METH_VARARGS,
      "Remove an element by index from the list and return it, or last item if no index provided" },
    { "popright", (PyCFunction)dllist_popright, METH_NOARGS,
      "Remove last element from the list and return it" },
    { "remove", (PyCFunction)dllist_remove, METH_O,
      "Remove element from the list" },
    { "rotate", (PyCFunction)dllist_rotate, METH_O,
      "Rotate the list n steps to the right" },
    { NULL },   /* sentinel */
};

static PyMemberDef DLListMembers[] =
{
    { "first", T_OBJECT_EX, offsetof(DLListObject, first), READONLY,
      "First node" },
    { "last", T_OBJECT_EX, offsetof(DLListObject, last), READONLY,
      "Next node" },
    { "middle", T_OBJECT_EX, offsetof(DLListObject, middle), READONLY,
      "Middle node" },
/*    { "middle_idx", T_INT, offsetof(DLListObject, middle_idx), READONLY,
      "Middle node index" },
*/
    { "size", T_INT, offsetof(DLListObject, size), READONLY,
      "Number of elements in the list" },
    { NULL },   /* sentinel */
};

static PySequenceMethods DLListSequenceMethods[] = {
{
    dllist_len,                 /* sq_length */
    dllist_concat,              /* sq_concat */
    dllist_repeat,              /* sq_repeat */
    dllist_get_item,            /* sq_item */
    (ssizessizeargfunc)dllist_simpleslice,  /* sq_slice */
    dllist_set_item,            /* sq_ass_item */
    0,                          /* sq_ass_slice */
    dllist_contains,            /* sq_contains */
    dllist_inplace_concat,      /* sq_inplace_concat */
    0,                          /* sq_inplace_repeat */
}
}
;

static PyMappingMethods DLListMappingMethods[] = {
{
    dllist_len,                /* mp_length */
    (binaryfunc)dllist_subscript,          /* mp_subscript */
    0,                         /* mp_ass_subscript */
}
};

PyTypeObject DLListType[] = {
{
    PyVarObject_HEAD_INIT(NULL, 0)
    "llist.dllist",             /* tp_name */
    sizeof(DLListObject),       /* tp_basicsize */
    0,                          /* tp_itemsize */
    (destructor)dllist_dealloc, /* tp_dealloc */
    0,                          /* tp_print */
    0,                          /* tp_getattr */
    0,                          /* tp_setattr */
    0,                          /* tp_compare */
    (reprfunc)dllist_repr,      /* tp_repr */
    0,                          /* tp_as_number */
    DLListSequenceMethods,      /* tp_as_sequence */
    DLListMappingMethods,                          /* tp_as_mapping */
    0,      /* tp_hash */
    0,                          /* tp_call */
    (reprfunc)dllist_str,       /* tp_str */
    0,                          /* tp_getattro */
    0,                          /* tp_setattro */
    0,                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,         /* tp_flags */
    "Doubly linked list",       /* tp_doc */
    0,                          /* tp_traverse */
    0,                          /* tp_clear */
    (richcmpfunc)dllist_richcompare,
                                /* tp_richcompare */
    offsetof(DLListObject, weakref_list),
                                /* tp_weaklistoffset */
    dllist_iter,                /* tp_iter */
    0,                          /* tp_iternext */
    DLListMethods,              /* tp_methods */
    DLListMembers,              /* tp_members */
    0,                          /* tp_getset */
    0,                          /* tp_base */
    0,                          /* tp_dict */
    0,                          /* tp_descr_get */
    0,                          /* tp_descr_set */
    0,                          /* tp_dictoffset */
    (initproc)dllist_init,      /* tp_init */
    0,                          /* tp_alloc */
    dllist_new,                 /* tp_new */
}
};


/* DLListIterator */

typedef struct
{
    PyObject_HEAD
    DLListObject* list;
    PyObject* current_node;
} DLListIteratorObject;

static void dllistiterator_dealloc(DLListIteratorObject* self)
{
    Py_XDECREF(self->current_node);
    Py_DECREF(self->list);

    PyObject_Del((PyObject*)self);
}

static PyObject* dllistiterator_new(PyTypeObject* type,
                                    PyObject* args,
                                    PyObject* kwds)
{
    DLListIteratorObject* self;
    PyObject* owner_list = NULL;

    if (!PyArg_UnpackTuple(args, "__new__", 1, 1, &owner_list))
        return NULL;

    if (!PyObject_TypeCheck(owner_list, DLListType))
    {
        PyErr_SetString(PyExc_TypeError, "dllist argument expected");
        return NULL;
    }

    self = (DLListIteratorObject*)type->tp_alloc(type, 0);
    if (self == NULL)
        return NULL;

    self->list = (DLListObject*)owner_list;
    self->current_node = self->list->first;

    Py_INCREF(self->list);
    Py_INCREF(self->current_node);

    return (PyObject*)self;
}

static PyObject* dllistiterator_iternext(PyObject* self)
{
    DLListIteratorObject* iter_self = (DLListIteratorObject*)self;
    PyObject* value;
    PyObject* next_node;

    if (iter_self->current_node == NULL || iter_self->current_node == Py_None)
    {
        Py_XDECREF(iter_self->current_node);
        iter_self->current_node = NULL;
        PyErr_SetNone(PyExc_StopIteration);
        return NULL;
    }

    value = ((DLListNodeObject*)iter_self->current_node)->value;
    Py_INCREF(value);

    next_node = ((DLListNodeObject*)iter_self->current_node)->next;
    Py_INCREF(next_node);
    Py_DECREF(iter_self->current_node);
    iter_self->current_node = next_node;

    return value;
}

PyTypeObject DLListIteratorType[] = {
{
    PyVarObject_HEAD_INIT(NULL, 0)
    "llist.dllistiterator",             /* tp_name */
    sizeof(DLListIteratorObject),       /* tp_basicsize */
    0,                                  /* tp_itemsize */
    (destructor)dllistiterator_dealloc, /* tp_dealloc */
    0,                                  /* tp_print */
    0,                                  /* tp_getattr */
    0,                                  /* tp_setattr */
    0,                                  /* tp_compare */
    0,                                  /* tp_repr */
    0,                                  /* tp_as_number */
    0,                                  /* tp_as_sequence */
    0,                                  /* tp_as_mapping */
    0,                                  /* tp_hash */
    0,                                  /* tp_call */
    0,                                  /* tp_str */
    0,                                  /* tp_getattro */
    0,                                  /* tp_setattro */
    0,                                  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                 /* tp_flags */
    "Doubly linked list iterator",      /* tp_doc */
    0,                                  /* tp_traverse */
    0,                                  /* tp_clear */
    0,                                  /* tp_richcompare */
    0,                                  /* tp_weaklistoffset */
    0,                                  /* tp_iter */
    dllistiterator_iternext,            /* tp_iternext */
    0,                                  /* tp_methods */
    0,                                  /* tp_members */
    0,                                  /* tp_getset */
    0,                                  /* tp_base */
    0,                                  /* tp_dict */
    0,                                  /* tp_descr_get */
    0,                                  /* tp_descr_set */
    0,                                  /* tp_dictoffset */
    0,                                  /* tp_init */
    0,                                  /* tp_alloc */
    dllistiterator_new,                 /* tp_new */
}
};


int dllist_init_type(void)
{
    return
        ((PyType_Ready(DLListType) == 0) &&
         (PyType_Ready(DLListNodeType) == 0) &&
         (PyType_Ready(DLListIteratorType) == 0))
        ? 1 : 0;
}

void dllist_register(PyObject* module)
{
    Py_INCREF(DLListType);
    Py_INCREF(DLListNodeType);
    Py_INCREF(DLListIteratorType);

    PyModule_AddObject(module, "dllist", (PyObject*)DLListType);
    PyModule_AddObject(module, "dllistnode", (PyObject*)DLListNodeType);
    PyModule_AddObject(module, "dllistiterator", (PyObject*)DLListIteratorType);
}
