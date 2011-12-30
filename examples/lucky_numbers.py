"""
This example compares performance of llist.dllist and collections.deque
datatypes.
It calculates a sequence of N lucky numbers
(see http://en.wikipedia.org/wiki/Lucky_number for definition).
The dominating operation for this problem is typically removal of elements
from container, which is much faster with linked lists.
"""

from collections import deque
from llist import dllist
import sys
import time

N = 128 * 1024


def generate_lucky_deque(max_num):
    lucky_numbers = deque(xrange(1, max_num + 1, 2))

    multiple_node = lucky_numbers[1]
    multiple_pos = 2

    while multiple_node != None:
        removed_multiple = multiple_node
        if removed_multiple >= len(lucky_numbers):
            break

        removed_pos = removed_multiple - 1
        while removed_pos < len(lucky_numbers):
            del lucky_numbers[removed_pos]
            removed_pos += removed_multiple - 1

        multiple_node = lucky_numbers[multiple_pos]
        multiple_pos += 1

    return lucky_numbers


def generate_lucky_list(max_num):
    lucky_numbers = dllist(xrange(1, max_num + 1, 2))

    multiple_node = lucky_numbers.nodeat(1)

    while multiple_node != None:
        removed_multiple = multiple_node()
        if removed_multiple >= len(lucky_numbers):
            break

        removed_pos = removed_multiple - 1
        while removed_pos < len(lucky_numbers):
            del lucky_numbers[removed_pos]
            removed_pos += removed_multiple - 1

        multiple_node = multiple_node.next

    return lucky_numbers


def time_execution(bench_func):
    start_time = time.clock()
    result = bench_func()
    elapsed = time.clock() - start_time
    return (result, elapsed)


if __name__ == '__main__':
    print 'Calculating lucky numbers using deque...',
    sys.stdout.flush()
    result_deque, time_deque = time_execution(lambda: generate_lucky_deque(N))
    print '%gs' % time_deque

    print 'Calculating lucky numbers using dllist...',
    sys.stdout.flush()
    result_list, time_list = time_execution(lambda: generate_lucky_list(N))
    print '%gs' % time_list

    if list(result_deque) == list(result_list):
        print 'Both results are equal.'
    else:
        print 'Results differ, you might have found a bug!'
