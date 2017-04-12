#!/usr/bin/env python

import os
import gc
import time
import random

from cllist import dllist, sllist

LIST_SIZE = 700

NUM_CONTAINS = 1500

NUM_ITERS = 200

def doContains(lst, containsItems):

    for containsItem in containsItems:
        return containsItem in lst

def doTime(func):
    t1 = time.time()
    func()
    t2 = time.time()

    return t2 - t1

if __name__ == '__main__':


    if 'LIST_SIZE' in os.environ:
        LIST_SIZE = int(os.environ['LIST_SIZE'])
    if 'NUM_CONTAINS' in os.environ:
        NUM_CONTAINS = int(os.environ['NUM_CONTAINS'])
    if 'NUM_ITERS' in os.environ:
        NUM_CONTAINS = int(os.environ['NUM_ITERS'])

    primeList = list(range(LIST_SIZE))

    # Generate a list of random indexes to pop.
    #   We avoid key errors by making sure we don't have a possible
    #     maximum larger than the smallest our list will become

    randomItems = []
    for j in range(NUM_ITERS):
        theseItems = []
        for i in range(NUM_CONTAINS):
            nextNum = random.randint(0, LIST_SIZE - 1) # Cheaply make sure we don't get key errors

            theseItems.append( primeList[nextNum] )
        randomItems.append(theseItems)

    headerLine =  "Starting:    LIST_SIZE=%d    NUM_CONTAINS=%d    NUM_ITERS=%d"  %(LIST_SIZE, NUM_CONTAINS, NUM_ITERS,)

    print ( "%s\n%s\n\n" %(headerLine, '-' * len(headerLine) ) )

    listTime = 0
    sllistTime = 0
    dllistTime = 0

    gc.collect()
    for i in range(NUM_ITERS):
        dlst = dllist(primeList[:])
        dllistTime += doTime ( lambda : doContains(dlst, randomItems[i]) )
        gc.collect()

    for i in range(NUM_ITERS):
        lst1 = primeList[:]
        listTime += doTime ( lambda : doContains(lst1, randomItems[i]) )
        gc.collect()

    for i in range(NUM_ITERS):
        slst = sllist(primeList[:])
        sllistTime += doTime ( lambda : doContains(slst, randomItems[i]) )
        gc.collect()


 #   csllistTime = doTime ( lambda : doPops(cslst, randomPops) )
    csllistTime = 0.0

    print ( "List time:\t\t%f\t=  %f\nSL time:\t\t%f\t=  %f\nDL time:\t\t%f\t=  %f\n" %(listTime, listTime / NUM_ITERS, sllistTime, sllistTime / NUM_ITERS, dllistTime, dllistTime / NUM_ITERS) )
