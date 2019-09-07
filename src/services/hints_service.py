from src.model.theorem import Theorem
from src.model.hint import TextHint
from src.services.theorems_service import TheoremsService

class HintsService:

    def __init__(self):
        self.theorems_service = TheoremsService()
        self.comparatorService = ComparatorService()


    def get_theorems_that_apply_hint(self, expression, theorems):
        theorems_that_apply = []
        
        for theo in theorems:
            comparison = self.comparatorService.compare(theo.left, expression)
            if comparison.structures_match:
                theorems_that_apply.append(theo)

    def get_hints(self, expression: Expression, theorems: List[Theorem]):
        hints = self.theorems_service.get_theorems_that_can_be_applied_to(expression, theorems)
        # Todo
        if len(hints) == 0:
            new_step_deriv = expression.solve_derivatives()
            if new_step_deriv != expression:
                hints.append(TextHint("Aplicar derivadas con la tabla"))
            else:
                new_step_simplif = expression.simplify()
                if new_step_simplif != expression:
                    hints.append(TextHint("Simplificar la expresion"))

        return hints