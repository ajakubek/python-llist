#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from llist import SLList
from llist import SLListNode


class testLList(unittest.TestCase):

    def testSll_append(self):
        ll = SLList()
        node = SLListNode()
        ll.append(node)
        ll.pop()
        self.assertTrue(1)

    def testSll_append_left(self):
        ll = SLList()
        node = SLListNode()
        node.value = 12
        ll.appendleft(node)
        self.assertTrue(1)

    # def testSll_pop(self):
    #     ll = SLList()
    #     node = SLListNode()
    #     node.value = 234
    #     ll.append(node)
    #     ll.append(node)
    #     ll.popleft()
    #     self.assertTrue()

    def testSll_pop_left_from_empty(self):
        ll = SLList()
        try:
            ll.popleft()
            self.assertEqual(1, 0)
        except RuntimeError:
            self.assertEqual(0, 0)

    def testSll_pop_right_from_empty(self):
        ll = SLList()
        try:
            ll.popright()
            self.assertEqual(1, 0)
        except RuntimeError:
            self.assertEqual(0, 0)

    def testSll_pop_left_from_one_elem(self):
        ll = SLList()
        nn = SLListNode()
        nn.value = 3
        ll.append(nn)
        dd = ll.popleft()
        self.assertEqual(dd.__class__, nn.__class__)

    def testSll_pop_right_from_one_elem(self):
        ll = SLList()
        nn = SLListNode()
        nn.value = 3
        ll.append(nn)
        dd = ll.popright()
        self.assertEqual(dd.__class__, nn.__class__)

    def testSll_pop_right_from_one_elem_and_later_from_empty(self):
        ll = SLList()
        nn = SLListNode()
        nn.value = 3
        ll.append(nn)
        dd = ll.popright()
        try:
            ll.popright()
            self.assertEqual(1, 0)
        except RuntimeError:
            self.assertEqual(0, 0)
        self.assertEqual(dd.__class__, nn.__class__)

    def testSll_pop_right_from_n_elem(self):
        ll = SLList()
        nn = SLListNode()
        nn.value = 3
        ll.append(nn)
        dd = ll.popright()
        self.assertEqual(dd.__class__, nn.__class__)

    # def testSll_get_node_at_from_n_elem(self):
    #     ll = SLList()
    #     for i in range(0, 2):
    #         nn = SLListNode()
    #         nn.value = 3 * i
    #         ll.append(nn)
    #     self.assertEqual(0, 0)

    def testSll_remove_from_n_elem(self):
        ll = SLList()
        nn = SLListNode()
        ll.append(nn)
        to_del = ll[0]
        ll.remove(to_del)
        self.assertEqual(None, None)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testLList))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
