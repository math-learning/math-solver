import unittest

from mathlearning.utils.list.commutative_group_transformer import \
    CommutativeGroupTransformer
from mathlearning.utils.list.list_size_transformer import ListSizeTransformer


class TestCommutativeGroupTransformer(unittest.TestCase):

    def test_transform_grouping_case(self):
        elements = [1,2,3,4]
        join_case = [1,0,1]

        group_transformer = CommutativeGroupTransformer()

        a = group_transformer.transform(join_case, elements)
        expected = [
            [[1], [2,3,4]],
            [[2], [1,3,4]],
            [[3], [1,2,4]],
            [[4], [1,2,3]]
        ]
        self.assertEquals(expected, a)