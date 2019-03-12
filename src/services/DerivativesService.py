from sympy import Derivative


class DerivativeApplyItem:
    def __init__(self, before, after):
        self.before = before
        self.after = after


def apply_derivatives_rec(expression, derivatives_applied):
    if expression.func == Derivative:
        derivatives_applied.append(DerivativeApplyItem(expression, expression.doit()))
        return derivatives_applied
    else:
        for arg in expression.args:
            derivatives_applied += apply_derivatives_rec(arg, derivatives_applied)
    return derivatives_applied


def apply_derivatives(expression):
    derivatives_applied = []
    return apply_derivatives_rec(expression, derivatives_applied)