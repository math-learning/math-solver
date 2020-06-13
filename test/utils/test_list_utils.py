import unittest
from mathlearning.utils.list.list_utils import ListUtils


class TestListUtils(unittest.TestCase):

    def test_combinations_size_two(self):
        lista = [1, 2]
        listb = [3, 4]
        expected_result = [
            [[1, 3], [2, 4]],
            [[1, 4], [2, 3]],
        ]
        combinations = ListUtils.pair_combinations(lista, listb)
        self.assertEqual(combinations, expected_result)

    def test_combinations_size_three(self):
        lista = [1, 2, 3]
        listb = [4, 5, 6]
        expected_result = [
            [[1, 4], [2, 5], [3, 6]],
            [[1, 4], [2, 6], [3, 5]],
            [[1, 5], [2, 4], [3, 6]],
            [[1, 5], [2, 6], [3, 4]],
            [[1, 6], [2, 4], [3, 5]],
            [[1, 6], [2, 5], [3, 4]]
        ]
        combinations = ListUtils.pair_combinations(lista, listb)
        self.assertEqual(len(combinations), len(expected_result))
        self.assertEqual(combinations, expected_result)

    def test_different_size_lists_return_none(self):
        lista = []
        listb = [1]
        self.assertIsNone(ListUtils.pair_combinations(lista, listb))
