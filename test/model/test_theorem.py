import unittest
import json
from src.model.theorem import Theorem
from src.model.expression import Expression


class TestTheorem(unittest.TestCase):


    def test_apply_to(self):    
        theorem = Theorem("Derivada de la suma",
                        "\\frac{d(f(x) + g(x))}{dx}",
                        "\\frac{d(f(x))}{dx} + \\frac{d(g(x))}{dx}",
                            [])

        exp = Expression("\\frac{d(x + x^2)}{dx}")
        possibilities = theorem.apply_to(exp)
            
        expected = Expression("\\frac{d(x)}{dx} + \\frac{d(x^2)}{dx}")

        self.assertTrue( expected in possibilities )
    
    def test_apply_to_children(self):    
        theorem = Theorem("Derivada de la suma",
                        "\\frac{d(f(x) + g(x))}{dx}",
                        "\\frac{d(f(x))}{dx} + \\frac{d(g(x))}{dx}",
                            [])

        expression = Expression("\\frac{d(x + x^2)}{dx} + x^3")
        possibilities = theorem.apply_to(expression)
        print(possibilities)
        expected = Expression("x^3 + \\frac{d(x)}{dx} + \\frac{d(x^2)}{dx}")
        
        self.assertTrue(expected in possibilities)
        
    