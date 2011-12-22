#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gc
import unittest
from llist import SLList
from llist import SLListNode
from llist import DLList
from llist import DLListNode

gc.set_debug(gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_STATS)

class testSLList(unittest.TestCase):

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

    def always_success(self):
        self.assertEqual(0, 0)


class testDLList(unittest.TestCase):

    def test_init_empty(self):
        ll = DLList()
        self.assertEqual(len(ll), 0)
        self.assertEqual(ll.size, 0)
        self.assertEqual(list(ll), [])

    def test_init_with_sequence(self):
        ref = range(0, 1024, 4)
        ll = DLList(ref)
        self.assertEqual(len(ll), len(ref))
        self.assertEqual(ll.size, len(ref))
        self.assertEqual(list(ll), ref)

    def test_init_with_non_sequence(self):
        self.assertRaises(TypeError, DLList, None);
        self.assertRaises(TypeError, DLList, 1);

    def test_str(self):
        a = DLList([])
        self.assertEqual(str(a), 'DLList()')
        b = DLList([None, 1, 'abc'])
        self.assertEqual(str(b), 'DLList([None, 1, abc])')

    def test_repr(self):
        a = DLList([])
        self.assertEqual(repr(a), 'DLList()')
        b = DLList([None, 1, 'abc'])
        self.assertEqual(repr(b), 'DLList([None, 1, \'abc\'])')

    def test_node_str(self):
        a = DLList([None, None]).first
        self.assertEqual(str(a), 'DLListNode(None)')
        b = DLList([1, None]).first
        self.assertEqual(str(b), 'DLListNode(1)')
        c = DLList(['abc', None]).first
        self.assertEqual(str(c), 'DLListNode(abc)')
        pass

    def test_node_repr(self):
        a = DLList([None]).first
        self.assertEqual(repr(a), '<DLListNode(None)>')
        b = DLList([1, None]).first
        self.assertEqual(repr(b), '<DLListNode(1)>')
        c = DLList(['abc', None]).first
        self.assertEqual(repr(c), '<DLListNode(\'abc\')>')
        pass

    def test_cmp(self):
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

    def test_iter(self):
        ref = range(0, 1024, 4)
        ll = DLList(ref)
        idx = 0
        for val in ll:
            self.assertEqual(val, ref[idx])
            idx += 1
        self.assertEqual(idx, len(ref))

    def test_insert_value(self):
        ll = DLList(xrange(4))
        ref = DLList([0, 1, 2, 3, 10])
        arg_node = DLListNode(10)
        new_node = ll.insert(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.prev, ll[-2])
        self.assertEqual(new_node.next, None)
        self.assertEqual(ll[-2].next, new_node)
        self.assertEqual(new_node, ll.last)
        self.assertEqual(ll, ref)

    def test_insert_value_before(self):
        ll = DLList(xrange(4))
        ref = DLList([0, 1, 10, 2, 3])
        arg_node = DLListNode(10)
        new_node = ll.insert(arg_node, ll[2])
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.prev, ll[1])
        self.assertEqual(new_node.next, ll[3])
        self.assertEqual(ll[1].next, new_node)
        self.assertEqual(ll[3].prev, new_node)
        self.assertEqual(ll, ref)

    def test_insert_invalid_ref(self):
        ll = DLList()
        self.assertRaises(TypeError, ll.insert, 10, 1)
        self.assertRaises(TypeError, ll.insert, 10, 'abc')
        self.assertRaises(TypeError, ll.insert, 10, [])

    def test_append(self):
        ll = DLList(xrange(4))
        ref = DLList([0, 1, 2, 3, 10])
        arg_node = DLListNode(10)
        new_node = ll.append(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10);
        self.assertEqual(new_node.prev, ll[-2])
        self.assertEqual(new_node.next, None)
        self.assertEqual(ll[-2].next, new_node)
        self.assertEqual(ll.last, new_node)
        self.assertEqual(ll, ref)

    def test_appendleft(self):
        ll = DLList(xrange(4))
        ref = DLList([10, 0, 1, 2, 3])
        arg_node = DLListNode(10)
        new_node = ll.appendleft(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10);
        self.assertEqual(new_node.prev, None)
        self.assertEqual(new_node.next, ll[1])
        self.assertEqual(ll[1].prev, new_node)
        self.assertEqual(ll.first, new_node)
        self.assertEqual(ll, ref)

    def test_appendright(self):
        ll = DLList(xrange(4))
        ref = DLList([0, 1, 2, 3, 10])
        arg_node = DLListNode(10)
        new_node = ll.appendright(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10);
        self.assertEqual(new_node.prev, ll[-2])
        self.assertEqual(new_node.next, None)
        self.assertEqual(ll[-2].next, new_node)
        self.assertEqual(ll.last, new_node)
        self.assertEqual(ll, ref)

    def test_pop(self):
        ref = range(0, 1024, 4)
        ll = DLList(ref)
        result = ll.pop();
        self.assertEqual(result, ref[-1])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.last.value, ref[-2])
        self.assertEqual(list(ll), ref[:-1])

    def test_popleft(self):
        ref = range(0, 1024, 4)
        ll = DLList(ref)
        result = ll.popleft()
        self.assertEqual(result, ref[0])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.first.value, ref[1])
        self.assertEqual(list(ll), ref[1:])

    def test_popright(self):
        ref = range(0, 1024, 4)
        ll = DLList(ref)
        result = ll.popright()
        self.assertEqual(result, ref[-1])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.last.value, ref[-2])
        self.assertEqual(list(ll), ref[:-1])

    def test_del(self):
        ref = range(0, 1024, 4)
        ll = DLList(ref)
        del ll[0]
        del ref[0]
        self.assertEqual(list(ll), ref)
        del ll[len(ll) - 1]
        del ref[len(ref) - 1]
        self.assertEqual(list(ll), ref)
        del ll[(len(ll) - 1) / 2]
        del ref[(len(ref) - 1) / 2]
        self.assertEqual(list(ll), ref)

        def del_item(idx):
            del ll[idx]
        self.assertRaises(IndexError, del_item, len(ll))

        for i in xrange(len(ll)):
            del ll[0]
        self.assertEqual(len(ll), 0)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testSLList))
    suite.addTest(unittest.makeSuite(testDLList))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
