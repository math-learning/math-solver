from src.services.step_service import StepService
from src.utils.logger import Logger

logger = Logger.getLogger()

class ResultService:
    
    def __init__(self):
        self.step_service = StepService()

    def validate_result(self, steps, exercise):
        
        # validate intermediate results
        for i in range(0, len(steps) - 1):
            old_step = steps[i]
            new_step = steps[i+1]
            if not self.step_service.is_a_valid_next_step(old_step, new_step, exercise.theorems):
                return False
        
        result = steps[-1]

        return  exercise.result == result
