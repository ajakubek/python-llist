#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gc
import sys
import unittest


class LListTestCase(unittest.TestCase):

    def assertStableRefCount(self, callable, object):
        gc.collect()
        original_ref_count = sys.getrefcount(None)

        callable()

        gc.collect()
        new_ref_count = sys.getrefcount(None)
        self.assertEqual(new_ref_count, original_ref_count)
