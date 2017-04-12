#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque
from cllist import sllist, dllist
import time
# import gc
# gc.set_debug(gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_STATS)

num = 10000


def append(c):
    for i in range(num):
        c.append(i)


def appendleft(c):
    for i in range(num):
        c.appendleft(i)


def pop(c):
    for i in range(num):
        c.pop()


def popleft(c):
    for i in range(num):
        c.popleft()


def remove(c):
    for i in range(0, num, 2):
        try:
            c.remove(num)
        except:
            pass


for container in [deque, dllist, sllist]:
    for operation in [append, appendleft, pop, popleft, remove]:
        c = container(range(num))
        start = time.time()
        operation(c)
        elapsed = time.time() - start

        col1 = "Completed %s/%s in" %(container.__name__, operation.__name__)
        col2 = "%.8f seconds:    %.1f" %(elapsed, num / elapsed )
        print ( "%s%s    %s%s ops/s" %(col1, (35 - len(col1)) * ' ', col2, (36 - len(col2)) * ' ') )
