/*
 * Copyright (c) 2017 Timothy Savannah, 
 * all rights reserved under terms of MIT license (see LICENSE)
 */

#ifndef LLIST_H
#define LLIST_H

#include <Python.h>


#define LLIST_VERSION_MAJOR 1
#define LLIST_VERSION_MINOR 0
#define LLIST_VERSION_PATCH 0
#define LLIST_VERSION_STR   ("1.0.0")

extern PyObject *mod_version;
extern PyObject *mod_version_tuple;


#ifdef __GNUC__

#define likely(x)   __builtin_expect(!!(x), 1)
#define unlikely(x) __builtin_expect(!!(x), 0)

#else

#define likely(x)   (x)
#define unlikely(x) (x)

#endif

/* #define DO_DEBUG */


#ifdef DO_DEBUG
static void debugmsg(char *format, ...)
{
    va_list args;
    FILE *f;

    f = fopen("debug.txt", "a");

    va_start(args, format);
    vfprintf(f, format, args);
    va_end(args);

    fclose(f);
}
#else

#define debugmsg(...)
/*static inline void debugmsg(char *format, ...)
{

}
*/
#endif

#if PY_MAJOR_VERSION >= 3

#define GET_INDICES_TYPE PyObject

#else

#define GET_INDICES_TYPE PySliceObject

#endif

static inline Py_ssize_t py_ssize_t_abs(Py_ssize_t x)
{
    return (x >= 0) ? x : -x;
}

static inline Py_ssize_t py_ssize_min(Py_ssize_t a, Py_ssize_t b)
{
    if ( a < b )
        return a;
    return b;
}


/* Calc difference between given end and actual end with step */
#define calc_end_difference_step(_start, _end, _step) (((_end - _start - 1) % _step) + 1)


static inline int _normalize_indexes(Py_ssize_t size, Py_ssize_t *idx_start, Py_ssize_t *idx_end)
{

    if ( unlikely(*idx_start < 0 ))
    {
        *idx_start = size - *idx_start;
        if ( unlikely(*idx_start < 0 ))
            return 0;
    }
    if ( unlikely(*idx_end < 0 ))
    {
        *idx_end = size - *idx_end;
        if ( unlikely(*idx_end < 0 ))
            return 0;
    }

    if ( unlikely(*idx_end >= size ))
        *idx_end = size;

    if ( unlikely(*idx_start >= size || *idx_start >= *idx_end))
        return 0;

    if ( unlikely(*idx_start >= *idx_end ))
        return 0;


    return 1;
}



#endif
