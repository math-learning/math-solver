import unittest
from src.utils.list_utils import ListUtils

class TestListUtils(unittest.TestCase):

    def test_combinations_size_two(self):
        lista = [1,2]
        listb = [3,4]
        expected_result = [
            [[1,3],[2,4]],
            [[1,4],[2,3]],
            ]
        combinations = ListUtils.combinations(lista, listb)
        self.assertEqual(combinations, expected_result)
    
    def test_combinations_size_three(self):
        lista = [1,2,3]
        listb = [4,5,6]
        expected_result = [
            [[1,4],[2,5],[3,6]],
            [[1,4],[2,6],[3,5]],
            [[1,5],[2,4],[3,6]],
            [[1,5],[2,6],[3,4]],
            [[1,6],[2,4],[3,5]],
            [[1,6],[2,5],[3,4]]
            ]
        combinations = ListUtils.combinations(lista, listb)
        self.assertEqual(len(combinations), len(expected_result))
        self.assertEqual(combinations, expected_result)

    
    def test_different_size_lists_return_none(self):
        lista = []
        listb = [1]
        self.assertIsNone(ListUtils.combinations(lista,listb))

    
    def test_combinations_diff_sizes(self):
        lista = [1,2,3]
        listb = [4,5,6]


    def test_get_list_of_joins(self):
        smaller_size = 2
        larger_size = 4
        a = ListUtils.compute_rec(3, 4, 2,[],[])
        expected = [[0,2,0], [1,0,1]]
        self.assertEquals(expected, a)

    