from sympy import Derivative
import logging
logger = logging.getLogger("flask.app")

class DerivativeApplyItem:
    def __init__(self, before, after):
        self.before = before
        self.after = after


class Derivatives:
    def get_derivatives_that_can_be_applied(self, expression, derivatives_applied):
        if expression.func == Derivative:
            derivatives_applied.append(DerivativeApplyItem(expression, expression.doit()))
            return derivatives_applied
        else:
            for arg in expression.args:
                derivatives_applied += self.get_derivatives_that_can_be_applied(arg, derivatives_applied)
        return derivatives_applied


    def apply(self, expression):
        
        logger.info('Applying derivatives to: {}'.format(expression))

        derivatives_applied = self.get_derivatives_that_can_be_applied(expression, [])
        result = expression

        for derivative in derivatives_applied:
            result = result.subs({derivative.before: derivative.after}, evaluate=False)

        logger.info('Result: {}'.format(result))
        
        return result

