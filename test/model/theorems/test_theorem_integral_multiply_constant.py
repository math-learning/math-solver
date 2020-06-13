import unittest

from mathlearning.model.expression import Expression
from mathlearning.model.integrate_theorems import IntegrateTheorems

theorem = IntegrateTheorems.integrate_multiply_for_constant()

class TestTheoremIntegralMultiplyForConstant(unittest.TestCase):

    def test_simple_multiplication_should_apply(self):
        exp = Expression('\\int(2*x)dx')
        expected = Expression('2*\\int(x)dx')
        result = theorem.apply_to(exp)
        self.assertEquals(len(result), 1)
        self.assertTrue(expected.is_equivalent_to(result[0]))

    def test_non_constant_multiplication_should_not_apply(self):
        exp = Expression('\\int(x*x)dx')
        result = theorem.apply_to(exp)
        self.assertEquals(len(result), 0)

    def test_sum_a_constant_should_not_apply(self):
        exp = Expression('\\int(2 + x)dx')
        result = theorem.apply_to(exp)
        self.assertEquals(len(result), 0)
