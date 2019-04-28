import unittest

from src.model.theorem import Theorem
from src.model.expression import Expression


class TestTheorem(unittest.TestCase):

    def test_apply_to(self):    
        theorem = Theorem("Derivada de la suma",
                        "d(f(x) + g(x), x)",
                        "d(f(x), x) + d(g(x),x)")

        exp = Expression("d(x + x**2, x)")
        new_exp = theorem.apply_to(exp)

        self.assertEqual(new_exp.to_string(), "d(x,x) + d(x**2,x)")
        