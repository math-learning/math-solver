import unittest

from mathlearning.model.derivative_theorems import DerivativeTheorems
from mathlearning.model.expression import Expression
from test.model.theorems.test_utils import TestUtils

theorem = DerivativeTheorems.derivative_of_a_multiplication()

equivalent_solutions = TestUtils.equivalent_solutions


class TestTheoremDerivativeOfAMultiplication(unittest.TestCase):

    def test_simple_multiplication_should_apply(self):
        exp = Expression('\\frac{d(x * \\cos(x))}{dx}')
        expected = Expression('\\frac{d(x)}{dx} * \\cos(x) + \\frac{d(\\cos(x))}{dx} * x')
        result = theorem.apply_to(exp)
        self.assertEquals(len(result), 1)
        self.assertTrue(expected.is_equivalent_to(result[0]))

    def test_simple_multiplication_that_can_be_simplified_should_apply(self):
        exp = Expression('\\frac{d(x * x)}{dx}')
        expected = Expression('\\frac{d(x)}{dx} * x + \\frac{d(x)}{dx} * x')
        result = theorem.apply_to(exp)
        self.assertEquals(len(result), 1)
        self.assertTrue(expected.is_equivalent_to(result[0]))

    def test_simple_multiplication_for_a_constant_shouldnt_apply(self):
        exp = Expression('\\frac{d(x * 1)}{dx}')
        result = theorem.apply_to(exp)
        self.assertEquals(len(result), 0)


    def test_complex_expression_with_multiplication_should_apply(self):
        exp = Expression('x^2 * \\sin(x) * \\frac{d(\\cos(x))}{dx} + \\cos(x) * \\frac{d(x^2 * \\sin(x))}{dx}')
        result = theorem.apply_to(exp)
        self.assertEquals(len(result), 1)

    def test_should_apply(self):
        exp = Expression("\\frac{d\\left(e^x.\\ x\\right)}{dx}\\ +\\ \\frac{d\\left(sen\\left(x\\right)\\cdot x^2\\right)}{dx}")
        result = theorem.apply_to(exp)
        self.assertEqual(2, len(result))
