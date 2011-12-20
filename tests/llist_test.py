#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from llist import SLList
from llist import SLListNode
from llist import DLList
from llist import DLListNode


class testSLList(unittest.TestCase):

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
        ll.remove(nn)
        print ll.first
        self.assertEqual(None, None)


class testDLList(unittest.TestCase):

    def setUp(self):
        self.v = [4 * x for x in xrange(1100)]
        self.l = DLList()
        for x in self.v:
            node = DLListNode(x)
            self.l.append(node)

    def testDll_init_with_sequence(self):
        l = DLList(xrange(0,1100))
        self.assertEqual(len(l), 1100)

    def testDll_init_with_non_sequence(self):
        self.assertRaises(TypeError, DLList, None);
        self.assertRaises(TypeError, DLList, 1);

    def testDll_str(self):
        a = DLList([])
        self.assertEqual(str(a), 'DLList()')
        b = DLList([None, 1, 'abc'])
        self.assertEqual(str(b), 'DLList([None, 1, abc])')

    def testDll_repr(self):
        a = DLList([])
        self.assertEqual(repr(a), 'DLList()')
        b = DLList([None, 1, 'abc'])
        self.assertEqual(repr(b), 'DLList([None, 1, \'abc\'])')

    def testDll_node_str(self):
        a = DLList([None, None]).first
        self.assertEqual(str(a), 'DLListNode(None)')
        b = DLList([1, None]).first
        self.assertEqual(str(b), 'DLListNode(1)')
        c = DLList(['abc', None]).first
        self.assertEqual(str(c), 'DLListNode(abc)')
        pass

    def testDll_node_repr(self):
        a = DLList([None]).first
        self.assertEqual(repr(a), '<DLListNode(None)>')
        b = DLList([1, None]).first
        self.assertEqual(repr(b), '<DLListNode(1)>')
        c = DLList(['abc', None]).first
        self.assertEqual(repr(c), '<DLListNode(\'abc\')>')
        pass

    def testDll_cmp(self):
        a = DLList(xrange(0, 1100))
        b = DLList(xrange(0, 1101))
        c = [xrange(0, 1100)]
        self.assertEqual(cmp(a, a), 0)
        self.assertEqual(cmp(a, b), -1)
        self.assertEqual(cmp(b, a), 1)
        self.assertEqual(cmp(a, c), 1)
        self.assertEqual(cmp(c, a), -1)
        self.assertEqual(cmp([], []), 0)
        self.assertEqual(cmp([], a), -1)
        self.assertEqual(cmp(a, []), 1)

    def testDll_iter(self):
        correct_sum = sum(range(0, 1100)) * 4
        list_sum = 0
        for val in self.l:
            list_sum += val
        self.assertEqual(correct_sum, list_sum);

    def testDll_insert(self):
        a = DLList(xrange(4))
        b = DLList([0, 1, 2, 3, 10])
        a.insert(10)
        self.assertEqual(a, b)

    def testDll_insert_ref_node(self):
        a = DLList(xrange(4))
        b = DLList([0, 1, 10, 2, 3])
        n = a[2]
        a.insert(10, n)
        self.assertEqual(a, b)

    def testDll_insert_invalid_ref(self):
        self.assertRaises(TypeError, self.l.insert, 10, 1)
        self.assertRaises(TypeError, self.l.insert, 10, 'abc')
        self.assertRaises(TypeError, self.l.insert, 10, [])

    def testDll_append(self):
        node = DLListNode()
        node.value = 4
        self.assertTrue(self.l.append(node))

    def testDll_appendleft(self):
        node = DLListNode()
        node.value = 5
        self.assertTrue(self.l.appendleft(node))

    def testDll_popright(self):
        orig_len = len(self.l)
        orig_last = self.l.last()
        self.l.popright()
        self.assertEqual(len(self.l), orig_len - 1)
        self.assertEqual(self.l.last(), orig_last - 4)

    def testDll_popleft(self):
        orig_len = len(self.l)
        orig_first = self.l.first()
        self.l.popleft()
        self.assertEqual(len(self.l), orig_len - 1)
        self.assertEqual(self.l.first(), orig_first + 4)

    def testDll_del(self):
        del self.l[0]
        del self.v[0]
        self.assertEqual(list(self.l), self.v)
        del self.l[len(self.l) - 1]
        del self.v[len(self.v) - 1]
        self.assertEqual(list(self.l), self.v)
        del self.l[(len(self.l) - 1) / 2]
        del self.v[(len(self.v) - 1) / 2]
        self.assertEqual(list(self.l), self.v)

        def del_item(idx):
            del self.l[idx]
        self.assertRaises(IndexError, del_item, len(self.l))

        for i in xrange(len(self.l)):
            del self.l[0]
        self.assertEqual(len(self.l), 0)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testSLList))
    suite.addTest(unittest.makeSuite(testDLList))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
