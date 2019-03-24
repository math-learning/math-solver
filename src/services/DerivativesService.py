from sympy import Derivative


class DerivativeApplyItem:
    def __init__(self, before, after):
        self.before = before
        self.after = after


class DerivativeApplier:

    def apply_derivatives_rec(self, expression, derivatives_applied):
        if expression.func == Derivative:
            derivatives_applied.append(DerivativeApplyItem(expression, expression.doit()))
            return derivatives_applied
        else:
            for arg in expression.args:
                derivatives_applied += self.apply_derivatives_rec(arg, derivatives_applied)
        return derivatives_applied


    def apply_derivatives(self, expression):
        derivatives_applied = []
        return self.apply_derivatives_rec(expression, derivatives_applied)

    def printDerivatives(self, derivativesApplied):
        for der in derivativesApplied:
            print("Before: " +str(der.before) + ". After: " + str(der.after))

