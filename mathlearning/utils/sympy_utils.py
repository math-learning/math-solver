import sympy
from sympy.core.numbers import NegativeOne


class SympyUtils:
    @staticmethod
    def is_division(sympy_expr):
        if sympy_expr.func == sympy.Mul:
            # sympy represents division a/b like a * (b**-1)
            arguments = sympy_expr.args
            for argument in arguments:
                if argument.func == sympy.Pow:
                    for pow_argument in argument.args:
                        if pow_argument.func == NegativeOne:
                            return True
        return False
