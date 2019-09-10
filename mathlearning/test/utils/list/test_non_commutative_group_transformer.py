import unittest

from mathlearning.utils.list.non_commutative_group_transformer import NonCommutativeGroupTransformer


class TestNonCommutativeGroupTransformer(unittest.TestCase):

    def test_transform(self):
        transformer = NonCommutativeGroupTransformer()
        grouping_case = [1, 0, 1]
        elements = [1, 2, 3, 4] 
        result = transformer.transform(grouping_case, elements)
        expected = [
            [[1],[2,3,4]],
            [[4],[1,2,3]]
        ]
        self.assertEquals(expected, result)