import unittest
from src.model.expressions import Expression

class TestExpression(unittest.TestCase):
    
    def test_is_leaf(self):

        leaf = Expression("x", False)
        self.assertTrue(leaf.is_leaf())

        non_leaf = Expression("x + 2", False)
        self.assertFalse(non_leaf.is_leaf())

    def test_solve_derivatives(self):
        exp = Expression("Derivative(x, x)", False)
        exp.solve_derivatives()
        self.assertEqual(exp.to_string(), '1')

    def test_compare(self):
        exp_one = Expression("x + x", evaluate=False)
        exp_two = Expression("2 * x", evaluate=False)

        self.assertTrue(exp_one.compare(exp_two))