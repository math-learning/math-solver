import unittest

from src.model.theorem import Theorem
from src.model.expression import Expression


class TestTheorem(unittest.TestCase):

    def test_apply_to(self):    
        theorem = Theorem("Derivada de la suma",
                        "Derivative(f(x) + g(x), x)",
                        "Derivative(f(x), x) + d(g(x),x)")

        exp = Expression("Derivative(x + x**2, x)")
        new_exp = theorem.apply_to(exp)

        self.assertEqual(new_exp.to_string(), "Derivative(x, x) + d(x**2, x)")
    
    def test_apply_to_children(self):    
        theorem = Theorem("Derivada de la suma",
                        "Derivative(f(x) + g(x), x)",
                        "Derivative(f(x), x) + d(g(x),x)")

        exp = Expression("Derivative(x + x**2, x) + x ** 3")
        new_exp = theorem.apply_to(exp)

        self.assertEqual("x**3 + d(x, x) + d(x**2, x)", new_exp.to_string())
        
    