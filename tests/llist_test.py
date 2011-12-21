#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from llist import SLList
from llist import SLListNode


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
        self.assertEqual(dd.value, 0)

    def testSll_pop_right_from_one_elem(self):
        ll = SLList(xrange(0, 100))
        dd = ll.popright()
        self.assertEqual(dd.value, 99)

    def testSll_pop_right_from_n_elem(self):
        ll = SLList(xrange(0, 100))
        dd = ll.popright()
        self.assertEqual(dd(), 99)

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


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testLList))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
