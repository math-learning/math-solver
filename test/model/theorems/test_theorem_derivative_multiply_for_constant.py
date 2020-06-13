import unittest

from mathlearning.model.derivative_theorems import DerivativeTheorems
from mathlearning.model.expression import Expression

theorem = DerivativeTheorems.derivative_multiply_for_constant()

class TestTheoremDerivativeMultiplyForConstant(unittest.TestCase):

    def test_simple_multiplication_should_apply(self):
        exp = Expression('\\frac{d(2*x)}{dx}')
        expected = Expression('2*\\frac{d(x)}{dx}')
        result = theorem.apply_to(exp)
        self.assertEquals(len(result), 1)
        self.assertTrue(expected.is_equivalent_to(result[0]))

    def test_non_constant_multiplication_should_not_apply(self):
        exp = Expression('\\frac{d(x*x)}{dx}')
        result = theorem.apply_to(exp)
        self.assertEquals(len(result), 0)

    def test_sum_a_constant_should_apply(self):
        exp = Expression('\\frac{d(2 + x)}{dx}')
        result = theorem.apply_to(exp)
        self.assertEquals(len(result), 0)
