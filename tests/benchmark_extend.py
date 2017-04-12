#!/usr/bin/env python

import os
import gc
import time
import random

from cllist import dllist, sllist

LIST1_SIZE = 600

LIST2_SIZE = 400

NUM_ITERS = 200

def doExtend(lst, otherList):
    
    return lst + otherList

def doIExtend(lst, otherList):

    lst += otherList
    return lst

def doExtendLeft(lst, otherList):
    
    lst.extendleft(otherList)
    return lst

def doTime(func):
    t1 = time.time()
    func()
    t2 = time.time()

    return t2 - t1

if __name__ == '__main__':


    if 'LIST1_SIZE' in os.environ:
        LIST1_SIZE = int(os.environ['LIST1_SIZE'])
    if 'LIST2_SIZE' in os.environ:
        LIST2_SIZE = int(os.environ['LIST2_SIZE'])
    if 'NUM_ITERS' in os.environ:
        LIST2_SIZE = int(os.environ['NUM_ITERS'])

    primeList = list(range(LIST1_SIZE))

    # Generate a list of random indexes to pop.
    #   We avoid key errors by making sure we don't have a possible
    #     maximum larger than the smallest our list will become

    primeList2 = list(range(LIST2_SIZE))

    headerLine =  "Starting:    LIST1_SIZE=%d    LIST2_SIZE=%d    NUM_ITERS=%d"  %(LIST1_SIZE, LIST2_SIZE, NUM_ITERS,)

    print ( "%s\n%s\n\n" %(headerLine, '-' * len(headerLine) ) )

    listTime = 0
    sllistTime = 0
    dllistTime = 0
    bllistTime = 0
    b2llistTime = 0

    listITime = 0
    sllistITime = 0
    dllistITime = 0
    bllistITime = 0
    b2llistITime = 0

    leftbllistTime = 0
    leftb2llistTime = 0

    lst1 = primeList[:]
    lst2 = primeList2[:]
    gc.collect()
    for i in range(NUM_ITERS):
        listTime += doTime ( lambda : doExtend(lst1, lst2) )
        gc.collect()

    for i in range(NUM_ITERS):
        lst1 = primeList[:]
        lst2 = primeList2[:]
        gc.collect()
        listITime += doTime ( lambda : doIExtend(lst1, lst2) )
        gc.collect()

    slst1 = sllist(primeList[:])
    slst2 = sllist(primeList2[:])
    gc.collect()
    for i in range(NUM_ITERS):
        sllistTime += doTime ( lambda : doExtend(slst1, slst2) )
        gc.collect()

    for i in range(NUM_ITERS):
        slst1 = sllist(primeList[:])
        slst2 = sllist(primeList2[:])
        gc.collect()
        sllistITime += doTime ( lambda : doIExtend(slst1, slst2) )
        gc.collect()


    dlst1 = dllist(primeList[:])
    dlst2 = dllist(primeList2[:])
    gc.collect()
    for i in range(NUM_ITERS):
        dllistTime += doTime ( lambda : doExtend(dlst1, dlst2) )
        gc.collect()

    for i in range(NUM_ITERS):
        dlst1 = dllist(primeList[:])
        dlst2 = dllist(primeList2[:])
        gc.collect()
        dllistITime += doTime ( lambda : doIExtend(dlst1, dlst2) )
        gc.collect()

    dlst1 = dllist(primeList[:])
    slst2 = sllist(primeList2[:])
    gc.collect()
    for i in range(NUM_ITERS):
        bllistTime += doTime ( lambda : doExtend(dlst1, slst2) )
        gc.collect()

    for i in range(NUM_ITERS):
        dlst1 = dllist(primeList[:])
        slst2 = sllist(primeList2[:])
        gc.collect()
        bllistITime += doTime ( lambda : doIExtend(dlst1, slst2) )
        gc.collect()

    slst1 = sllist(primeList[:])
    dlst2 = dllist(primeList2[:])
    gc.collect()
    for i in range(NUM_ITERS):
        b2llistTime += doTime ( lambda : doExtend(slst1, dlst2) )
        gc.collect()

    for i in range(NUM_ITERS):
        slst1 = sllist(primeList[:])
        dlst2 = dllist(primeList2[:])
        gc.collect()
        b2llistITime += doTime ( lambda : doIExtend(slst1, dlst2) )
        gc.collect()

    for i in range(NUM_ITERS):
        dlst1 = dllist(primeList[:])
        slst2 = sllist(primeList2[:])
        gc.collect()
        leftbllistTime += doTime ( lambda : doExtendLeft(dlst1, slst2) )
        gc.collect()

    for i in range(NUM_ITERS):
        slst1 = sllist(primeList[:])
        dlst2 = dllist(primeList2[:])
        gc.collect()
        leftb2llistTime += doTime ( lambda : doExtendLeft(slst1, dlst2) )
        gc.collect()

    print ( "List time:\t\t%f\t=  %f\nSL time:\t\t%f\t=  %f\nDL time:\t\t%f\t=  %f\nBL time:\t\t%f\t=  %f\nBL2 time:\t\t%f\t=  %f\n" %(listTime, listTime / NUM_ITERS, sllistTime, sllistTime / NUM_ITERS, dllistTime, dllistTime / NUM_ITERS, bllistTime, bllistTime / NUM_ITERS, b2llistTime, b2llistTime / NUM_ITERS) )
    print ( "List itime:\t\t%f\t=  %f\nSL itime:\t\t%f\t=  %f\nDL itime:\t\t%f\t=  %f\nBL time:\t\t%f\t=  %f\nBL2 time:\t\t%f\t=  %f\n" %(listITime, listITime / NUM_ITERS, sllistITime, sllistITime / NUM_ITERS, dllistITime, dllistITime / NUM_ITERS, bllistITime, bllistITime / NUM_ITERS, b2llistITime, b2llistITime / NUM_ITERS) )

    print ( "leftB time:\t\t%f\t=  %f\nleftB2 time:\t\t%f\t=  %f\n" %(leftbllistTime, leftbllistTime / NUM_ITERS, leftb2llistTime, leftb2llistTime / NUM_ITERS) )
