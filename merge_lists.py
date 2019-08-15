"""
Written by Henry George, August 2019, in Python 3.7
"""

import unittest
from typing import Callable, List, TypeVar
import functools

T = TypeVar('T')


def merge_lists(a: List[T], b: List[T], key: Callable = lambda x: x) -> List[T]:
    """Merge two sorted lists

    The two lists must have homogeneous types and be sorted with the same ordering, and this ordering must match that of the key.

    Args:
        a: A sorted list
        b: Another sorted list with the same sorting order
        key: The ordering key, this should return any type which provides comparison methods.

    Returns:
        A sorted list containing all the elements of lists a and b.

    """
    if len(a) == 0:
        return b
    if len(b) == 0:
        return a
    if key(b[-1]) > key(a[-1]):
        # this ensures the final element is from list a.
        a, b = b, a
    merged: List[T] = []
    comparison_index = 0
    for index in range(len(a)):
        while comparison_index < len(b) and key(b[comparison_index]) < key(a[index]):
            merged.append(b[comparison_index])
            comparison_index += 1
        merged.append(a[index])
    return merged


class TestListMerging(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_both_lists_empty(self):
        self.assertEqual([], merge_lists([], []))

    def test_one_list_empty(self):
        a = [1, 2, 3]
        b = []
        self.assertEqual(a, merge_lists(a, b))

    def test_string_lists(self):
        a = ['a', 'b', 'ba', 'bc']
        b = ['ab', 'bb']
        self.assertEqual(['a', 'ab', 'b', 'ba', 'bb', 'bc'], merge_lists(a, b))

    def test_custom_ordering_key(self):
        key = lambda x: -x
        a = [5, 3, 1]
        b = [4, 2, 0, -1]
        self.assertEqual(list(range(5, -2, -1)), merge_lists(a, b, key=key))

    def test_custom_class_with_default_ordering(self):

        @functools.total_ordering
        class Item:
            def __init__(self, value):
                self.value = value

            def __gt__(self, other):
                return self.value > other.value

            def __eq__(self, other):
                return self.value == other.value

        a = [Item(1), Item(3), Item(5)]
        b = [Item(2), Item(4)]
        merged = [Item(i) for i in range(1, 6)]
        self.assertEqual(merged, merge_lists(a, b))

    def test_custom_class_with_custom_ordering(self):

        class ItemSimple:
            def __init__(self, value):
                self.value = value

            def __eq__(self, other):
                return self.value == other.value

        a = [ItemSimple(1), ItemSimple(3), ItemSimple(5)]
        b = [ItemSimple(2), ItemSimple(4)]
        merged = [ItemSimple(i) for i in range(1, 6)]
        self.assertEqual(merged, merge_lists(a, b, key=lambda x: x.value))