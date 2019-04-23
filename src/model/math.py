

class MathWrapper:

    # Returns the result of applying the theorem to the expression
    # or None if the theorem cant be applied
    def apply_theorem(self, expression, theorem):
        # if not theorem_can_be_applied(expression, theorem):
        #   return None
        pass

    def theorems_that_apply(self, expression, theorems):
        pass

    def apply_simplifications(self, expression):
        pass

    def apply_derivatives(self, expression):
        return self.derivatives.apply(expression)

    # Tell if the theorem can be applied to the expression or
    # to a part of the expression
    def theorem_can_be_applied(self, expression, theorem):
        pass



