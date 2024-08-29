#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque
from llist import sllist, dllist
import time
# import gc
# gc.set_debug(gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_STATS)

num = 10000


class Stopwatch(object):
    def __init__(self):
        self.elapsed = 0.0
        self._start_time = None

    def __enter__(self):
        self._start_time = time.time()

    def __exit__(self, *exc_details):
        stop_time = time.time()
        assert(self._start_time is not None)
        self.elapsed += stop_time - self._start_time


def append(stopwatch, c):
    for i in range(num):
        with stopwatch:
            c.append(i)


def appendleft(stopwatch, c):
    for i in range(num):
        with stopwatch:
            c.appendleft(i)


def pop(stopwatch, c):
    for i in range(num):
        with stopwatch:
            c.pop()


def popleft(stopwatch, c):
    if isinstance(c, deque):
        for i in range(num):
            with stopwatch:
                c.popleft()
    else:
        for i in range(num):
            with stopwatch:
                c.pop()


def remove(stopwatch, c):
    if isinstance(c, deque):
        for i in range(0, num, 2):
            with stopwatch:
                c.remove(i)
    else:
        nodes = list(c.iternodes())
        for i in range(0, num, 2):
            with stopwatch:
                c.remove(nodes[i])


def index_iter(stopwatch, c):
    for i in range(len(c)):
        with stopwatch:
            c[i]


for container in [deque, dllist, sllist]:
    for operation in [append, appendleft, pop, popleft, remove, index_iter]:
        stopwatch = Stopwatch()
        c = container(range(num))
        operation(stopwatch, c)
        print("Completed %s/%s in \t\t%.8f seconds:\t %.1f ops/sec" % (
            container.__name__,
            operation.__name__,
            stopwatch.elapsed,
            num / stopwatch.elapsed))
