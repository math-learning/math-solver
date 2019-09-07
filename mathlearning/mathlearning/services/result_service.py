from mathlearning.services.step_service import StepService
from mathlearning.utils.logger import Logger
from mathlearning.model.expression import Expression
from typing import List

logger = Logger.getLogger()

class ResultService:
    
    def __init__(self):
        self.step_service = StepService()

    def get_derivative_result(self, expression: Expression) -> Expression:
        return expression.solve_derivatives()
        
                
            


        