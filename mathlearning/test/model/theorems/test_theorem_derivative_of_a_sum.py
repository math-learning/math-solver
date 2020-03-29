import unittest

from mathlearning.model.derivative_theorems import DerivativeTheorems
from mathlearning.model.expression import Expression
from test.model.theorems.test_utils import TestUtils


theorem_sum_of_derivatives = DerivativeTheorems().derivative_of_a_sum

equivalent_solutions = TestUtils.equivalent_solutions

class TestTheoremDerivativeOfASum(unittest.TestCase):

    def test_simple_sum_should_apply(self):
        exp = Expression('\\frac{d(x + x^2)}{dx}')
        expected_result = [Expression('\\frac{d(x)}{dx} + \\frac{d(x^2)}{dx}')]
        result = theorem_sum_of_derivatives.apply_to(exp)
        self.assertEquals(result, expected_result)

    def test_sum_of_three_should_return_all_possibilities(self):
        exp = Expression('\\frac{d(x + x^2 + x^3)}{dx}')
        expected_result = [
            Expression('\\frac{d(x + x^2)}{dx} + \\frac{d( x^3)}{dx}'),
            Expression('\\frac{d(x)}{dx} + \\frac{d(x^2 + x^3)}{dx}'),
            Expression('\\frac{d(x + x^3)}{dx} + \\frac{d(x^2)}{dx}')
        ]
        result = theorem_sum_of_derivatives.apply_to(exp)
        self.assertTrue(equivalent_solutions(result, expected_result))

    def test_subtract_should_apply(self):
        exp = Expression('\\frac{d(x - x^3)}{dx}')
        expected_result = [
            Expression('\\frac{d(x)}{dx} + \\frac{d(-x^3)}{dx}'),
        ]
        result = theorem_sum_of_derivatives.apply_to(exp)
        self.assertTrue(equivalent_solutions(result, expected_result))