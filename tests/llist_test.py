#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gc
import unittest
from llist import SLList
from llist import SLListNode
from llist import DLList
from llist import DLListNode

gc.set_debug(gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_STATS)


class testLList(unittest.TestCase):

    def testSll_append_left(self):
        ll = SLList([1, 2, 3, 4])
        ll.appendleft(5)
        self.assertTrue([5, 1, 2, 3, 4], list(ll))

    def testSll_append_right(self):
        ll = SLList([1, 2, 3, 4])
        ll.appendleft(5)
        self.assertTrue([1, 2, 3, 4, 5], list(ll))

    def testSll_pop_left_from_one_elem(self):
        ll = SLList(xrange(0, 100))
        dd = ll.popleft()
        self.assertEqual(dd, 0)

    def testSll_pop_right_from_one_elem(self):
        ll = SLList(xrange(0, 100))
        dd = ll.popright()
        self.assertEqual(dd, 99)

    def testSll_pop_right_from_n_elem(self):
        ll = SLList(xrange(0, 100))
        dd = ll.popright()
        self.assertEqual(dd, 99)

    def testSll_get_node_at_from_n_elem(self):
        ll = SLList(xrange(0, 100))
        self.assertEqual(50, ll[50]())

    def testSll_remove_from_n_elem(self):
        ll = SLList()
        nn = SLListNode()
        ll.append(nn)
        to_del = ll[0]
        ll.remove(to_del)
        self.assertEqual(None, None)

    def testSll_inser_after(self):
        ll = SLList([1, 3, '123'])
        ll.insert_after(100, ll.first)
        self.assertEqual([1, 100, 3, '123'], list(ll))

    def testSll_inser_before(self):
        ll = SLList([1, 3, '123'])
        ll.insert_before(100, ll.first)
        self.assertEqual([100, 1, 3, '123'], list(ll))

    def testDll_append_left(self):
        ll = DLList([1, 2, 3, 4])
        ll.appendleft(5)
        self.assertTrue([5, 1, 2, 3, 4], list(ll))

    def testDll_append_right(self):
        ll = DLList([1, 2, 3, 4])
        ll.appendleft(5)
        self.assertTrue([1, 2, 3, 4, 5], list(ll))

    def testDll_pop_left_from_one_elem(self):
        ll = DLList(xrange(0, 100))
        dd = ll.popleft()
        self.assertEqual(dd.value, 0)

    def testDll_pop_right_from_one_elem(self):
        ll = DLList(xrange(0, 100))
        dd = ll.popright()
        self.assertEqual(dd.value, 99)

    def testDll_pop_right_from_n_elem(self):
        ll = DLList(xrange(0, 100))
        dd = ll.popright()
        self.assertEqual(dd(), 99)

    def testDll_get_node_at_from_n_elem(self):
        ll = DLList(xrange(0, 100))
        self.assertEqual(50, ll[50]())

    def testDll_remove_from_n_elem(self):
        ll = DLList()
        nn = DLListNode()
        ll.append(nn)
        to_del = ll[0]
        ll.remove(to_del)
        self.assertEqual(None, None)

    def testDll_insert(self):
        ll = DLList([1, 3, '123'])
        ll.insert(100)
        self.assertEqual([1, 3, '123', 100], list(ll))

    def testDll_inser_before(self):
        ll = DLList([1, 3, '123'])
        ll.insert(100, ll.first)
        self.assertEqual([100, 1, 3, '123'], list(ll))

    def always_success(self):
        self.assertEqual(0, 0)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testLList))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
