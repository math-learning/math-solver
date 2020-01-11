import unittest
import json
from mathlearning.model.theorem import Theorem
from mathlearning.model.expression import Expression


def is_present(expression, expressions):
    for exp in expressions:
        if exp.is_equivalent_to(expression):
            return True
    return False


class TestTheorem(unittest.TestCase):

    def setUp(self):
        self.derivative_sum_theorem = Theorem("Derivada de la suma",
                                              "\\frac{d(f(x) + g(x))}{dx}",
                                              "\\frac{d(f(x))}{dx} + \\frac{d(g(x))}{dx}",
                                              [])

    def test_apply_to(self):
        theorem = self.derivative_sum_theorem
        exp = Expression("\\frac{d(x + x^2)}{dx}")
        possibilities = theorem.apply_to(exp)
        expected = Expression("\\frac{d(x)}{dx} + \\frac{d(x^2)}{dx}")
        self.assertTrue(expected in possibilities)

    def test_apply_to_children(self):
        theorem = self.derivative_sum_theorem
        expression = Expression("\\frac{d(x + x^2)}{dx} + x^3")
        possibilities = theorem.apply_to(expression)
        expected = Expression("x^3 + \\frac{d(x)}{dx} + \\frac{d(x^2)}{dx}")

        self.assertTrue(is_present(expected, possibilities))

    def test_apply_reverse_to(self):
        theorem = self.derivative_sum_theorem
        expression = Expression("x^3 + \\frac{d(x)}{dx} + \\frac{d(x^2)}{dx}")
        possibilities = theorem.apply_reverse_to(expression)
        expected = Expression("\\frac{d(x + x^2)}{dx} + x^3")
        print(possibilities)
        self.assertTrue(is_present(expected, possibilities))

    # def test_apply_reverse_to_(self):
    #     theorem = self.derivative_sum_theorem
    #     expression = Expression("- x^2\\sin ^2(x) +\\cos (x)\\frac{d\\left(x^2\\sin (x)\\right)}{dx}")
    #     possibilities = theorem.apply_reverse_to(expression)
    #     expected = Expression("-\\ x^2\\sin ^2(x) +\\cos (x) * \\left(\\frac{d\\left(\\sin (x)\\right)}{dx}x^2+ \\frac{d\\left(x^2\\right)}{dx} * \\sin \\left(x\\right)\\right)")
    #     print(possibilities)
    #     self.assertTrue(is_present(expected, possibilities))
