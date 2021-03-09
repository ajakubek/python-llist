#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gc
import sys
import unittest
import weakref
from llist import sllist
from llist import sllistnode
from llist import dllist
from llist import dllistnode

gc.set_debug(gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_STATS)


if sys.hexversion >= 0x03000000:
    # python 3 compatibility wrappers

    def py23_xrange(*args):
        return range(*args)

    def py23_range(*args):
        return list(range(*args))

    def cmp(a, b):
        if a == b:
            return 0
        elif a < b:
            return -1
        else:
            return 1

else:
    # python 2 compatibility wrappers

    def py23_xrange(*args):
        return xrange(*args)

    def py23_range(*args):
        return range(*args)



class testsllist(unittest.TestCase):

    def test_init_empty(self):
        ll = sllist()
        self.assertEqual(len(ll), 0)
        self.assertEqual(ll.size, 0)
        self.assertEqual(list(ll), [])

    def test_init_with_sequence(self):
        ref = py23_range(0, 1024, 4)
        ll = sllist(ref)
        self.assertEqual(len(ll), len(ref))
        self.assertEqual(ll.size, len(ref))
        self.assertEqual(list(ll), ref)

    def test_init_with_non_sequence(self):
        self.assertRaises(TypeError, sllist, 1)
        self.assertRaises(TypeError, sllist, 1.5)

    def test_str(self):
        a = sllist([])
        self.assertEqual(str(a), 'sllist()')
        b = sllist([None, 1, 'abc'])
        self.assertEqual(str(b), 'sllist([None, 1, abc])')

    def test_repr(self):
        a = sllist([])
        self.assertEqual(repr(a), 'sllist()')
        b = sllist([None, 1, 'abc'])
        self.assertEqual(repr(b), 'sllist([None, 1, \'abc\'])')

    def test_node_str(self):
        a = sllist([None, None]).first
        self.assertEqual(str(a), 'sllistnode(None)')
        b = sllist([1, None]).first
        self.assertEqual(str(b), 'sllistnode(1)')
        c = sllist(['abc', None]).first
        self.assertEqual(str(c), 'sllistnode(abc)')

    def test_node_repr(self):
        a = sllist([None]).first
        self.assertEqual(repr(a), '<sllistnode(None)>')
        b = sllist([1, None]).first
        self.assertEqual(repr(b), '<sllistnode(1)>')
        c = sllist(['abc', None]).first
        self.assertEqual(repr(c), '<sllistnode(\'abc\')>')

    def test_str_recursive_list(self):
        ll = sllist()
        ll.append(sllistnode(ll))
        self.assertEqual(str(ll), 'sllist([sllist(<...>)])')

    def test_str_recursive_node(self):
        ll = self.make_recursive_node_list()
        self.assertEqual(str(ll), 'sllist([sllistnode(sllistnode(<...>))])')

    def test_repr_recursive_list(self):
        ll = sllist()
        ll.append(sllistnode(ll))
        self.assertEqual(repr(ll), 'sllist([sllist(<...>)])')

    def test_repr_recursive_node_list(self):
        ll = self.make_recursive_node_list()
        self.assertEqual(repr(ll), 'sllist([<sllistnode(sllistnode(<...>))>])')

    def make_recursive_node_list(self):
        ll = sllist()
        node = sllistnode()
        node.value = node
        ll.append(node)
        return ll

    def test_cmp(self):
        a = sllist(py23_xrange(0, 1100))
        b = sllist(py23_xrange(0, 1101))
        c = sllist([1, 2, 3, 4])
        d = sllist([1, 2, 3, 5])
        e = sllist([1, 0, 0, 0])
        f = sllist([0, 0, 0, 0])
        self.assertEqual(cmp(a, a), 0)
        self.assertEqual(cmp(a, b), -1)
        self.assertEqual(cmp(b, a), 1)
        self.assertEqual(cmp(c, d), -1)
        self.assertEqual(cmp(d, c), 1)
        self.assertEqual(cmp(e, f), 1)
        self.assertEqual(cmp(f, e), -1)

    def test_cmp_nonlist(self):
        a = sllist(py23_xrange(0, 1100))
        b = [py23_xrange(0, 1100)]
        if sys.hexversion < 0x03000000:
            # actual order is not specified by language
            self.assertNotEqual(cmp(a, b), 0)
            self.assertNotEqual(cmp(b, a), 0)
            self.assertNotEqual(cmp([], a), 0)
            self.assertNotEqual(cmp(a, []), 0)

    def test_eq(self):
        a = sllist(py23_xrange(0, 1100))
        b = sllist(py23_xrange(0, 1101))
        c = sllist([1, 2, 3, 4])
        d = sllist([1, 2, 3, 5])
        e = sllist([1, 0, 0, 0])
        f = sllist([0, 0, 0, 0])
        self.assertTrue(sllist() == sllist())
        self.assertTrue(a == a)
        self.assertFalse(sllist() == a)
        self.assertFalse(a == sllist())
        self.assertFalse(a == b)
        self.assertFalse(b == a)
        self.assertFalse(c == d)
        self.assertFalse(d == c)
        self.assertFalse(e == f)
        self.assertFalse(f == e)

    def test_ne(self):
        a = sllist(py23_xrange(0, 1100))
        b = sllist(py23_xrange(0, 1101))
        c = sllist([1, 2, 3, 4])
        d = sllist([1, 2, 3, 5])
        e = sllist([1, 0, 0, 0])
        f = sllist([0, 0, 0, 0])
        self.assertFalse(sllist() != sllist())
        self.assertFalse(a != a)
        self.assertTrue(sllist() != a)
        self.assertTrue(a != sllist())
        self.assertTrue(a != b)
        self.assertTrue(b != a)
        self.assertTrue(c != d)
        self.assertTrue(d != c)
        self.assertTrue(e != f)
        self.assertTrue(f != e)

    def test_lt(self):
        a = sllist(py23_xrange(0, 1100))
        b = sllist(py23_xrange(0, 1101))
        c = sllist([1, 2, 3, 4])
        d = sllist([1, 2, 3, 5])
        e = sllist([1, 0, 0, 0])
        f = sllist([0, 0, 0, 0])
        self.assertFalse(sllist() < sllist())
        self.assertFalse(a < a)
        self.assertTrue(sllist() < a)
        self.assertFalse(a < sllist())
        self.assertTrue(a < b)
        self.assertFalse(b < a)
        self.assertTrue(c < d)
        self.assertFalse(d < c)
        self.assertFalse(e < f)
        self.assertTrue(f < e)

    def test_gt(self):
        a = sllist(py23_xrange(0, 1100))
        b = sllist(py23_xrange(0, 1101))
        c = sllist([1, 2, 3, 4])
        d = sllist([1, 2, 3, 5])
        e = sllist([1, 0, 0, 0])
        f = sllist([0, 0, 0, 0])
        self.assertFalse(sllist() > sllist())
        self.assertFalse(a > a)
        self.assertFalse(sllist() > a)
        self.assertTrue(a > sllist())
        self.assertFalse(a > b)
        self.assertTrue(b > a)
        self.assertFalse(c > d)
        self.assertTrue(d > c)
        self.assertTrue(e > f)
        self.assertFalse(f > e)

    def test_le(self):
        a = sllist(py23_xrange(0, 1100))
        b = sllist(py23_xrange(0, 1101))
        c = sllist([1, 2, 3, 4])
        d = sllist([1, 2, 3, 5])
        e = sllist([1, 0, 0, 0])
        f = sllist([0, 0, 0, 0])
        self.assertTrue(sllist() <= sllist())
        self.assertTrue(a <= a)
        self.assertTrue(sllist() <= a)
        self.assertFalse(a <= sllist())
        self.assertTrue(a <= b)
        self.assertFalse(b <= a)
        self.assertTrue(c <= d)
        self.assertFalse(d <= c)
        self.assertFalse(e <= f)
        self.assertTrue(f <= e)

    def test_ge(self):
        a = sllist(py23_xrange(0, 1100))
        b = sllist(py23_xrange(0, 1101))
        c = sllist([1, 2, 3, 4])
        d = sllist([1, 2, 3, 5])
        e = sllist([1, 0, 0, 0])
        f = sllist([0, 0, 0, 0])
        self.assertTrue(sllist() >= sllist())
        self.assertTrue(a >= a)
        self.assertFalse(sllist() >= a)
        self.assertTrue(a >= sllist())
        self.assertFalse(a >= b)
        self.assertTrue(b >= a)
        self.assertFalse(c >= d)
        self.assertTrue(d >= c)
        self.assertTrue(e >= f)
        self.assertFalse(f >= e)

    def test_nodeat(self):
        ref = py23_range(0, 1024, 4)
        ll = sllist(ref)
        for idx in py23_xrange(len(ll)):
            self.assertTrue(isinstance(ll.nodeat(idx), sllistnode))
            self.assertEqual(ll.nodeat(idx).value, ref[idx])
        for idx in py23_xrange(len(ll)):
            self.assertTrue(isinstance(ll.nodeat(idx), sllistnode))
            self.assertEqual(ll.nodeat(-idx - 1).value, ref[-idx - 1])
        self.assertRaises(TypeError, ll.nodeat, None)
        self.assertRaises(TypeError, ll.nodeat, 'abc')
        self.assertRaises(IndexError, ll.nodeat, len(ref))
        self.assertRaises(IndexError, ll.nodeat, -len(ref) - 1)

    def test_nodeat_empty(self):
        ll = sllist()
        self.assertRaises(TypeError, ll.nodeat, None)
        self.assertRaises(TypeError, ll.nodeat, 'abc')
        self.assertRaises(IndexError, ll.nodeat, 0)
        self.assertRaises(IndexError, ll.nodeat, -1)

    def test_iter(self):
        ref = py23_range(0, 1024, 4)
        ll = sllist(ref)
        idx = 0
        for val in ll:
            self.assertFalse(isinstance(val, sllistnode))
            self.assertEqual(val, ref[idx])
            idx += 1
        self.assertEqual(idx, len(ref))

    def test_iter_empty(self):
        ll = sllist()
        count = 0
        for val in ll:
            count += 1
        self.assertEqual(count, 0)

    def test_iter_of_appended_node(self):
        ll = sllist()
        ll.append('initial item')

        appended_item_visited = False

        for x in ll:
            if x == 'initial item':
                ll.append('new item')
            elif x == 'new item':
                appended_item_visited = True

        self.assertTrue(appended_item_visited)

    def test_iter_of_removed_node(self):
        ll = sllist(['x', 'removed item'])

        for x in ll:
            self.assertNotEqual(x, 'removed item')
            ll.remove(ll.last)

    def test_reversed(self):
        ref = py23_range(0, 1024, 4)
        ll = sllist(ref)
        idx = len(ref) - 1
        for val in reversed(ll):
            self.assertFalse(isinstance(val, sllistnode))
            self.assertEqual(val, ref[idx])
            idx -= 1
        self.assertEqual(idx, -1)

    def test_reversed_empty(self):
        ll = sllist()
        count = 0
        for val in reversed(ll):
            count += 1
        self.assertEqual(count, 0)

    def test_append_left(self):
        ll = sllist([1, 2, 3, 4])
        ll.appendleft(5)
        self.assertEqual([5, 1, 2, 3, 4], list(ll))

    def test_append_right(self):
        ll = sllist([1, 2, 3, 4])
        ll.appendright(5)
        self.assertEqual([1, 2, 3, 4, 5], list(ll))

    def test_appendnode(self):
        ll = sllist([1, 2, 3, 4])
        node = sllistnode(5)
        ll.appendnode(node)
        self.assertEqual([1, 2, 3, 4, 5], list(ll))
        self.assertIs(node, ll.last)

    def test_appendnode_with_bad_argument_type(self):
        ll = sllist()
        self.assertRaises(TypeError, ll.appendnode, 'non-node argument')

    def test_appendnode_with_already_owned_node(self):
        ll = sllist()
        other_list = sllist([1234])
        self.assertRaises(ValueError, ll.appendnode, other_list.first)

    def test_appendnode_refcount_update(self):
        ll = sllist()
        node = ll.appendnode(sllistnode(1234))
        self.assertGreaterEqual(sys.getrefcount(node), 3)

    def test_pop_left_from_one_elem(self):
        ll = sllist(py23_xrange(0, 100))
        dd = ll.popleft()
        self.assertEqual(dd, 0)

    def test_pop_right_from_one_elem(self):
        ll = sllist(py23_xrange(0, 100))
        dd = ll.popright()
        self.assertEqual(dd, 99)

    def test_pop_right_from_n_elem(self):
        ll = sllist(py23_xrange(0, 100))
        dd = ll.popright()
        self.assertEqual(dd, 99)

    def test_get_node_at_from_n_elem(self):
        ll = sllist(py23_xrange(0, 100))
        self.assertEqual(50, ll[50])

    def test_remove_from_n_elem(self):
        ll = sllist()
        nn = sllistnode()
        ll.append(nn)
        to_del = ll.nodeat(0)
        ll.remove(to_del)
        self.assertEqual(None, None)

    def test_insert_after(self):
        ll = sllist([1, 3, '123'])
        ll.insertafter(100, ll.first)
        self.assertEqual([1, 100, 3, '123'], list(ll))

    def test_insert_before(self):
        ll = sllist([1, 3, '123'])
        ll.insertbefore(100, ll.first)
        self.assertEqual([100, 1, 3, '123'], list(ll))

    def test_insert_value_after(self):
        ll = sllist(py23_xrange(4))
        ref = sllist([0, 1, 2, 10, 3])
        prev = ll.nodeat(2)
        next = ll.nodeat(3)
        arg_node = sllistnode(10)
        new_node = ll.insertafter(arg_node, ll.nodeat(2))
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, next)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(ll, ref)

    def test_insert_value_after_last(self):
        ll = sllist(py23_xrange(4))
        ref = sllist([0, 1, 2, 3, 10])
        prev = ll.nodeat(3)
        arg_node = sllistnode(10)
        new_node = ll.insertafter(arg_node, ll.nodeat(-1))
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, None)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(new_node, ll.last)
        self.assertEqual(ll, ref)

    def test_insert_value_before(self):
        ll = sllist(py23_xrange(4))
        ref = sllist([0, 1, 10, 2, 3])
        prev = ll.nodeat(1)
        next = ll.nodeat(2)
        arg_node = sllistnode(10)
        new_node = ll.insertbefore(arg_node, ll.nodeat(2))
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, next)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(ll, ref)

    def test_insert_value_before_first(self):
        ll = sllist(py23_xrange(4))
        ref = sllist([10, 0, 1, 2, 3])
        next = ll.nodeat(0)
        arg_node = sllistnode(10)
        new_node = ll.insertbefore(arg_node, ll.nodeat(0))
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, next)
        self.assertEqual(new_node, ll.first)
        self.assertEqual(ll, ref)

    def test_insert_invalid_ref(self):
        ll = sllist([1, 2, 3, 4])
        self.assertRaises(TypeError, ll.insertafter, 10, 1)
        self.assertRaises(TypeError, ll.insertafter, 10, 'abc')
        self.assertRaises(TypeError, ll.insertafter, 10, [])
        self.assertRaises(ValueError, ll.insertafter, 10, sllistnode())
        self.assertRaises(TypeError, ll.insertbefore, 10, 1)
        self.assertRaises(TypeError, ll.insertbefore, 10, 'abc')
        self.assertRaises(TypeError, ll.insertbefore, 10, [])
        self.assertRaises(ValueError, ll.insertbefore, 10, sllistnode())

    def test_insert_node_after_first(self):
        ll = sllist([1, 3, '123'])
        arg_node = sllistnode(100)
        new_node = ll.insertnodeafter(arg_node, ll.first)
        self.assertEqual([1, 100, 3, '123'], list(ll))
        self.assertEqual(new_node, arg_node);

    def test_insert_node_before_first(self):
        ll = sllist([1, 3, '123'])
        arg_node = sllistnode(100)
        new_node = ll.insertnodebefore(arg_node, ll.first)
        self.assertEqual([100, 1, 3, '123'], list(ll))
        self.assertEqual(new_node, arg_node);

    def test_insert_node_after_another(self):
        ll = sllist(py23_xrange(4))
        ref = sllist([0, 1, 2, 10, 3])
        prev = ll.nodeat(2)
        next = ll.nodeat(3)
        arg_node = sllistnode(10)
        new_node = ll.insertnodeafter(arg_node, ll.nodeat(2))
        self.assertEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, next)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(ll, ref)

    def test_insert_node_after_last(self):
        ll = sllist(py23_xrange(4))
        ref = sllist([0, 1, 2, 3, 10])
        prev = ll.nodeat(3)
        arg_node = sllistnode(10)
        new_node = ll.insertnodeafter(arg_node, ll.nodeat(-1))
        self.assertEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, None)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(new_node, ll.last)
        self.assertEqual(ll, ref)

    def test_insert_node_before_another(self):
        ll = sllist(py23_xrange(4))
        ref = sllist([0, 1, 10, 2, 3])
        prev = ll.nodeat(1)
        next = ll.nodeat(2)
        arg_node = sllistnode(10)
        new_node = ll.insertnodebefore(arg_node, ll.nodeat(2))
        self.assertEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, next)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(ll, ref)

    def test_insert_node_before_first(self):
        ll = sllist(py23_xrange(4))
        ref = sllist([10, 0, 1, 2, 3])
        next = ll.nodeat(0)
        arg_node = sllistnode(10)
        new_node = ll.insertnodebefore(arg_node, ll.nodeat(0))
        self.assertEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, next)
        self.assertEqual(new_node, ll.first)
        self.assertEqual(ll, ref)

    def test_insert_node_after_with_bad_argument_type(self):
        ll = sllist([1234])
        self.assertRaises(
            TypeError, ll.insertnodeafter, 'non-node argument', ll.first)

    def test_insert_node_before_with_bad_argument_type(self):
        ll = sllist([1234])
        self.assertRaises(
            TypeError, ll.insertnodebefore, 'non-node argument', ll.first)

    def test_insert_node_after_with_already_owned_node(self):
        ll = sllist([1234])
        other_list = sllist([5678])
        self.assertRaises(
            ValueError, ll.insertnodeafter, other_list.first, ll.first)

    def test_insert_node_before_with_already_owned_node(self):
        ll = sllist([1234])
        other_list = sllist([5678])
        self.assertRaises(
            ValueError, ll.insertnodebefore, other_list.first, ll.first)

    def test_insert_node_with_invalid_ref(self):
        ll = sllist([1, 2, 3, 4])
        self.assertRaises(TypeError, ll.insertnodeafter, sllistnode(10), 1)
        self.assertRaises(TypeError, ll.insertnodeafter, sllistnode(10), 'abc')
        self.assertRaises(TypeError, ll.insertnodeafter, sllistnode(10), [])
        self.assertRaises(
            ValueError, ll.insertnodeafter, sllistnode(10), sllistnode())
        self.assertRaises(TypeError, ll.insertnodebefore, sllistnode(10), 1)
        self.assertRaises(TypeError, ll.insertnodebefore, sllistnode(10), 'abc')
        self.assertRaises(TypeError, ll.insertnodebefore, sllistnode(10), [])
        self.assertRaises(
            ValueError, ll.insertnodebefore, sllistnode(10), sllistnode())

    def test_insert_node_after_refcount_update(self):
        ll = sllist([1234])
        node = ll.insertnodeafter(sllistnode(5678), ll.nodeat(0))
        self.assertGreaterEqual(sys.getrefcount(node), 3)

    def test_insert_node_before_refcount_update(self):
        ll = sllist([1234])
        node = ll.insertnodebefore(sllistnode(5678), ll.nodeat(0))
        self.assertGreaterEqual(sys.getrefcount(node), 3)

    def test_append(self):
        ll = sllist(py23_xrange(4))
        ref = sllist([0, 1, 2, 3, 10])
        prev = ll.nodeat(-1)
        arg_node = sllistnode(10)
        new_node = ll.append(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, None)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(ll.last, new_node)
        self.assertEqual(ll, ref)

    def test_appendleft(self):
        ll = sllist(py23_xrange(4))
        ref = sllist([10, 0, 1, 2, 3])
        next = ll.nodeat(0)
        arg_node = sllistnode(10)
        new_node = ll.appendleft(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, next)
        self.assertEqual(ll.first, new_node)
        self.assertEqual(ll, ref)

    def test_appendright(self):
        ll = sllist(py23_xrange(4))
        ref = sllist([0, 1, 2, 3, 10])
        prev = ll.nodeat(-1)
        arg_node = sllistnode(10)
        new_node = ll.appendright(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, None)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(ll.last, new_node)
        self.assertEqual(ll, ref)

    def test_extend(self):
        a_ref = py23_range(0, 1024, 4)
        b_ref = py23_range(8092, 8092 + 1024, 4)
        b = sllist(b_ref)
        ab_ref = sllist(a_ref + b_ref)
        a = sllist(a_ref)
        a.extend(b)
        self.assertEqual(a, ab_ref)
        self.assertEqual(len(a), len(ab_ref))
        a = sllist(a_ref)
        a.extend(b_ref)
        self.assertEqual(a, ab_ref)
        self.assertEqual(len(a), len(ab_ref))
        a = sllist(a_ref)
        a.extend(a)
        self.assertEqual(a, sllist(a_ref + a_ref))
        self.assertEqual(len(a), len(a_ref) * 2)

    def test_extend_empty(self):
        filled_ref = py23_range(0, 1024, 4)
        filled = sllist(filled_ref)
        empty = sllist()
        empty.extend(empty)
        self.assertEqual(empty, sllist([] + []))
        self.assertEqual(len(empty), 0)
        empty = sllist()
        empty.extend(filled)
        self.assertEqual(empty, sllist([] + filled_ref))
        self.assertEqual(len(empty), len(filled_ref))
        empty = sllist()
        filled.extend(empty)
        self.assertEqual(filled, sllist(filled_ref + []))
        self.assertEqual(len(filled), len(filled_ref))

    def test_extendleft(self):
        a_ref = py23_range(0, 1024, 4)
        b_ref = py23_range(8092, 8092 + 1024, 4)
        b = sllist(b_ref)
        ab_ref = sllist(list(reversed(b_ref)) + a_ref)
        a = sllist(a_ref)
        a.extendleft(b)
        self.assertEqual(a, ab_ref)
        self.assertEqual(len(a), len(ab_ref))
        a = sllist(a_ref)
        a.extendleft(b_ref)
        self.assertEqual(a, ab_ref)
        self.assertEqual(len(a), len(ab_ref))
        a = sllist(a_ref)
        a.extendleft(a)
        self.assertEqual(a, sllist(list(reversed(a_ref)) + a_ref))
        self.assertEqual(len(a), len(a_ref) * 2)

    def test_extendleft_empty(self):
        filled_ref = py23_range(0, 1024, 4)
        filled = sllist(filled_ref)
        empty = sllist()
        empty.extendleft(empty)
        self.assertEqual(empty, sllist([] + []))
        self.assertEqual(len(empty), 0)
        empty = sllist()
        empty.extendleft(filled)
        self.assertEqual(empty, sllist(list(reversed(filled_ref)) + []))
        self.assertEqual(len(empty), len(filled_ref))
        empty = sllist()
        filled.extendleft(empty)
        self.assertEqual(filled, sllist(list(reversed([])) + filled_ref))
        self.assertEqual(len(filled), len(filled_ref))

    def test_extendright(self):
        a_ref = py23_range(0, 1024, 4)
        b_ref = py23_range(8092, 8092 + 1024, 4)
        b = sllist(b_ref)
        ab_ref = sllist(a_ref + b_ref)
        a = sllist(a_ref)
        a.extendright(b)
        self.assertEqual(a, ab_ref)
        self.assertEqual(len(a), len(ab_ref))
        a = sllist(a_ref)
        a.extendright(b_ref)
        self.assertEqual(a, ab_ref)
        self.assertEqual(len(a), len(ab_ref))
        a = sllist(a_ref)
        a.extendright(a)
        self.assertEqual(a, sllist(a_ref + a_ref))
        self.assertEqual(len(a), len(a_ref) * 2)

    def test_extendright_empty(self):
        filled_ref = py23_range(0, 1024, 4)
        filled = sllist(filled_ref)
        empty = sllist()
        empty.extendright(empty)
        self.assertEqual(empty, sllist([] + []))
        self.assertEqual(len(empty), 0)
        empty = sllist()
        empty.extendright(filled)
        self.assertEqual(empty, sllist([] + filled_ref))
        self.assertEqual(len(empty), len(filled_ref))
        empty = sllist()
        filled.extendright(empty)
        self.assertEqual(filled, sllist(filled_ref + []))
        self.assertEqual(len(filled), len(filled_ref))

    def test_clear_empty(self):
        empty_list = sllist()
        empty_list.clear()
        self.assertEqual(empty_list.first, None)
        self.assertEqual(empty_list.last, None)
        self.assertEqual(empty_list.size, 0)
        self.assertEqual(list(empty_list), [])

    def test_clear(self):
        ll = sllist(py23_xrange(0, 1024, 4))
        del_node = ll.nodeat(4)
        ll.clear()
        self.assertEqual(ll.first, None)
        self.assertEqual(ll.last, None)
        self.assertEqual(ll.size, 0)
        self.assertEqual(list(ll), [])
        self.assertEqual(del_node.next, None)

    def test_pop(self):
        ref = py23_range(0, 1024, 4)
        ll = sllist(ref)
        result = ll.pop()
        self.assertEqual(result, ref[-1])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.last.value, ref[-2])
        self.assertEqual(list(ll), ref[:-1])

    def test_node_after_pop(self):
        ll = sllist([1, 2])
        del_node = ll.last
        ll.pop()
        self.assertIs(del_node.next, None)
        self.assertIs(del_node.owner, None)

    def test_popleft(self):
        ref = py23_range(0, 1024, 4)
        ll = sllist(ref)
        result = ll.popleft()
        self.assertEqual(result, ref[0])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.first.value, ref[1])
        self.assertEqual(list(ll), ref[1:])

    def test_node_after_popleft(self):
        ll = sllist([1, 2])
        del_node = ll.first
        ll.popleft()
        self.assertIs(del_node.next, None)
        self.assertIs(del_node.owner, None)

    def test_popright(self):
        ref = py23_range(0, 1024, 4)
        ll = sllist(ref)
        result = ll.popright()
        self.assertEqual(result, ref[-1])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.last.value, ref[-2])
        self.assertEqual(list(ll), ref[:-1])

    def test_node_after_popright(self):
        ll = sllist([1, 2])
        del_node = ll.last
        ll.popright()
        self.assertIs(del_node.next, None)
        self.assertIs(del_node.owner, None)

    def test_pop_from_empty_list(self):
        ll = sllist()
        self.assertRaises(ValueError, ll.pop)
        self.assertRaises(ValueError, ll.popleft)
        self.assertRaises(ValueError, ll.popright)

    def test_remove(self):
        ref = py23_range(0, 1024, 4)
        ll = sllist(ref)
        prev_node = ll.nodeat(3)
        del_node = ll.nodeat(4)
        next_node = ll.nodeat(5)
        result = ll.remove(del_node)
        ref_result = ref[4]
        del ref[4]
        self.assertEqual(list(ll), ref)
        self.assertEqual(result, ref_result)
        self.assertEqual(len(ll), len(ref))
        self.assertEqual(ll.size, len(ref))
        self.assertEqual(prev_node.next, next_node)

    def test_remove_after_remove(self):
        ll = sllist([1, 2, 3])
        del_node = ll.nodeat(1)
        ll.remove(del_node)
        self.assertIs(del_node.next, None)
        self.assertIs(del_node.owner, None)

    def test_remove_from_empty_list(self):
        ll = sllist()
        self.assertRaises(ValueError, ll.remove, sllistnode())

    def test_remove_invalid_node(self):
        ll = sllist([1, 2, 3, 4])
        self.assertRaises(ValueError, ll.remove, sllistnode())
        self.assertEqual(len(ll), 4)

    def test_remove_already_deleted_node(self):
        ll = sllist([1, 2, 3, 4])
        node = ll.nodeat(2)
        ll.remove(node)
        self.assertRaises(ValueError, ll.remove, node)

    def test_rotate_left(self):
        for n in py23_xrange(128):
            ref = py23_range(32)
            split = n % len(ref)
            ref_result = ref[split:] + ref[:split]
            ll = sllist(ref)
            new_first = ll.nodeat(split)
            new_last = ll.nodeat(split - 1)
            ll.rotate(-n)
            self.assertEqual(list(ll), ref_result)
            self.assertEqual(ll.first, new_first)
            self.assertEqual(ll.last, new_last)
            self.assertEqual(ll.size, len(ref))
            self.assertEqual(ll.last.next, None)

    def test_rotate_right(self):
        for n in py23_xrange(128):
            ref = py23_range(32)
            split = n % len(ref)
            ref_result = ref[-split:] + ref[:-split]
            ll = sllist(ref)
            new_first = ll.nodeat(-split)
            last_idx = -split - 1
            new_last = ll.nodeat(last_idx)
            ll.rotate(n)
            self.assertEqual(list(ll), ref_result)
            self.assertEqual(ll.first, new_first)
            self.assertEqual(ll.last, new_last)
            self.assertEqual(ll.size, len(ref))
            self.assertEqual(ll.last.next, None)

    def test_rotate_left_empty(self):
        for n in py23_xrange(4):
            ll = sllist()
            ll.rotate(-n)
            self.assertEqual(ll.first, None)
            self.assertEqual(ll.last, None)
            self.assertEqual(ll.size, 0)

    def test_rotate_right_empty(self):
        for n in py23_xrange(4):
            ll = sllist()
            ll.rotate(n)
            self.assertEqual(ll.first, None)
            self.assertEqual(ll.last, None)
            self.assertEqual(ll.size, 0)

    def test_getitem(self):
        ref = py23_range(0, 1024, 4)
        ll = sllist(ref)
        for idx in py23_xrange(len(ll)):
            self.assertFalse(isinstance(ll[idx], sllistnode))
            self.assertEqual(ll[idx], ref[idx])
        for idx in py23_xrange(len(ll)):
            self.assertFalse(isinstance(ll[idx], sllistnode))
            self.assertEqual(ll[-idx - 1], ref[-idx - 1])
        self.assertRaises(TypeError, ll.__getitem__, None)
        self.assertRaises(TypeError, ll.__getitem__, 'abc')
        self.assertRaises(IndexError, ll.__getitem__, len(ref))
        self.assertRaises(IndexError, ll.__getitem__, -len(ref) - 1)

    def test_getitem_empty(self):
        ll = sllist()
        self.assertRaises(TypeError, ll.__getitem__, None)
        self.assertRaises(TypeError, ll.__getitem__, 'abc')
        self.assertRaises(IndexError, ll.__getitem__, 0)
        self.assertRaises(IndexError, ll.__getitem__, -1)

    def test_del(self):
        ref = py23_range(0, 1024, 4)
        ll = sllist(ref)
        del ll[0]
        del ref[0]
        self.assertEqual(list(ll), ref)
        del ll[len(ll) - 1]
        del ref[len(ref) - 1]
        self.assertEqual(list(ll), ref)
        del ll[(len(ll) - 1) // 2]
        del ref[(len(ref) - 1) // 2]
        self.assertEqual(list(ll), ref)

        def del_item(idx):
            del ll[idx]
        self.assertRaises(IndexError, del_item, len(ll))

        for i in py23_xrange(len(ll)):
            del ll[0]
        self.assertEqual(len(ll), 0)

    def test_node_after_del(self):
        ll = sllist([1, 2, 3])
        del_node = ll.nodeat(1)
        del ll[1]
        self.assertIs(del_node.next, None)
        self.assertIs(del_node.owner, None)

    def test_concat(self):
        a_ref = py23_range(0, 1024, 4)
        a = sllist(a_ref)
        b_ref = py23_range(8092, 8092 + 1024, 4)
        b = sllist(b_ref)
        ab_ref = sllist(a_ref + b_ref)
        c = a + b
        self.assertEqual(c, ab_ref)
        self.assertEqual(len(c), len(ab_ref))
        c = a + b_ref
        self.assertEqual(c, ab_ref)
        self.assertEqual(len(c), len(ab_ref))

    def test_concat_empty(self):
        empty = sllist()
        filled_ref = py23_range(0, 1024, 4)
        filled = sllist(filled_ref)
        res = empty + empty
        self.assertEqual(res, sllist([] + []))
        self.assertEqual(len(res), 0)
        res = empty + filled
        self.assertEqual(res, sllist([] + filled_ref))
        self.assertEqual(len(res), len(filled_ref))
        res = filled + empty
        self.assertEqual(res, sllist(filled_ref + []))
        self.assertEqual(len(res), len(filled_ref))

    def test_concat_inplace(self):
        a_ref = py23_range(0, 1024, 4)
        b_ref = py23_range(8092, 8092 + 1024, 4)
        b = sllist(b_ref)
        ab_ref = sllist(a_ref + b_ref)
        a = sllist(a_ref)
        a += b
        self.assertEqual(a, ab_ref)
        self.assertEqual(len(a), len(ab_ref))
        a = sllist(a_ref)
        a += b_ref
        self.assertEqual(a, ab_ref)
        self.assertEqual(len(a), len(ab_ref))
        a = sllist(a_ref)
        a += a
        self.assertEqual(a, sllist(a_ref + a_ref))
        self.assertEqual(len(a), len(ab_ref))

    def test_concat_inplace_empty(self):
        filled_ref = py23_range(0, 1024, 4)
        filled = sllist(filled_ref)
        empty = sllist()
        empty += empty
        self.assertEqual(empty, sllist([] + []))
        self.assertEqual(len(empty), 0)
        empty = sllist()
        empty += filled
        self.assertEqual(empty, sllist([] + filled_ref))
        self.assertEqual(len(empty), len(filled_ref))
        empty = sllist()
        filled += empty
        self.assertEqual(filled, sllist(filled_ref + []))
        self.assertEqual(len(filled), len(filled_ref))

    def test_repeat(self):
        ref = py23_range(0, 1024, 4)
        ll = sllist(ref)
        self.assertEqual(ll * 4, sllist(ref * 4))

    def test_repeat_empty(self):
        ll = sllist()
        self.assertEqual(ll * 4, sllist([] * 4))

    def test_repeat_inplace(self):
        ref = py23_range(0, 1024, 4)
        ll = sllist(ref)
        ll *= 4
        self.assertEqual(ll, sllist(ref * 4))

    def test_repeat_inplace_empty(self):
        ll = sllist()
        ll *= 4
        self.assertEqual(ll, sllist([] * 4))

    def test_list_readonly_attributes(self):
        if sys.hexversion >= 0x03000000:
            expected_error = AttributeError
        else:
            expected_error = TypeError

        ll = sllist(py23_range(4))
        self.assertRaises(expected_error, setattr, ll, 'first', None)
        self.assertRaises(expected_error, setattr, ll, 'last', None)
        self.assertRaises(expected_error, setattr, ll, 'size', None)

    def test_node_readonly_attributes(self):
        if sys.hexversion >= 0x03000000:
            expected_error = AttributeError
        else:
            expected_error = TypeError

        ll = sllistnode()
        self.assertRaises(expected_error, setattr, ll, 'next', None)

    def test_node_owner(self):
        ll = sllist([1234])
        owner_ref = ll.first.owner
        self.assertIsInstance(owner_ref, weakref.ref)
        self.assertIs(owner_ref(), ll)
        del ll
        self.assertIsNone(owner_ref())

    def test_list_hash(self):
        self.assertEqual(hash(sllist()), hash(sllist()))
        self.assertEqual(hash(sllist(py23_range(0, 1024, 4))),
            hash(sllist(py23_range(0, 1024, 4))))
        self.assertEqual(hash(sllist([0, 2])), hash(sllist([0.0, 2.0])))
        self.assertNotEqual(hash(sllist([1, 2])), hash(sllist([2, 1])))

    def test_list_can_be_subclassed(self):
        class DerivedList(sllist):
            pass

    def test_list_node_can_be_subclassed(self):
        class DerivedNode(sllistnode):
            pass

    def test_cyclic_list_destruction_does_not_release_extra_None_refs(self):
        original_ref_count = sys.getrefcount(None)

        for _ in range(original_ref_count * 10):
            ll = sllist()
            ll.append(sllistnode(ll))
            del ll

        self.assertGreater(sys.getrefcount(None), 0)

    def test_cyclic_node_destruction_does_not_release_extra_None_refs(self):
        original_ref_count = sys.getrefcount(None)

        for _ in range(original_ref_count * 10):
            ll = self.make_recursive_node_list()
            del ll

        self.assertGreater(sys.getrefcount(None), 0)


class testdllist(unittest.TestCase):

    def test_init_empty(self):
        ll = dllist()
        self.assertEqual(len(ll), 0)
        self.assertEqual(ll.size, 0)
        self.assertEqual(list(ll), [])

    def test_init_with_sequence(self):
        ref = py23_range(0, 1024, 4)
        ll = dllist(ref)
        self.assertEqual(len(ll), len(ref))
        self.assertEqual(ll.size, len(ref))
        self.assertEqual(list(ll), ref)

    def test_init_with_non_sequence(self):
        self.assertRaises(TypeError, dllist, None);
        self.assertRaises(TypeError, dllist, 1);
        self.assertRaises(TypeError, dllist, 1.5);

    def test_str(self):
        a = dllist([])
        self.assertEqual(str(a), 'dllist()')
        b = dllist([None, 1, 'abc'])
        self.assertEqual(str(b), 'dllist([None, 1, abc])')

    def test_repr(self):
        a = dllist([])
        self.assertEqual(repr(a), 'dllist()')
        b = dllist([None, 1, 'abc'])
        self.assertEqual(repr(b), 'dllist([None, 1, \'abc\'])')

    def test_node_str(self):
        a = dllist([None, None]).first
        self.assertEqual(str(a), 'dllistnode(None)')
        b = dllist([1, None]).first
        self.assertEqual(str(b), 'dllistnode(1)')
        c = dllist(['abc', None]).first
        self.assertEqual(str(c), 'dllistnode(abc)')

    def test_node_repr(self):
        a = dllist([None]).first
        self.assertEqual(repr(a), '<dllistnode(None)>')
        b = dllist([1, None]).first
        self.assertEqual(repr(b), '<dllistnode(1)>')
        c = dllist(['abc', None]).first
        self.assertEqual(repr(c), '<dllistnode(\'abc\')>')

    def test_str_recursive_list(self):
        ll = dllist()
        ll.append(dllistnode(ll))
        self.assertEqual(str(ll), 'dllist([dllist(<...>)])')

    def test_str_recursive_node(self):
        ll = self.make_recursive_node_list()
        self.assertEqual(str(ll), 'dllist([dllistnode(dllistnode(<...>))])')

    def test_repr_recursive_list(self):
        ll = dllist()
        ll.append(dllistnode(ll))
        self.assertEqual(repr(ll), 'dllist([dllist(<...>)])')

    def test_repr_recursive_node(self):
        ll = self.make_recursive_node_list()
        self.assertEqual(repr(ll), 'dllist([<dllistnode(dllistnode(<...>))>])')

    def make_recursive_node_list(self):
        ll = dllist()
        node = dllistnode()
        node.value = node
        ll.append(node)
        return ll

    def test_cmp(self):
        a = dllist(py23_xrange(0, 1100))
        b = dllist(py23_xrange(0, 1101))
        c = dllist([1, 2, 3, 4])
        d = dllist([1, 2, 3, 5])
        e = dllist([1, 0, 0, 0])
        f = dllist([0, 0, 0, 0])
        self.assertEqual(cmp(a, a), 0)
        self.assertEqual(cmp(a, b), -1)
        self.assertEqual(cmp(b, a), 1)
        self.assertEqual(cmp(c, d), -1)
        self.assertEqual(cmp(d, c), 1)
        self.assertEqual(cmp(e, f), 1)
        self.assertEqual(cmp(f, e), -1)

    def test_cmp_nonlist(self):
        a = dllist(py23_xrange(0, 1100))
        b = [py23_xrange(0, 1100)]
        if sys.hexversion < 0x03000000:
            # actual order is not specified by language
            self.assertNotEqual(cmp(a, b), 0)
            self.assertNotEqual(cmp(b, a), 0)
            self.assertNotEqual(cmp([], a), 0)
            self.assertNotEqual(cmp(a, []), 0)

    def test_eq(self):
        a = dllist(py23_xrange(0, 1100))
        b = dllist(py23_xrange(0, 1101))
        c = dllist([1, 2, 3, 4])
        d = dllist([1, 2, 3, 5])
        e = dllist([1, 0, 0, 0])
        f = dllist([0, 0, 0, 0])
        self.assertTrue(dllist() == dllist())
        self.assertTrue(a == a)
        self.assertFalse(dllist() == a)
        self.assertFalse(a == dllist())
        self.assertFalse(a == b)
        self.assertFalse(b == a)
        self.assertFalse(c == d)
        self.assertFalse(d == c)
        self.assertFalse(e == f)
        self.assertFalse(f == e)

    def test_ne(self):
        a = dllist(py23_xrange(0, 1100))
        b = dllist(py23_xrange(0, 1101))
        c = dllist([1, 2, 3, 4])
        d = dllist([1, 2, 3, 5])
        e = dllist([1, 0, 0, 0])
        f = dllist([0, 0, 0, 0])
        self.assertFalse(dllist() != dllist())
        self.assertFalse(a != a)
        self.assertTrue(dllist() != a)
        self.assertTrue(a != dllist())
        self.assertTrue(a != b)
        self.assertTrue(b != a)
        self.assertTrue(c != d)
        self.assertTrue(d != c)
        self.assertTrue(e != f)
        self.assertTrue(f != e)

    def test_lt(self):
        a = dllist(py23_xrange(0, 1100))
        b = dllist(py23_xrange(0, 1101))
        c = dllist([1, 2, 3, 4])
        d = dllist([1, 2, 3, 5])
        e = dllist([1, 0, 0, 0])
        f = dllist([0, 0, 0, 0])
        self.assertFalse(dllist() < dllist())
        self.assertFalse(a < a)
        self.assertTrue(dllist() < a)
        self.assertFalse(a < dllist())
        self.assertTrue(a < b)
        self.assertFalse(b < a)
        self.assertTrue(c < d)
        self.assertFalse(d < c)
        self.assertFalse(e < f)
        self.assertTrue(f < e)

    def test_gt(self):
        a = dllist(py23_xrange(0, 1100))
        b = dllist(py23_xrange(0, 1101))
        c = dllist([1, 2, 3, 4])
        d = dllist([1, 2, 3, 5])
        e = dllist([1, 0, 0, 0])
        f = dllist([0, 0, 0, 0])
        self.assertFalse(dllist() > dllist())
        self.assertFalse(a > a)
        self.assertFalse(dllist() > a)
        self.assertTrue(a > dllist())
        self.assertFalse(a > b)
        self.assertTrue(b > a)
        self.assertFalse(c > d)
        self.assertTrue(d > c)
        self.assertTrue(e > f)
        self.assertFalse(f > e)

    def test_le(self):
        a = dllist(py23_xrange(0, 1100))
        b = dllist(py23_xrange(0, 1101))
        c = dllist([1, 2, 3, 4])
        d = dllist([1, 2, 3, 5])
        e = dllist([1, 0, 0, 0])
        f = dllist([0, 0, 0, 0])
        self.assertTrue(dllist() <= dllist())
        self.assertTrue(a <= a)
        self.assertTrue(dllist() <= a)
        self.assertFalse(a <= dllist())
        self.assertTrue(a <= b)
        self.assertFalse(b <= a)
        self.assertTrue(c <= d)
        self.assertFalse(d <= c)
        self.assertFalse(e <= f)
        self.assertTrue(f <= e)

    def test_ge(self):
        a = dllist(py23_xrange(0, 1100))
        b = dllist(py23_xrange(0, 1101))
        c = dllist([1, 2, 3, 4])
        d = dllist([1, 2, 3, 5])
        e = dllist([1, 0, 0, 0])
        f = dllist([0, 0, 0, 0])
        self.assertTrue(dllist() >= dllist())
        self.assertTrue(a >= a)
        self.assertFalse(dllist() >= a)
        self.assertTrue(a >= dllist())
        self.assertFalse(a >= b)
        self.assertTrue(b >= a)
        self.assertFalse(c >= d)
        self.assertTrue(d >= c)
        self.assertTrue(e >= f)
        self.assertFalse(f >= e)

    def test_nodeat(self):
        ref = py23_range(0, 1024, 4)
        ll = dllist(ref)
        for idx in py23_xrange(len(ll)):
            self.assertTrue(isinstance(ll.nodeat(idx), dllistnode))
            self.assertEqual(ll.nodeat(idx).value, ref[idx])
        for idx in py23_xrange(len(ll)):
            self.assertTrue(isinstance(ll.nodeat(idx), dllistnode))
            self.assertEqual(ll.nodeat(-idx - 1).value, ref[-idx - 1])
        self.assertRaises(TypeError, ll.nodeat, None)
        self.assertRaises(TypeError, ll.nodeat, 'abc')
        self.assertRaises(IndexError, ll.nodeat, len(ref))
        self.assertRaises(IndexError, ll.nodeat, -len(ref) - 1)

    def test_nodeat_empty(self):
        ll = dllist()
        self.assertRaises(TypeError, ll.nodeat, None)
        self.assertRaises(TypeError, ll.nodeat, 'abc')
        self.assertRaises(IndexError, ll.nodeat, 0)
        self.assertRaises(IndexError, ll.nodeat, -1)

    def test_iter(self):
        ref = py23_range(0, 1024, 4)
        ll = dllist(ref)
        idx = 0
        for val in ll:
            self.assertFalse(isinstance(val, dllistnode))
            self.assertEqual(val, ref[idx])
            idx += 1
        self.assertEqual(idx, len(ref))

    def test_iter_empty(self):
        ll = dllist()
        count = 0
        for val in ll:
            count += 1
        self.assertEqual(count, 0)

    def test_iter_of_appended_node(self):
        ll = dllist(['initial item'])

        appended_item_visited = False

        for x in ll:
            if x == 'initial item':
                ll.append('new item')
            elif x == 'new item':
                appended_item_visited = True

        self.assertTrue(appended_item_visited)

    def test_iter_of_removed_node(self):
        ll = dllist(['x', 'removed item'])

        for x in ll:
            self.assertNotEqual(x, 'removed item')
            ll.remove(ll.last)

    def test_reversed(self):
        ref = py23_range(0, 1024, 4)
        ll = dllist(ref)
        idx = len(ref) - 1
        for val in reversed(ll):
            self.assertFalse(isinstance(val, dllistnode))
            self.assertEqual(val, ref[idx])
            idx -= 1
        self.assertEqual(idx, -1)

    def test_reversed_empty(self):
        ll = dllist()
        count = 0
        for val in reversed(ll):
            count += 1
        self.assertEqual(count, 0)

    def test_insert_value(self):
        ll = dllist(py23_xrange(4))
        ref = dllist([0, 1, 2, 3, 10])
        prev = ll.nodeat(-1)
        arg_node = dllistnode(10)
        new_node = ll.insert(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.prev, prev)
        self.assertEqual(new_node.next, None)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(new_node, ll.last)
        self.assertEqual(ll, ref)

    def test_insert_value_before(self):
        ll = dllist(py23_xrange(4))
        ref = dllist([0, 1, 10, 2, 3])
        prev = ll.nodeat(1)
        next = ll.nodeat(2)
        arg_node = dllistnode(10)
        new_node = ll.insert(arg_node, ll.nodeat(2))
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.prev, prev)
        self.assertEqual(new_node.next, next)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(next.prev, new_node)
        self.assertEqual(ll, ref)

    def test_insert_value_before_first(self):
        ll = dllist(py23_xrange(4))
        ref = dllist([10, 0, 1, 2, 3])
        next = ll.nodeat(0)
        arg_node = dllistnode(10)
        new_node = ll.insert(arg_node, ll.nodeat(0))
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.prev, None)
        self.assertEqual(new_node.next, next)
        self.assertEqual(next.prev, new_node)
        self.assertEqual(new_node, ll.first)
        self.assertEqual(ll, ref)

    def test_insert_invalid_ref(self):
        ll = dllist()
        self.assertRaises(TypeError, ll.insert, 10, 1)
        self.assertRaises(TypeError, ll.insert, 10, 'abc')
        self.assertRaises(TypeError, ll.insert, 10, [])
        self.assertRaises(ValueError, ll.insert, 10, dllistnode())

    def test_insertbefore_without_ref_node(self):
        ll = dllist()
        self.assertRaises(TypeError, ll.insertbefore, 1234)

    def test_insertbefore_with_invalid_ref_node(self):
        ll = dllist()
        other_list = dllist(['node in other list'])
        self.assertRaises(TypeError, ll.insertbefore, 1234, None)
        self.assertRaises(TypeError, ll.insertbefore, 1234, 'not a dllist node')
        self.assertRaises(ValueError, ll.insertbefore, 1234, dllistnode())
        self.assertRaises(ValueError, ll.insertbefore, 1234, other_list.first)

    def test_insertbefore_adds_item_in_correct_position(self):
        ll = dllist([0, 1, 2, 3, 4])
        ref_node = ll.nodeat(2)
        ll.insertbefore(1234, ref_node)
        self.assertEqual(ll, dllist([0, 1, 1234, 2, 3, 4]))

    def test_insertbefore_returns_node_with_inserted_value(self):
        ll = dllist([0])
        value = 'inserted value'
        new_node = ll.insertbefore(value, ll.first)
        self.assertIs(new_node.value, value)

    def test_insertbefore_extracts_value_from_inserted_node(self):
        ll = dllist([0])
        free_node = dllistnode('free node')
        other_list = dllist(['node in other list'])
        new_node = ll.insertbefore(free_node, ll.first)
        self.assertIsNot(new_node, free_node)
        self.assertIs(new_node.value, free_node.value)
        new_node = ll.insertbefore(other_list.first, ll.first)
        self.assertIsNot(new_node, other_list.first)
        self.assertIs(new_node.value, other_list.first.value)

    def test_insertbefore_correctly_links_items(self):
        ll = dllist([0, 1, 2, 3])
        prev_node = ll.nodeat(1)
        next_node = ll.nodeat(2)
        new_node = ll.insertbefore(1234, next_node)
        self.assertIs(new_node.prev, prev_node)
        self.assertIs(prev_node.next, new_node)
        self.assertIs(new_node.next, next_node)
        self.assertIs(next_node.prev, new_node)

    def test_insertbefore_before_first_item_makes_node_without_prev(self):
        ll = dllist([0])
        new_node = ll.insertbefore(1234, ll.first)
        self.assertIs(new_node.prev, None)

    def test_insertbefore_before_first_item_updates_list_head(self):
        ll = dllist([0])
        original_head = ll.first
        new_node = ll.insertbefore(1234, ll.first)
        self.assertIs(ll.first, new_node)

    def test_insertbefore_after_first_item_does_not_update_list_head(self):
        ll = dllist([0, 1])
        original_head = ll.first
        ll.insertbefore(1234, ll.last)
        self.assertIs(ll.first, original_head)

    def test_insertbefore_does_not_update_list_tail(self):
        ll = dllist([0])
        original_tail = ll.last
        ll.insertbefore(1234, ll.last)
        self.assertIs(ll.last, original_tail)

    def test_insertbefore_updates_list_length(self):
        ll = dllist([0])
        self.assertEqual(len(ll), 1)
        ll.insertbefore(1234, ll.first)
        self.assertEqual(len(ll), 2)

    def test_insert_node(self):
        ll = dllist(py23_xrange(4))
        ref = dllist([0, 1, 2, 3, 10])
        prev = ll.nodeat(-1)
        arg_node = dllistnode(10)
        new_node = ll.insertnode(arg_node)
        self.assertEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.prev, prev)
        self.assertEqual(new_node.next, None)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(new_node, ll.last)
        self.assertEqual(ll, ref)

    def test_insert_node_value_before(self):
        ll = dllist(py23_xrange(4))
        ref = dllist([0, 1, 10, 2, 3])
        prev = ll.nodeat(1)
        next = ll.nodeat(2)
        arg_node = dllistnode(10)
        new_node = ll.insertnode(arg_node, ll.nodeat(2))
        self.assertEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.prev, prev)
        self.assertEqual(new_node.next, next)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(next.prev, new_node)
        self.assertEqual(ll, ref)

    def test_insert_node_value_before_first(self):
        ll = dllist(py23_xrange(4))
        ref = dllist([10, 0, 1, 2, 3])
        next = ll.nodeat(0)
        arg_node = dllistnode(10)
        new_node = ll.insertnode(arg_node, ll.nodeat(0))
        self.assertEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.prev, None)
        self.assertEqual(new_node.next, next)
        self.assertEqual(next.prev, new_node)
        self.assertEqual(new_node, ll.first)
        self.assertEqual(ll, ref)

    def test_insert_node_with_bad_argument_type(self):
        ll = dllist([1234])
        self.assertRaises(
            TypeError, ll.insertnode, 'non-node argument', ll.first)

    def test_insert_node_with_already_owned_node(self):
        ll = dllist([1234])
        other_list = dllist([5678])
        self.assertRaises(
            ValueError, ll.insertnode, other_list.first, ll.first)

    def test_insert_node_with_invalid_ref(self):
        ll = dllist()
        self.assertRaises(TypeError, ll.insertnode, dllistnode(10), 1)
        self.assertRaises(TypeError, ll.insertnode, dllistnode(10), 'abc')
        self.assertRaises(TypeError, ll.insertnode, dllistnode(10), [])
        self.assertRaises(
            ValueError, ll.insertnode, dllistnode(10), dllistnode())

    def test_insert_node_refcount_update(self):
        ll = dllist([1234])
        node = ll.insertnode(dllistnode(5678), ll.nodeat(0))
        self.assertGreaterEqual(sys.getrefcount(node), 3)

    def test_append(self):
        ll = dllist(py23_xrange(4))
        ref = dllist([0, 1, 2, 3, 10])
        prev = ll.nodeat(-1)
        arg_node = dllistnode(10)
        new_node = ll.append(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10);
        self.assertEqual(new_node.prev, prev)
        self.assertEqual(new_node.next, None)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(ll.last, new_node)
        self.assertEqual(ll, ref)

    def test_appendleft(self):
        ll = dllist(py23_xrange(4))
        ref = dllist([10, 0, 1, 2, 3])
        next = ll.nodeat(0)
        arg_node = dllistnode(10)
        new_node = ll.appendleft(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10);
        self.assertEqual(new_node.prev, None)
        self.assertEqual(new_node.next, next)
        self.assertEqual(next.prev, new_node)
        self.assertEqual(ll.first, new_node)
        self.assertEqual(ll, ref)

    def test_appendright(self):
        ll = dllist(py23_xrange(4))
        ref = dllist([0, 1, 2, 3, 10])
        prev = ll.nodeat(-1)
        arg_node = dllistnode(10)
        new_node = ll.appendright(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10);
        self.assertEqual(new_node.prev, prev)
        self.assertEqual(new_node.next, None)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(ll.last, new_node)
        self.assertEqual(ll, ref)

    def test_appendnode(self):
        ll = dllist([1, 2, 3, 4])
        node = dllistnode(5)
        ll.appendnode(node)
        self.assertEqual([1, 2, 3, 4, 5], list(ll))
        self.assertIs(node, ll.last)

    def test_appendnode_with_bad_argument_type(self):
        ll = dllist()
        self.assertRaises(TypeError, ll.appendnode, 'non-node argument')

    def test_appendnode_with_already_owned_node(self):
        ll = dllist()
        other_list = dllist([1234])
        self.assertRaises(ValueError, ll.appendnode, other_list.first)

    def test_appendnode_refcount_update(self):
        ll = dllist()
        node = ll.appendnode(dllistnode(1234))
        self.assertGreaterEqual(sys.getrefcount(node), 3)

    def test_extend(self):
        a_ref = py23_range(0, 1024, 4)
        b_ref = py23_range(8092, 8092 + 1024, 4)
        b = dllist(b_ref)
        ab_ref = dllist(a_ref + b_ref)
        a = dllist(a_ref)
        a.extend(b)
        self.assertEqual(a, ab_ref)
        self.assertEqual(len(a), len(ab_ref))
        a = dllist(a_ref)
        a.extend(b_ref)
        self.assertEqual(a, ab_ref)
        self.assertEqual(len(a), len(ab_ref))
        a = dllist(a_ref)
        a.extend(a)
        self.assertEqual(a, dllist(a_ref + a_ref))
        self.assertEqual(len(a), len(a_ref) * 2)

    def test_extend_empty(self):
        filled_ref = py23_range(0, 1024, 4)
        filled = dllist(filled_ref)
        empty = dllist()
        empty.extend(empty)
        self.assertEqual(empty, dllist([] + []))
        self.assertEqual(len(empty), 0)
        empty = dllist()
        empty.extend(filled)
        self.assertEqual(empty, dllist([] + filled_ref))
        self.assertEqual(len(empty), len(filled_ref))
        empty = dllist()
        filled.extend(empty)
        self.assertEqual(filled, dllist(filled_ref + []))
        self.assertEqual(len(filled), len(filled_ref))

    def test_extendleft(self):
        a_ref = py23_range(0, 1024, 4)
        b_ref = py23_range(8092, 8092 + 1024, 4)
        b = dllist(b_ref)
        ab_ref = dllist(list(reversed(b_ref)) + a_ref)
        a = dllist(a_ref)
        a.extendleft(b)
        self.assertEqual(a, ab_ref)
        self.assertEqual(len(a), len(ab_ref))
        a = dllist(a_ref)
        a.extendleft(b_ref)
        self.assertEqual(a, ab_ref)
        self.assertEqual(len(a), len(ab_ref))
        a = dllist(a_ref)
        a.extendleft(a)
        self.assertEqual(a, dllist(list(reversed(a_ref)) + a_ref))
        self.assertEqual(len(a), len(a_ref) * 2)

    def test_extendleft_empty(self):
        filled_ref = py23_range(0, 1024, 4)
        filled = dllist(filled_ref)
        empty = dllist()
        empty.extendleft(empty)
        self.assertEqual(empty, dllist([] + []))
        self.assertEqual(len(empty), 0)
        empty = dllist()
        empty.extendleft(filled)
        self.assertEqual(empty, dllist(list(reversed(filled_ref)) + []))
        self.assertEqual(len(empty), len(filled_ref))
        empty = dllist()
        filled.extendleft(empty)
        self.assertEqual(filled, dllist(list(reversed([])) + filled_ref))
        self.assertEqual(len(filled), len(filled_ref))

    def test_extendright(self):
        a_ref = py23_range(0, 1024, 4)
        b_ref = py23_range(8092, 8092 + 1024, 4)
        b = dllist(b_ref)
        ab_ref = dllist(a_ref + b_ref)
        a = dllist(a_ref)
        a.extendright(b)
        self.assertEqual(a, ab_ref)
        self.assertEqual(len(a), len(ab_ref))
        a = dllist(a_ref)
        a.extendright(b_ref)
        self.assertEqual(a, ab_ref)
        self.assertEqual(len(a), len(ab_ref))
        a = dllist(a_ref)
        a.extendright(a)
        self.assertEqual(a, dllist(a_ref + a_ref))
        self.assertEqual(len(a), len(a_ref) * 2)

    def test_extendright_empty(self):
        filled_ref = py23_range(0, 1024, 4)
        filled = dllist(filled_ref)
        empty = dllist()
        empty.extendright(empty)
        self.assertEqual(empty, dllist([] + []))
        self.assertEqual(len(empty), 0)
        empty = dllist()
        empty.extendright(filled)
        self.assertEqual(empty, dllist([] + filled_ref))
        self.assertEqual(len(empty), len(filled_ref))
        empty = dllist()
        filled.extendright(empty)
        self.assertEqual(filled, dllist(filled_ref + []))
        self.assertEqual(len(filled), len(filled_ref))

    def test_clear_empty(self):
        empty_list = dllist()
        empty_list.clear()
        self.assertEqual(empty_list.first, None)
        self.assertEqual(empty_list.last, None)
        self.assertEqual(empty_list.size, 0)
        self.assertEqual(list(empty_list), [])

    def test_clear(self):
        ll = dllist(py23_xrange(0, 1024, 4))
        del_node = ll.nodeat(4)
        ll.clear()
        self.assertEqual(ll.first, None)
        self.assertEqual(ll.last, None)
        self.assertEqual(ll.size, 0)
        self.assertEqual(list(ll), [])
        self.assertEqual(del_node.prev, None)
        self.assertEqual(del_node.next, None)

    def test_pop(self):
        ref = py23_range(0, 1024, 4)
        ll = dllist(ref)
        result = ll.pop();
        self.assertEqual(result, ref[-1])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.last.value, ref[-2])
        self.assertEqual(list(ll), ref[:-1])

    def test_node_after_pop(self):
        ll = dllist([1, 2])
        del_node = ll.last
        ll.pop()
        self.assertIs(del_node.prev, None)
        self.assertIs(del_node.next, None)
        self.assertIs(del_node.owner, None)

    def test_popleft(self):
        ref = py23_range(0, 1024, 4)
        ll = dllist(ref)
        result = ll.popleft()
        self.assertEqual(result, ref[0])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.first.value, ref[1])
        self.assertEqual(list(ll), ref[1:])

    def test_node_after_popleft(self):
        ll = dllist([1, 2])
        del_node = ll.first
        ll.popleft()
        self.assertIs(del_node.prev, None)
        self.assertIs(del_node.next, None)
        self.assertIs(del_node.owner, None)

    def test_popright(self):
        ref = py23_range(0, 1024, 4)
        ll = dllist(ref)
        result = ll.popright()
        self.assertEqual(result, ref[-1])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.last.value, ref[-2])
        self.assertEqual(list(ll), ref[:-1])

    def test_node_after_popright(self):
        ll = dllist([1, 2])
        del_node = ll.last
        ll.popright()
        self.assertIs(del_node.prev, None)
        self.assertIs(del_node.next, None)
        self.assertIs(del_node.owner, None)

    def test_pop_from_empty_list(self):
        ll = dllist()
        self.assertRaises(ValueError, ll.pop)
        self.assertRaises(ValueError, ll.popleft)
        self.assertRaises(ValueError, ll.popright)

    def test_remove(self):
        ref = py23_range(0, 1024, 4)
        ll = dllist(ref)
        prev_node = ll.nodeat(3)
        del_node = ll.nodeat(4)
        next_node = ll.nodeat(5)
        result = ll.remove(del_node)
        ref_result = ref[4]
        del ref[4]
        self.assertEqual(list(ll), ref)
        self.assertEqual(result, ref_result)
        self.assertEqual(len(ll), len(ref))
        self.assertEqual(ll.size, len(ref))
        self.assertEqual(prev_node.next, next_node)
        self.assertEqual(next_node.prev, prev_node)

    def test_remove_after_remove(self):
        ll = dllist([1, 2, 3])
        del_node = ll.nodeat(1)
        ll.remove(del_node)
        self.assertIs(del_node.prev, None)
        self.assertIs(del_node.next, None)
        self.assertIs(del_node.owner, None)

    def test_remove_from_empty_list(self):
        ll = dllist()
        self.assertRaises(ValueError, ll.remove, dllistnode())

    def test_remove_invalid_node(self):
        ll = dllist([1, 2, 3, 4])
        self.assertRaises(ValueError, ll.remove, dllistnode())
        self.assertEqual(len(ll), 4)

    def test_remove_already_deleted_node(self):
        ll = dllist([1, 2, 3, 4])
        node = ll.nodeat(2)
        ll.remove(node)
        self.assertRaises(ValueError, ll.remove, node)

    def test_rotate_left(self):
        for n in py23_xrange(128):
            ref = py23_range(32)
            split = n % len(ref)
            ref_result = ref[split:] + ref[:split]
            ll = dllist(ref)
            new_first = ll.nodeat(split)
            new_last = ll.nodeat(split - 1)
            # touch future middle element to initialize cache
            cached_idx = (len(ll) // 2 + n) % len(ll)
            ll[cached_idx]
            ll.rotate(-n)
            self.assertEqual(list(ll), ref_result)
            self.assertEqual(ll.first, new_first)
            self.assertEqual(ll.last, new_last)
            self.assertEqual(ll.size, len(ref))
            self.assertEqual(ll.first.prev, None)
            self.assertEqual(ll.first.next.prev, ll.first)
            self.assertEqual(ll.last.next, None)
            self.assertEqual(ll.last.prev.next, ll.last)
            # check if cached index is updated correctly
            self.assertEqual(ll[len(ll) // 2], ref_result[len(ref_result) // 2])

    def test_rotate_right(self):
        for n in py23_xrange(128):
            ref = py23_range(32)
            split = n % len(ref)
            ref_result = ref[-split:] + ref[:-split]
            ll = dllist(ref)
            new_first = ll.nodeat(-split)
            last_idx = -split - 1
            new_last = ll.nodeat(last_idx)
            # touch future middle element to initialize cache
            cached_idx = len(ll) - (len(ll) // 2 + n) % len(ll) - 1
            ll[cached_idx]
            ll.rotate(n)
            self.assertEqual(list(ll), ref_result)
            self.assertEqual(ll.first, new_first)
            self.assertEqual(ll.last, new_last)
            self.assertEqual(ll.size, len(ref))
            self.assertEqual(ll.first.prev, None)
            self.assertEqual(ll.first.next.prev, ll.first)
            self.assertEqual(ll.last.next, None)
            self.assertEqual(ll.last.prev.next, ll.last)
            # check if cached index is updated correctly
            self.assertEqual(ll[len(ll) // 2], ref_result[len(ref_result) // 2])

    def test_rotate_left_empty(self):
        for n in py23_xrange(4):
            ll = dllist()
            ll.rotate(-n)
            self.assertEqual(ll.first, None)
            self.assertEqual(ll.last, None)
            self.assertEqual(ll.size, 0)

    def test_rotate_right_empty(self):
        for n in py23_xrange(4):
            ll = dllist()
            ll.rotate(n)
            self.assertEqual(ll.first, None)
            self.assertEqual(ll.last, None)
            self.assertEqual(ll.size, 0)

    def test_getitem(self):
        ref = py23_range(0, 1024, 4)
        ll = dllist(ref)
        for idx in py23_xrange(len(ll)):
            self.assertFalse(isinstance(ll[idx], dllistnode))
            self.assertEqual(ll[idx], ref[idx])
        for idx in py23_xrange(len(ll)):
            self.assertFalse(isinstance(ll[idx], dllistnode))
            self.assertEqual(ll[-idx - 1], ref[-idx - 1])
        self.assertRaises(TypeError, ll.__getitem__, None)
        self.assertRaises(TypeError, ll.__getitem__, 'abc')
        self.assertRaises(IndexError, ll.__getitem__, len(ref))
        self.assertRaises(IndexError, ll.__getitem__, -len(ref) - 1)

    def test_getitem_empty(self):
        ll = dllist()
        self.assertRaises(TypeError, ll.__getitem__, None)
        self.assertRaises(TypeError, ll.__getitem__, 'abc')
        self.assertRaises(IndexError, ll.__getitem__, 0)
        self.assertRaises(IndexError, ll.__getitem__, -1)

    def test_del(self):
        ref = py23_range(0, 1024, 4)
        ll = dllist(ref)
        del ll[0]
        del ref[0]
        self.assertEqual(list(ll), ref)
        del ll[len(ll) - 1]
        del ref[len(ref) - 1]
        self.assertEqual(list(ll), ref)
        del ll[(len(ll) - 1) // 2]
        del ref[(len(ref) - 1) // 2]
        self.assertEqual(list(ll), ref)

        def del_item(idx):
            del ll[idx]
        self.assertRaises(IndexError, del_item, len(ll))

        for i in py23_xrange(len(ll)):
            del ll[0]
        self.assertEqual(len(ll), 0)

    def test_node_after_del(self):
        ll = dllist([1, 2, 3])
        del_node = ll.nodeat(1)
        del ll[1]
        self.assertIs(del_node.prev, None)
        self.assertIs(del_node.next, None)
        self.assertIs(del_node.owner, None)

    def test_concat(self):
        a_ref = py23_range(0, 1024, 4)
        a = dllist(a_ref)
        b_ref = py23_range(8092, 8092 + 1024, 4)
        b = dllist(b_ref)
        ab_ref = dllist(a_ref + b_ref)
        c = a + b
        self.assertEqual(c, ab_ref)
        self.assertEqual(len(c), len(ab_ref))
        c = a + b_ref
        self.assertEqual(c, ab_ref)
        self.assertEqual(len(c), len(a_ref) * 2)

    def test_concat_empty(self):
        empty = dllist()
        filled_ref = py23_range(0, 1024, 4)
        filled = dllist(filled_ref)
        res = empty + empty
        self.assertEqual(res, dllist([] + []))
        self.assertEqual(len(res), 0)
        res = empty + filled
        self.assertEqual(res, dllist([] + filled_ref))
        self.assertEqual(len(res), len(filled_ref))
        res = filled + empty
        self.assertEqual(res, dllist(filled_ref + []))
        self.assertEqual(len(res), len(filled_ref))

    def test_concat_inplace(self):
        a_ref = py23_range(0, 1024, 4)
        b_ref = py23_range(8092, 8092 + 1024, 4)
        b = dllist(b_ref)
        ab_ref = dllist(a_ref + b_ref)
        a = dllist(a_ref)
        a += b
        self.assertEqual(a, ab_ref)
        self.assertEqual(len(a), len(ab_ref))
        a = dllist(a_ref)
        a += b_ref
        self.assertEqual(a, ab_ref)
        self.assertEqual(len(a), len(ab_ref))
        a = dllist(a_ref)
        a += a
        self.assertEqual(a, dllist(a_ref + a_ref))
        self.assertEqual(len(a), len(a_ref) * 2)

    def test_concat_inplace_empty(self):
        filled_ref = py23_range(0, 1024, 4)
        filled = dllist(filled_ref)
        empty = dllist()
        empty += empty
        self.assertEqual(empty, dllist([] + []))
        self.assertEqual(len(empty), 0)
        empty = dllist()
        empty += filled
        self.assertEqual(empty, dllist([] + filled_ref))
        self.assertEqual(len(empty), len(filled_ref))
        empty = dllist()
        filled += empty
        self.assertEqual(filled, dllist(filled_ref + []))
        self.assertEqual(len(filled), len(filled_ref))

    def test_repeat(self):
        ref = py23_range(0, 1024, 4)
        ll = dllist(ref)
        self.assertEqual(ll * 4, dllist(ref * 4))

    def test_repeat_empty(self):
        ll = dllist()
        self.assertEqual(ll * 4, dllist([] * 4))

    def test_repeat_inplace(self):
        ref = py23_range(0, 1024, 4)
        ll = dllist(ref)
        ll *= 4
        self.assertEqual(ll, dllist(ref * 4))

    def test_repeat_inplace_empty(self):
        ll = dllist()
        ll *= 4
        self.assertEqual(ll, dllist([] * 4))

    def test_list_readonly_attributes(self):
        if sys.hexversion >= 0x03000000:
            expected_error = AttributeError
        else:
            expected_error = TypeError

        ll = dllist(py23_range(4))
        self.assertRaises(expected_error, setattr, ll, 'first', None)
        self.assertRaises(expected_error, setattr, ll, 'last', None)
        self.assertRaises(expected_error, setattr, ll, 'size', None)

    def test_node_readonly_attributes(self):
        if sys.hexversion >= 0x03000000:
            expected_error = AttributeError
        else:
            expected_error = TypeError

        ll = dllistnode()
        self.assertRaises(expected_error, setattr, ll, 'prev', None)
        self.assertRaises(expected_error, setattr, ll, 'next', None)

    def test_node_owner(self):
        ll = dllist([1234])
        owner_ref = ll.first.owner
        self.assertIsInstance(owner_ref, weakref.ref)
        self.assertIs(owner_ref(), ll)
        del ll
        self.assertIsNone(owner_ref())

    def test_list_hash(self):
        self.assertEqual(hash(dllist()), hash(dllist()))
        self.assertEqual(hash(dllist(py23_range(0, 1024, 4))),
            hash(dllist(py23_range(0, 1024, 4))))
        self.assertEqual(hash(dllist([0, 2])), hash(dllist([0.0, 2.0])))
        self.assertNotEqual(hash(sllist([1, 2])), hash(sllist([2, 1])))

    def test_list_can_be_subclassed(self):
        class DerivedList(dllist):
            pass

    def test_list_node_can_be_subclassed(self):
        class DerivedNode(dllistnode):
            pass

    def test_cyclic_list_destruction_does_not_release_extra_None_refs(self):
        original_ref_count = sys.getrefcount(None)

        for _ in range(original_ref_count * 10):
            ll = dllist()
            ll.append(dllistnode(ll))
            del ll

        self.assertGreater(sys.getrefcount(None), 0)

    def test_cyclic_node_destruction_does_not_release_extra_None_refs(self):
        original_ref_count = sys.getrefcount(None)

        for _ in range(original_ref_count * 10):
            ll = self.make_recursive_node_list()
            del ll

        self.assertGreater(sys.getrefcount(None), 0)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testsllist))
    suite.addTest(unittest.makeSuite(testdllist))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
