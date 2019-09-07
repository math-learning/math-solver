from src.services.step_service import StepService
from src.utils.logger import Logger
from src.services.hints_service import HintsService
from src.model.expression import Expression
from typing import List

logger = Logger.getLogger()

class ResultService:
    
    def __init__(self):
        self.step_service = StepService()
        self.hints_service = HintsService()

    def validate_result(self, steps: List[Expression], exercise: Expression) -> bool:
        
        # validate intermediate results
        for i in range(0, len(steps) - 1):
            old_step = steps[i]
            new_step = steps[i+1]
            if not self.step_service.is_a_valid_next_step(old_step, new_step, exercise.theorems):
                return False
        
        result = steps[-1]

        return  exercise.result == result

    def get_derivative_result(self, expression: Expression) -> Expression:
        return expression.solve_derivatives()
        
                
            


        