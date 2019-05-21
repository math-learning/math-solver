from sympy import simplify
from src.services.theorems_service import TheoremsService
from src.utils.logger import Logger

RESULT_FOUND_TEMPLATE = "The new expression {} was the result of applying {} theorem to {}"

logger = Logger.getLogger()

class StepService:

    def __init__(self):
        self.theorems_service = TheoremsService()

    def is_a_valid_next_step(self, old_expression, new_expression, theorems):
        logger.info("Starting transition validation")
        
        if old_expression == new_expression:
            logger.info("New expression is equal to the old one.")
            return False

        theorems_that_apply = self.theorems_service.get_theorems_that_can_be_applied_to(old_expression, theorems)

        for theorem in theorems_that_apply:
            if theorem.apply_to(old_expression) == new_expression:
                logger.info("Theorem can be applied")
                return True
        
        #try with derivatives
        if old_expression.solve_derivatives() == new_expression:
            logger.info("Derivatives were applied")
            return True
        
        #try simplifying the expression
        if old_expression.simplify() == new_expression:
            logger.info("Simplifications were applied")
            return True
        
        return False
        
    
    def validate_not_in_history(self, expr, history):
        for item in history:
            if expr == item:
                return False
        return True
