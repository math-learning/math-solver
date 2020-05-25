import unittest

from mathlearning.model.expression import Expression
from mathlearning.model.integral_theorems import IntegralTheorems
from test.model.theorems.test_utils import TestUtils


theorem = IntegralTheorems.integral_of_a_sum()

equivalent_solutions = TestUtils.equivalent_solutions

class TestTheoremIntegralOfASum(unittest.TestCase):

    def test_simple_sum_should_apply(self):
        exp = Expression('\\int (x + x^2)dx')
        expected_result = [Expression('\\int(x)dx + \\int(x^2)dx')]
        result = theorem.apply_to(exp)
        self.assertEquals(result, expected_result)

    def test_sum_of_three_should_return_all_possibilities(self):
        exp = Expression('\\int(x + x^2 + x^3)dx')
        expected_result = [
            Expression('\\int(x + x^2)dx + \\int( x^3)dx'),
            Expression('\\int(x)dx + \\int(x^2 + x^3)dx'),
            Expression('\\int(x + x^3)dx + \\int(x^2)dx')
        ]
        result = theorem.apply_to(exp)
        self.assertTrue(equivalent_solutions(result, expected_result))

    def test_subtract_should_apply(self):
        exp = Expression('\\int(x - x^3)dx')
        expected_result = [
            Expression('\\int(x)dx + \\int(-x^3)dx'),
        ]
        result = theorem.apply_to(exp)
        self.assertTrue(equivalent_solutions(result, expected_result))
