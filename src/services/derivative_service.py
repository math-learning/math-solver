from sympy import Derivative
import logging
logger = logging.getLogger("flask.app")

class DerivativeApplyItem:
    def __init__(self, before, after):
        self.before = before
        self.after = after


class DerivativeApplier:

    def get_derivatives_that_can_be_applied(self, expression, derivatives_applied):
        if expression.func == Derivative:
            derivatives_applied.append(DerivativeApplyItem(expression, expression.doit()))
            return derivatives_applied
        else:
            for arg in expression.args:
                derivatives_applied += self.get_derivatives_that_can_be_applied(arg, derivatives_applied)
        return derivatives_applied


    def apply_derivatives(self, expression):
        derivatives_applied = self.get_derivatives_that_can_be_applied(expression, [])
        new_expression = expression
        logger.info('Applying derivatives to: {}'.format(expression))
        for derivative in derivatives_applied:
            new_expression = new_expression.subs({derivative.before: derivative.after}, evaluate=False)
        logger.info('Result: {}'.format(new_expression))
        return new_expression

    def printDerivatives(self, derivativesApplied):
        for der in derivativesApplied:
            print("Before: " +str(der.before) + ". After: " + str(der.after))

