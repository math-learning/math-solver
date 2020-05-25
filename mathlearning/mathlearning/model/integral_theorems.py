from mathlearning.model.theorem import Theorem


class IntegralTheorems:

    @staticmethod
    def integral_of_a_sum():
        return Theorem(
            "Integral de la suma",
            "\\int (f(x) + g(x)) dx",
            "\\int (f(x)) dx + \\int (g(x)) dx",
            {}
        )

    @staticmethod
    def integral_multiply_for_constant():
        return Theorem(
            "Integral por una constante",
            "\\int ( a * f(x)) dx",
            "a * \\int (f(x)) dx",
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
            IntegralTheorems.integral_of_a_sum(),
            IntegralTheorems.integral_multiply_for_constant()
        ]
