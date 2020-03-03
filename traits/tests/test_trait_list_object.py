# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import copy
import pickle
import unittest

from traits.trait_base import Undefined
from traits.trait_list_object import TraitList
from traits.trait_types import _validate_int


def int_validator(trait_list, index, removed, value):
    if isinstance(index, slice):
        return [_validate_int(item) for item in value]
    else:
        if value is Undefined:
            return Undefined
        return _validate_int(value)


class TestTraitList(unittest.TestCase):

    def setUp(self):
        self.index = None
        self.added = None
        self.removed = None
        self.trait_list = None

    def notification_handler(self, trait_list, index, removed, added):
        self.trait_list = trait_list
        self.index = index
        self.removed = removed
        self.added = added

    def test_init(self):
        tl = TraitList([1, 2, 3])

        self.assertListEqual(tl, [1, 2, 3])
        self.assertIsNone(tl.validator)
        self.assertEqual(tl.notifiers, [])

    def test_validator(self):
        tl = TraitList([1, 2, 3], validator=int_validator)

        self.assertListEqual(tl, [1, 2, 3])
        self.assertEqual(tl.validator, int_validator)
        self.assertEqual(tl.notifiers, [])

    def test_notification(self):
        tl = TraitList([1, 2, 3], notifiers=[self.notification_handler])

        self.assertListEqual(tl, [1, 2, 3])
        self.assertIsNone(tl.validator)
        self.assertEqual(tl.notifiers, [self.notification_handler])

        tl[0] = 5

        self.assertListEqual(tl, [5, 2, 3])
        self.assertIs(self.trait_list, tl)
        self.assertEqual(self.index, 0)
        self.assertEqual(self.removed, 1)
        self.assertEqual(self.added, 5)

    def test_deepcopy(self):
        tl = TraitList([1, 2, 3],
                       validator=int_validator,
                       notifiers=[self.notification_handler])

        tl_copy = copy.deepcopy(tl)

        for itm, itm_cpy in zip(tl, tl_copy):
            self.assertEqual(itm, itm_cpy)

        self.assertEqual([], tl_copy.notifiers)
        self.assertEqual(tl.validator, tl_copy.validator)

    def test_setitem(self):
        tl = TraitList([1, 2, 3],
                       validator=int_validator,
                       notifiers=[self.notification_handler])

        tl[1] = 5
        self.assertEqual(self.index, 1)
        self.assertEqual(self.removed, 2)
        self.assertEqual(self.added, 5)

        tl[:] = [1, 2, 3, 4, 5]
        self.assertEqual(slice(0, 3, None), self.index)
        self.assertEqual([1, 5, 3], self.removed)
        self.assertEqual([1, 2, 3, 4, 5], self.added)

    def test_delitem(self):
        tl = TraitList([1, 2, 3],
                       validator=int_validator,
                       notifiers=[self.notification_handler])

        del tl[2]
        self.assertEqual(2, self.index)
        self.assertEqual(3, self.removed)
        self.assertEqual(Undefined, self.added)

        del tl[:]

        with self.assertRaises(IndexError):
            del tl[0]

    def test_iadd(self):
        tl = TraitList([4, 5],
                       validator=int_validator,
                       notifiers=[self.notification_handler])

        tl += [6, 7]
        self.assertEqual(slice(2, 4, None), self.index)
        self.assertEqual([], self.removed)
        self.assertEqual([6, 7], self.added)

    def test_imul(self):
        tl = TraitList([1, 2],
                       validator=int_validator,
                       notifiers=[self.notification_handler])

        tl *= 2
        self.assertEqual(slice(2, 4, None), self.index)
        self.assertEqual([], self.removed)
        self.assertEqual([1, 2], self.added)

        with self.assertRaises(TypeError):
            tl *= 2.5

        tl *= 0
        self.assertEqual(slice(0, 4, None), self.index)
        self.assertEqual([1, 2, 1, 2], self.removed)
        self.assertEqual([], self.added)

    def test_append(self):
        tl = TraitList([1],
                       validator=int_validator,
                       notifiers=[self.notification_handler])

        tl.append(2)
        self.assertEqual(1, self.index)
        self.assertEqual(Undefined, self.removed)
        self.assertEqual(2, self.added)

    def test_extend(self):
        tl = TraitList([1],
                       validator=int_validator,
                       notifiers=[self.notification_handler])

        tl.extend([2])
        self.assertEqual(slice(1, 2, None), self.index)
        self.assertEqual([], self.removed)
        self.assertEqual([2], self.added)

    def test_insert(self):
        tl = TraitList([2],
                       validator=int_validator,
                       notifiers=[self.notification_handler])

        tl.insert(0, 1)  # [1,2]
        self.assertEqual(0, self.index)
        self.assertEqual(Undefined, self.removed)
        self.assertEqual(1, self.added)

        tl.insert(-1, 3)  # [1,3,2]
        self.assertEqual(1, self.index)
        self.assertEqual(Undefined, self.removed)
        self.assertEqual(3, self.added)

    def test_pop(self):
        tl = TraitList([1, 2, 3, 4, 5],
                       validator=int_validator,
                       notifiers=[self.notification_handler])

        tl.pop()
        self.assertEqual(4, self.index)
        self.assertEqual(5, self.removed)
        self.assertEqual(Undefined, self.added)

        tl.pop(0)
        self.assertEqual(0, self.index)
        self.assertEqual(1, self.removed)
        self.assertEqual(Undefined, self.added)

        # tl is now [2,3,4]
        tl.pop(-2)
        self.assertEqual(1, self.index)
        self.assertEqual(3, self.removed)
        self.assertEqual(Undefined, self.added)

    def test_remove(self):
        tl = TraitList([1, 2, 3, 4, 5],
                       validator=int_validator,
                       notifiers=[self.notification_handler])

        tl.remove(3)
        self.assertEqual(2, self.index)
        self.assertEqual(3, self.removed)
        self.assertEqual(Undefined, self.added)

        with self.assertRaises(ValueError):
            tl.remove(3)

    def test_clear(self):
        tl = TraitList([1, 2, 3, 4, 5],
                       validator=int_validator,
                       notifiers=[self.notification_handler])
        tl.clear()
        self.assertEqual(slice(0, 5, None), self.index)
        self.assertEqual([1, 2, 3, 4, 5], self.removed)
        self.assertEqual([], self.added)

    def test_sort(self):
        tl = TraitList([2, 3, 1, 4, 5, 0],
                       validator=int_validator,
                       notifiers=[self.notification_handler])

        tl.sort()

        self.assertEqual([0, 1, 2, 3, 4, 5], tl)
        self.assertEqual(slice(0, 6, None), self.index)
        self.assertEqual(Undefined, self.removed)
        self.assertEqual([], self.added)

    def test_reverse(self):
        tl = TraitList([1, 2, 3, 4, 5],
                       validator=int_validator,
                       notifiers=[self.notification_handler])

        tl.reverse()
        self.assertEqual([5, 4, 3, 2, 1], tl)
        self.assertEqual(slice(0, 5, None), self.index)
        self.assertEqual(Undefined, self.removed)
        self.assertEqual([], self.added)

    def test_pickle(self):
        tl = TraitList([1, 2, 3, 4, 5],
                       validator=int_validator,
                       notifiers=[self.notification_handler])
        serialized = pickle.dumps(tl)

        tl_unpickled = pickle.loads(serialized)

        self.assertIs(tl_unpickled.validator, tl.validator)
        self.assertEqual([], tl_unpickled.notifiers)

        for i, j in zip(tl, tl_unpickled):
            self.assertIs(i, j)

    def test_invalid_entry(self):
        tl = TraitList([1, 2, 3, 4, 5],
                       validator=int_validator,
                       notifiers=[self.notification_handler])

        with self.assertRaises(TypeError):
            tl.append("A")