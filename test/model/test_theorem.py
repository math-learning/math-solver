import unittest

from src.model.theorem import Theorem
from src.model.expression import Expression


class TestTheorem(unittest.TestCase):

    def test_apply_to(self):    
        theorem = Theorem("Derivada de la suma",
                        "\\frac{d(f(x) + g(x))}{dx}",
                        "\\frac{d(f(x))}{dx} + d(g(x))}{dx}",
                            [])

        exp = Expression("\\frac{d(x + x^2)}{dx}")
        new_exp = theorem.apply_to(exp)

        self.assertEqual(new_exp.to_string(), "\\frac{d(x)}{dx} + d(x^2)}{dx}")
    
    def test_apply_to_children(self):    
        theorem = Theorem("Derivada de la suma",
                        "\\frac{d(f(x) + g(x))}{dx}",
                        "\\frac{d(f(x))}{dx} + d(g(x))}{dx}",
                            [])

        exp = Expression("\\frac{d(x + x^2)}{dx} + x ^ 3")
        new_exp = theorem.apply_to(exp)

        self.assertEqual("x^3 + \\frac{d(x)}{dx} + \\frac{d(x^2)}{dx}", new_exp.to_string())
        
    