from mathlearning.model.theorem import Theorem


class DerivativeTheorems:

    @staticmethod
    def derivative_of_a_sum():
        return Theorem(
            "Derivada de la suma",
            "\\frac{d(f(x) + g(x))}{dx}",
            "\\frac{d(f(x))}{dx} + \\frac{d(g(x))}{dx}",
            {}
        )

    @staticmethod
    def derivative_of_a_division():
        return Theorem(
            "derivada de la division",
            "\\frac{d(\\frac{f(x)}{g(x)})}{dx}",
            "\\frac{ \\frac{ d(f(x))}{dx} * g(x) - \\frac{d(g(x))}{dx} * f(x) }{g(x)^ 2}",
            {}
        )

    @staticmethod
    def derivative_of_a_multiplication():
        return Theorem(
            "derivada del producto",
            "\\frac{d(f(x) * g(x))}{dx}",
            "\\frac{d(f(x))}{dx} * g(x) + \\frac{d(g(x))}{dx} * f(x)",
            {},
        )

    @staticmethod
    def derivative_multiply_for_constant():
        return Theorem(
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

    @staticmethod
    def get_all():
        return [
            DerivativeTheorems.derivative_of_a_multiplication(),
            DerivativeTheorems.derivative_multiply_for_constant(),
            DerivativeTheorems.derivative_of_a_division(),
            DerivativeTheorems.derivative_of_a_sum()
        ]
