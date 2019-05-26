from src.services.comparator_service import ComparatorService
from sympy import simplify
from src.model.theorem import Theorem
from src.services.derivative_service import DerivativeApplier

class HintsService:

    def __init__(self):
        self.comparatorService = ComparatorService()
        self.derivatives_applier = DerivativeApplier()

<<<<<<< Updated upstream
    def get_theorems_that_apply_hint(self, expression, theorems):
        theorems_that_apply = []
        
        for theo in theorems:
            comparison = self.comparatorService.compare(theo.left, expression)
            if comparison.structures_match:
                theorems_that_apply.append(theo)
=======
    def get_hints(self, expression, theorems):
        
        hints = self.theorems_service.get_theorems_that_can_be_applied_to(expression, theorems)
>>>>>>> Stashed changes
        
        if len(theorems_that_apply) == 0:
            new_step_deriv = self.derivatives_applier.apply_derivatives(expression)
            if new_step_deriv != expression:
                theorems_that_apply.append(Theorem("Aplicar derivadas con la tabla", "", ""))
            else:
                new_step_simplif = simplify(expression)
                if new_step_simplif != expression:
                    theorems_that_apply.append(Theorem("Simplificar la expresion", "", ""))


        return theorems_that_apply