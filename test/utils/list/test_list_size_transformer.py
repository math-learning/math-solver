import unittest

from src.utils.list.commutative_group_transformer import \
    CommutativeGroupTransformer
from src.utils.list.non_commutative_group_transformer import \
    NonCommutativeGroupTransformer
from src.utils.list.list_size_transformer import ListSizeTransformer


class TestListSizeTransformer(unittest.TestCase):
    
    def test_transform(self):
        a_list = [1,2,3]
        group_transformer = CommutativeGroupTransformer()
        transformer = ListSizeTransformer(group_transformer)
        transformations  = transformer.transform(a_list,2)
        expected = [
            [[1],[2,3]],
            [[2],[1,3]],
            [[3],[1,2]]
        ]
        self.assertEquals(expected, transformations)
    
    def test_transform_only_continuous(self):
        a_list = [1,2,3]
        group_transformer = NonCommutativeGroupTransformer()
        transformer = ListSizeTransformer(group_transformer)
        transformations  = transformer.transform(a_list,2)
        expected = [
            [[1],[2,3]],
            [[3],[1,2]]
        ]
        self.assertEquals(expected, transformations)

    def test_amount_of_groups_by_group_elements_number(self):
        smaller_size = 2
        larger_size = 4
        group_transformer = CommutativeGroupTransformer()
        transformer = ListSizeTransformer(group_transformer)
        result = transformer.amount_of_groups_by_group_elements_number(smaller_size, larger_size)
        expected = [[0,2,0], [1,0,1]]
        self.assertEquals(expected, result)

    def test_amount_of_groups_by_group_elements_number_other(self):
        smaller_size = 2
        larger_size = 5
        group_transformer = CommutativeGroupTransformer()
        transformer = ListSizeTransformer(group_transformer)
        result = transformer.amount_of_groups_by_group_elements_number(smaller_size, larger_size)
        expected = [[0,1,1,0], [1,0,0,1]]
        self.assertEquals(expected, result)


    # def test_combinations_of_n_elem(self):

    #     elements = [1,2,3]
    #     n = 2
        
    #     combinations = ListUtils.combinations_of_n_elem(elements, n)
    #     expected = [
    #             SubCombination([1,2], [3]),
    #             SubCombination([1,3], [2]),
    #             SubCombination([2,3], [1])
    #         ]
    #     self.assertEquals(expected, combinations)


    
