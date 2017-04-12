#!/usr/bin/env python

import os
import gc
import time
import random

from cllist import dllist, sllist

LIST_SIZE = 700

NUM_SLICES = 500

NUM_ITERS = 200

def doSlice(lst, slices):
    for thisSlice in slices:
        try:
            x = lst[thisSlice[0] : thisSlice[1]]
        except TypeError as e:
            import pdb; pdb.set_trace()

def doTime(func):
    t1 = time.time()
    func()
    t2 = time.time()

    return t2 - t1

if __name__ == '__main__':


    if 'LIST_SIZE' in os.environ:
        LIST_SIZE = int(os.environ['LIST_SIZE'])
    if 'NUM_SLICES' in os.environ:
        NUM_SLICES = int(os.environ['NUM_SLICES'])
    if 'NUM_ITERS' in os.environ:
        NUM_SLICES = int(os.environ['NUM_ITERS'])

    primeList = list(range(LIST_SIZE))

    # Generate a list of random indexes to pop.
    #   We avoid key errors by making sure we don't have a possible
    #     maximum larger than the smallest our list will become

    randomSlices = []
    for j in range(NUM_ITERS):
        theseSlices = []
        for i in range(NUM_SLICES):
            num1 = random.randint(0, LIST_SIZE - 1) 
            num2 = random.randint(0, LIST_SIZE - 1)
            if num1 > num2:
                thisSlice = (num2, num1)
            else:
                thisSlice = (num1, num2)

            theseSlices.append( thisSlice )
        randomSlices.append(theseSlices)

    headerLine =  "Starting:    LIST_SIZE=%d    NUM_SLICES=%d    NUM_ITERS=%d"  %(LIST_SIZE, NUM_SLICES, NUM_ITERS,)

    print ( "%s\n%s\n\n" %(headerLine, '-' * len(headerLine) ) )

    listTime = 0
    sllistTime = 0
    dllistTime = 0

    gc.collect()
    for i in range(NUM_ITERS):
        lst1 = primeList[:]
        listTime += doTime ( lambda : doSlice(lst1, randomSlices[i]) )
        gc.collect()

    gc.collect()
    for i in range(NUM_ITERS):
        dlst = dllist(primeList[:])
        dllistTime += doTime ( lambda : doSlice(dlst, randomSlices[i]) )
        gc.collect()


    for i in range(NUM_ITERS):
        slst = sllist(primeList[:])
        sllistTime += doTime ( lambda : doSlice(slst, randomSlices[i]) )
        gc.collect()


 #   csllistTime = doTime ( lambda : doPops(cslst, randomPops) )
    csllistTime = 0.0

    print ( "List time:\t\t%f\t=  %f\nSL time:\t\t%f\t=  %f\nDL time:\t\t%f\t=  %f\n" %(listTime, listTime / NUM_ITERS, sllistTime, sllistTime / NUM_ITERS, dllistTime, dllistTime / NUM_ITERS) )
