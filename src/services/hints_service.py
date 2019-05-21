from sympy import simplify
from src.model.theorem import Theorem
from src.services.theorems_service import TheoremsService

class HintsService:

    def __init__(self):
        self.theorems_service = TheoremsService()

    def get_theorems_that_apply_hint(self, expression, exercise):
        theorems_that_apply = self.theorems_service.get_theorems_that_can_be_applied_to(expression, exercise.theorems)
        
        if len(theorems_that_apply) == 0:
            new_step_deriv = expression.apply_derivatives()
            if new_step_deriv != expression:
                theorems_that_apply.append(Theorem("Aplicar derivadas con la tabla", "", ""))
            else:
                new_step_simplif = expression.simplify()
                if new_step_simplif != expression:
                    theorems_that_apply.append(Theorem("Simplificar la expresion", "", ""))

        return theorems_that_apply