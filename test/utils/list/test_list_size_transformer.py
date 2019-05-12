import unittest

from src.utils.list.index_combinations_strategy import IndexCombinationStrategy
from src.utils.list.list_size_transformer import ListSizeTransformer


class TestListSizeTransformer(unittest.TestCase):
    
    def test_transform(self):
        a_list = [1,2,3]
        combinations_strategy = IndexCombinationStrategy()
        transformer = ListSizeTransformer(combinations_strategy)
        transformations  = transformer.transform(a_list,2)
        expected = [
            [[1],[2,3]],
            [[2],[1,3]],
            [[3],[1,2]]
        ]
        self.assertEquals(expected, transformations)
    

    def test_amount_of_groups_by_group_elements_number(self):
        smaller_size = 2
        larger_size = 4
        combinations_strategy = IndexCombinationStrategy()
        transformer = ListSizeTransformer(combinations_strategy)
        result = transformer.amount_of_groups_by_group_elements_number(smaller_size, larger_size)
        expected = [[0,2,0], [1,0,1]]
        self.assertEquals(expected, result)

    def test_amount_of_groups_by_group_elements_number_other(self):
        smaller_size = 2
        larger_size = 5
        combinations_strategy = IndexCombinationStrategy()
        transformer = ListSizeTransformer(combinations_strategy)
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


    def test_transform_grouping_case(self):
        elements = [1,2,3,4]
        join_case = [1,0,1]

        combinations_strategy = IndexCombinationStrategy()
        transformer = ListSizeTransformer(combinations_strategy)

        a = transformer.transform_grouping_case(join_case, elements)
        expected = [
            [[1], [2,3,4]],
            [[2], [1,3,4]],
            [[3], [1,2,4]],
            [[4], [1,2,3]]
        ]
        self.assertEquals(expected, a)
    
