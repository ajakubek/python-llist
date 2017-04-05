#!/usr/bin/env python

import os
import gc
import time
import random

from llist import dllist, sllist

LIST_SIZE = 600

NUM_POPS = 400

NUM_ITERS = 200

def doPops(lst, popIdxs):

    for popIdx in popIdxs:
        lst.pop(popIdx)

def doTime(func):
    t1 = time.time()
    func()
    t2 = time.time()

    return t2 - t1

if __name__ == '__main__':


    if 'LIST_SIZE' in os.environ:
        LIST_SIZE = int(os.environ['LIST_SIZE'])
    if 'NUM_POPS' in os.environ:
        NUM_POPS = int(os.environ['NUM_POPS'])
    if 'NUM_ITERS' in os.environ:
        NUM_POPS = int(os.environ['NUM_ITERS'])

    primeList = list(range(LIST_SIZE))

    # Generate a list of random indexes to pop.
    #   We avoid key errors by making sure we don't have a possible
    #     maximum larger than the smallest our list will become

    randomPops = []
    for i in range(NUM_POPS):
        nextNum = random.randint(0, LIST_SIZE - i - 1) # Cheaply make sure we don't get key errors

        randomPops.append(nextNum)

    headerLine =  "Starting:    LIST_SIZE=%d    NUM_POPS=%d    NUM_ITERS=%d"  %(LIST_SIZE, NUM_POPS, NUM_ITERS,)

    print ( "%s\n%s\n\n" %(headerLine, '-' * len(headerLine) ) )

    listTime = 0
    sllistTime = 0
    dllistTime = 0

    gc.collect()
    for i in range(NUM_ITERS):
        lst1 = primeList[:]
        listTime += doTime ( lambda : doPops(lst1, randomPops) )
        gc.collect()

    for i in range(NUM_ITERS):
        slst = sllist(primeList[:])
        sllistTime += doTime ( lambda : doPops(slst, randomPops) )
        gc.collect()

    for i in range(NUM_ITERS):
        dlst = dllist(primeList[:])
        dllistTime += doTime ( lambda : doPops(dlst, randomPops) )
        gc.collect()

 #   csllistTime = doTime ( lambda : doPops(cslst, randomPops) )
    csllistTime = 0.0

    print ( "List time:\t\t%f\t=  %f\nSL time:\t\t%f\t=  %f\nDL time:\t\t%f\t=  %f\n" %(listTime, listTime / NUM_ITERS, sllistTime, sllistTime / NUM_ITERS, dllistTime, dllistTime / NUM_ITERS) )
