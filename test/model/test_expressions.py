import unittest
from src.model.expressions import Expression

class TestExpression(unittest.TestCase):
    
    def test_is_leaf(self):

        leaf = Expression("x")
        self.assertTrue(leaf.is_leaf())

        non_leaf = Expression("x + 2")
        self.assertFalse(non_leaf.is_leaf())

    def test_solve_derivatives(self):
        exp = Expression("Derivative(x, x)")
        exp.solve_derivatives()
        self.assertEqual(exp.to_string(), '1')

    def test_compare(self):
        exp_one = Expression("x + x")
        exp_two = Expression("2 * x")

        self.assertTrue(exp_one.is_equivalent_to(exp_two))
    
    def test_get_children(self):
        exp = Expression("x + x**2")
        children = exp.get_children()
        self.assertEqual(2, len(children))

        self.assertTrue(Expression("x") in children)
        self.assertTrue(Expression("x**2") in children)