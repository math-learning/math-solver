from mathlearning.model.theorem import Theorem

class DerivativeTheorems:

    def __init__(self):
        self.sum_of_derivatives = Theorem(
            "Derivada de la suma",
            "\\frac{d(f(x) + g(x))}{dx}",
            "\\frac{d(f(x))}{dx} + \\frac{d(g(x))}{dx}",
            {}
        )
        self.derivative_of_a_division = Theorem(
            "derivada de la division",
            "\\frac{d(\\frac{f(x)}{g(x)})}{dx}",
            "\\frac{ \\frac{ d(f(x))}{dx} * g(x) - \\frac{d(g(x))}{dx} * f(x) }{g(x)^ 2}",
            {}
        )
        self.derivative_of_a_multiplication = Theorem(
            "derivada del producto",
            "\\frac{d(f(x) * g(x))}{dx}",
            "\\frac{d(f(x))}{dx} * g(x) + \\frac{d(g(x))}{dx} * f(x)",
            {}
        )
        self.derivative_multiply_for_constant = Theorem(
            "Derivada por un numero real",
            "\\frac{d( a * f(x))}{dx}",
            "a * \\frac{d(f(x))}{dx}",
            {
                "a": [
                    "IS_REAL",
                    "IS_CONSTANT"
                ]
            }
        )
