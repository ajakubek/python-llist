#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from llist import SLList
from llist import SLListNode


class testLList(unittest.TestCase):
    
    def setUp(self):
        self.l = SLList()
        for i in range(0,1100):
            node = SLListNode()
            node.value = 4 * i
	    self.l.append(node)

    def testSll_append(self):
        node = SLListNode()
        node.value = 4
        self.assertTrue(self.l.append(node))

    def testSll_append_left(self):
        node = SLListNode()
        node.value = 5
        self.assertTrue(self.l.appendleft(node))

	
    def testSll_pop(self):
        self.assertTrue(self.l.pop())

    def testSll_popright(self):
        self.assertTrue(self.l.popright())


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testLList))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())


