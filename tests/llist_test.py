#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gc
import unittest
from llist import sllist
from llist import sllistnode
from llist import dllist
from llist import dllistnode

gc.set_debug(gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_STATS)

class testsllist(unittest.TestCase):

    def test_init_empty(self):
        ll = sllist()
        self.assertEqual(len(ll), 0)
        self.assertEqual(ll.size, 0)
        self.assertEqual(list(ll), [])

    def test_init_with_sequence(self):
        ref = range(0, 1024, 4)
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

    def test_cmp(self):
        a = sllist(xrange(0, 1100))
        b = sllist(xrange(0, 1101))
        c = [xrange(0, 1100)]
        self.assertEqual(cmp(a, a), 0)
        self.assertEqual(cmp(a, b), -1)
        self.assertEqual(cmp(b, a), 1)
        self.assertEqual(cmp(a, c), 1)
        self.assertEqual(cmp(c, a), -1)
        self.assertEqual(cmp([], []), 0)
        self.assertEqual(cmp([], a), -1)
        self.assertEqual(cmp(a, []), 1)

    def test_nodeat(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        for idx in xrange(len(ll)):
            self.assertTrue(isinstance(ll.nodeat(idx), sllistnode))
            self.assertEqual(ll.nodeat(idx).value, ref[idx])
        for idx in xrange(len(ll)):
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
        ref = range(0, 1024, 4)
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

    def test_reversed(self):
        ref = range(0, 1024, 4)
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
        self.assertTrue([5, 1, 2, 3, 4], list(ll))

    def test_append_right(self):
        ll = sllist([1, 2, 3, 4])
        ll.appendleft(5)
        self.assertTrue([1, 2, 3, 4, 5], list(ll))

    def test_pop_left_from_one_elem(self):
        ll = sllist(xrange(0, 100))
        dd = ll.popleft()
        self.assertEqual(dd, 0)

    def test_pop_right_from_one_elem(self):
        ll = sllist(xrange(0, 100))
        dd = ll.popright()
        self.assertEqual(dd, 99)

    def test_pop_right_from_n_elem(self):
        ll = sllist(xrange(0, 100))
        dd = ll.popright()
        self.assertEqual(dd, 99)

    def test_get_node_at_from_n_elem(self):
        ll = sllist(xrange(0, 100))
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
        ll = sllist(xrange(4))
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
        ll = sllist(xrange(4))
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
        ll = sllist(xrange(4))
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
        ll = sllist(xrange(4))
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

    def test_append(self):
        ll = sllist(xrange(4))
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
        ll = sllist(xrange(4))
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
        ll = sllist(xrange(4))
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
        a_ref = range(0, 1024, 4)
        b_ref = range(8092, 8092 + 1024, 4)
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
        filled_ref = range(0, 1024, 4)
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
        a_ref = range(0, 1024, 4)
        b_ref = range(8092, 8092 + 1024, 4)
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
        filled_ref = range(0, 1024, 4)
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
        a_ref = range(0, 1024, 4)
        b_ref = range(8092, 8092 + 1024, 4)
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
        filled_ref = range(0, 1024, 4)
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
        ll = sllist(xrange(0, 1024, 4))
        del_node = ll.nodeat(4)
        ll.clear()
        self.assertEqual(ll.first, None)
        self.assertEqual(ll.last, None)
        self.assertEqual(ll.size, 0)
        self.assertEqual(list(ll), [])
        self.assertEqual(del_node.next, None)

    def test_pop(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        del_node = ll.nodeat(-1)
        result = ll.pop()
        self.assertEqual(result, ref[-1])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.last.value, ref[-2])
        self.assertEqual(list(ll), ref[:-1])
        self.assertEqual(del_node.next, None)

    def test_popleft(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        del_node = ll.nodeat(0)
        result = ll.popleft()
        self.assertEqual(result, ref[0])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.first.value, ref[1])
        self.assertEqual(list(ll), ref[1:])
        self.assertEqual(del_node.next, None)

    def test_popright(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        del_node = ll.nodeat(-1)
        result = ll.popright()
        self.assertEqual(result, ref[-1])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.last.value, ref[-2])
        self.assertEqual(list(ll), ref[:-1])
        self.assertEqual(del_node.next, None)

    def test_pop_from_empty_list(self):
        ll = sllist()
        self.assertRaises(ValueError, ll.pop)
        self.assertRaises(ValueError, ll.popleft)
        self.assertRaises(ValueError, ll.popright)

    def test_remove(self):
        ref = range(0, 1024, 4)
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
        self.assertEqual(del_node.next, None)

    def test_remove_from_empty_list(self):
        ll = sllist()
        self.assertRaises(ValueError, ll.remove, sllistnode())

    def test_remove_invalid_node(self):
        ll = sllist([1, 2, 3, 4])
        self.assertRaises(ValueError, ll.remove, sllistnode())

    def test_remove_already_deleted_node(self):
        ll = sllist([1, 2, 3, 4])
        node = ll.nodeat(2)
        ll.remove(node)
        self.assertRaises(ValueError, ll.remove, node)

    def test_rotate_left(self):
        for n in xrange(128):
            ref = range(32)
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
        for n in xrange(128):
            ref = range(32)
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
        for n in xrange(4):
            ll = sllist()
            ll.rotate(-n)
            self.assertEqual(ll.first, None)
            self.assertEqual(ll.last, None)
            self.assertEqual(ll.size, 0)

    def test_rotate_right_empty(self):
        for n in xrange(4):
            ll = sllist()
            ll.rotate(n)
            self.assertEqual(ll.first, None)
            self.assertEqual(ll.last, None)
            self.assertEqual(ll.size, 0)

    def test_getitem(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        for idx in xrange(len(ll)):
            self.assertFalse(isinstance(ll[idx], sllistnode))
            self.assertEqual(ll[idx], ref[idx])
        for idx in xrange(len(ll)):
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
        ref = range(0, 1024, 4)
        ll = sllist(ref)
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

    def test_concat(self):
        a_ref = range(0, 1024, 4)
        a = sllist(a_ref)
        b_ref = range(8092, 8092 + 1024, 4)
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
        filled_ref = range(0, 1024, 4)
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
        a_ref = range(0, 1024, 4)
        b_ref = range(8092, 8092 + 1024, 4)
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
        filled_ref = range(0, 1024, 4)
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
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        self.assertEqual(ll * 4, sllist(ref * 4))

    def test_repeat_empty(self):
        ll = sllist()
        self.assertEqual(ll * 4, sllist([] * 4))

    def test_repeat_inplace(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        ll *= 4
        self.assertEqual(ll, sllist(ref * 4))

    def test_repeat_inplace_empty(self):
        ll = sllist()
        ll *= 4
        self.assertEqual(ll, sllist([] * 4))

    def test_list_readonly_attributes(self):
        ll = sllist(range(4))
        self.assertRaises(TypeError, setattr, ll, 'first', None)
        self.assertRaises(TypeError, setattr, ll, 'last', None)
        self.assertRaises(TypeError, setattr, ll, 'size', None)

    def test_node_readonly_attributes(self):
        ll = sllistnode()
        self.assertRaises(TypeError, setattr, ll, 'next', None)

    def test_list_hash(self):
        self.assertEqual(hash(sllist()), hash(sllist()))
        self.assertEqual(hash(sllist(range(0, 1024, 4))),
            hash(sllist(range(0, 1024, 4))))
        self.assertEqual(hash(sllist([0, 2])), hash(sllist([0.0, 2.0])))


class testdllist(unittest.TestCase):

    def test_init_empty(self):
        ll = dllist()
        self.assertEqual(len(ll), 0)
        self.assertEqual(ll.size, 0)
        self.assertEqual(list(ll), [])

    def test_init_with_sequence(self):
        ref = range(0, 1024, 4)
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

    def test_cmp(self):
        a = dllist(xrange(0, 1100))
        b = dllist(xrange(0, 1101))
        c = [xrange(0, 1100)]
        self.assertEqual(cmp(a, a), 0)
        self.assertEqual(cmp(a, b), -1)
        self.assertEqual(cmp(b, a), 1)
        self.assertEqual(cmp(a, c), 1)
        self.assertEqual(cmp(c, a), -1)
        self.assertEqual(cmp([], []), 0)
        self.assertEqual(cmp([], a), -1)
        self.assertEqual(cmp(a, []), 1)

    def test_nodeat(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        for idx in xrange(len(ll)):
            self.assertTrue(isinstance(ll.nodeat(idx), dllistnode))
            self.assertEqual(ll.nodeat(idx).value, ref[idx])
        for idx in xrange(len(ll)):
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
        ref = range(0, 1024, 4)
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

    def test_reversed(self):
        ref = range(0, 1024, 4)
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
        ll = dllist(xrange(4))
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
        ll = dllist(xrange(4))
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
        ll = dllist(xrange(4))
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

    def test_append(self):
        ll = dllist(xrange(4))
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
        ll = dllist(xrange(4))
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
        ll = dllist(xrange(4))
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

    def test_extend(self):
        a_ref = range(0, 1024, 4)
        b_ref = range(8092, 8092 + 1024, 4)
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
        filled_ref = range(0, 1024, 4)
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
        a_ref = range(0, 1024, 4)
        b_ref = range(8092, 8092 + 1024, 4)
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
        filled_ref = range(0, 1024, 4)
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
        a_ref = range(0, 1024, 4)
        b_ref = range(8092, 8092 + 1024, 4)
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
        filled_ref = range(0, 1024, 4)
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
        ll = dllist(xrange(0, 1024, 4))
        del_node = ll.nodeat(4)
        ll.clear()
        self.assertEqual(ll.first, None)
        self.assertEqual(ll.last, None)
        self.assertEqual(ll.size, 0)
        self.assertEqual(list(ll), [])
        self.assertEqual(del_node.prev, None)
        self.assertEqual(del_node.next, None)

    def test_pop(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        del_node = ll.nodeat(-1)
        result = ll.pop();
        self.assertEqual(result, ref[-1])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.last.value, ref[-2])
        self.assertEqual(list(ll), ref[:-1])
        self.assertEqual(del_node.prev, None)
        self.assertEqual(del_node.next, None)

    def test_popleft(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        del_node = ll.nodeat(0)
        result = ll.popleft()
        self.assertEqual(result, ref[0])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.first.value, ref[1])
        self.assertEqual(list(ll), ref[1:])
        self.assertEqual(del_node.prev, None)
        self.assertEqual(del_node.next, None)

    def test_popright(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        del_node = ll.nodeat(-1)
        result = ll.popright()
        self.assertEqual(result, ref[-1])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.last.value, ref[-2])
        self.assertEqual(list(ll), ref[:-1])
        self.assertEqual(del_node.prev, None)
        self.assertEqual(del_node.next, None)

    def test_pop_from_empty_list(self):
        ll = dllist()
        self.assertRaises(ValueError, ll.pop)
        self.assertRaises(ValueError, ll.popleft)
        self.assertRaises(ValueError, ll.popright)

    def test_remove(self):
        ref = range(0, 1024, 4)
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
        self.assertEqual(del_node.prev, None)
        self.assertEqual(del_node.next, None)

    def test_remove_from_empty_list(self):
        ll = dllist()
        self.assertRaises(ValueError, ll.remove, dllistnode())

    def test_remove_invalid_node(self):
        ll = dllist([1, 2, 3, 4])
        self.assertRaises(ValueError, ll.remove, dllistnode())

    def test_remove_already_deleted_node(self):
        ll = dllist([1, 2, 3, 4])
        node = ll.nodeat(2)
        ll.remove(node)
        self.assertRaises(ValueError, ll.remove, node)

    def test_rotate_left(self):
        for n in xrange(128):
            ref = range(32)
            split = n % len(ref)
            ref_result = ref[split:] + ref[:split]
            ll = dllist(ref)
            new_first = ll.nodeat(split)
            new_last = ll.nodeat(split - 1)
            # touch future middle element to initialize cache
            cached_idx = (len(ll) / 2 + n) % len(ll)
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
            self.assertEqual(ll[len(ll) / 2], ref_result[len(ref_result) / 2])

    def test_rotate_right(self):
        for n in xrange(128):
            ref = range(32)
            split = n % len(ref)
            ref_result = ref[-split:] + ref[:-split]
            ll = dllist(ref)
            new_first = ll.nodeat(-split)
            last_idx = -split - 1
            new_last = ll.nodeat(last_idx)
            # touch future middle element to initialize cache
            cached_idx = len(ll) - (len(ll) / 2 + n) % len(ll) - 1
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
            self.assertEqual(ll[len(ll) / 2], ref_result[len(ref_result) / 2])

    def test_rotate_left_empty(self):
        for n in xrange(4):
            ll = dllist()
            ll.rotate(-n)
            self.assertEqual(ll.first, None)
            self.assertEqual(ll.last, None)
            self.assertEqual(ll.size, 0)

    def test_rotate_right_empty(self):
        for n in xrange(4):
            ll = dllist()
            ll.rotate(n)
            self.assertEqual(ll.first, None)
            self.assertEqual(ll.last, None)
            self.assertEqual(ll.size, 0)

    def test_getitem(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        for idx in xrange(len(ll)):
            self.assertFalse(isinstance(ll[idx], dllistnode))
            self.assertEqual(ll[idx], ref[idx])
        for idx in xrange(len(ll)):
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
        ref = range(0, 1024, 4)
        ll = dllist(ref)
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

    def test_concat(self):
        a_ref = range(0, 1024, 4)
        a = dllist(a_ref)
        b_ref = range(8092, 8092 + 1024, 4)
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
        filled_ref = range(0, 1024, 4)
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
        a_ref = range(0, 1024, 4)
        b_ref = range(8092, 8092 + 1024, 4)
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
        filled_ref = range(0, 1024, 4)
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
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        self.assertEqual(ll * 4, dllist(ref * 4))

    def test_repeat_empty(self):
        ll = dllist()
        self.assertEqual(ll * 4, dllist([] * 4))

    def test_repeat_inplace(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        ll *= 4
        self.assertEqual(ll, dllist(ref * 4))

    def test_repeat_inplace_empty(self):
        ll = dllist()
        ll *= 4
        self.assertEqual(ll, dllist([] * 4))

    def test_list_readonly_attributes(self):
        ll = dllist(range(4))
        self.assertRaises(TypeError, setattr, ll, 'first', None)
        self.assertRaises(TypeError, setattr, ll, 'last', None)
        self.assertRaises(TypeError, setattr, ll, 'size', None)

    def test_node_readonly_attributes(self):
        ll = dllistnode()
        self.assertRaises(TypeError, setattr, ll, 'prev', None)
        self.assertRaises(TypeError, setattr, ll, 'next', None)

    def test_list_hash(self):
        self.assertEqual(hash(dllist()), hash(dllist()))
        self.assertEqual(hash(dllist(range(0, 1024, 4))),
            hash(dllist(range(0, 1024, 4))))
        self.assertEqual(hash(dllist([0, 2])), hash(dllist([0.0, 2.0])))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testsllist))
    suite.addTest(unittest.makeSuite(testdllist))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
