from src.services.theorems_service import TheoremsService
from src.utils.logger import Logger

RESULT_FOUND_TEMPLATE = "The new expression {} was the result of applying {} theorem to {}"

logger = Logger.getLogger()

class StepService:

    def __init__(self):
        self.theorems_service = TheoremsService()

    def is_a_valid_next_step(self, old_expression, new_expression, theorems):
        logger.info("Starting transition validation")

        logger.info("Checking if a theorem can be applied")
        theorems_that_apply = self.theorems_service.get_theorems_that_can_be_applied_to(old_expression, theorems)

        logger.info("THEOREMS THAT APPLY:")
        logger.info(theorems_that_apply)

        for theorem in theorems_that_apply:
            theo_applied = theorem.apply_to(old_expression)
            for possibility in theo_applied:
                if possibility != None and possibility.simplify() == new_expression.simplify():
                    logger.info("Theorem can be applied")
                    return True
                    
            theo_applied_reverse = theorem.apply_reverse_to(new_expression)
            for possibility in theo_applied_reverse:
                if possibility != None and possibility.simplify() == old_expression.simplify():
                    logger.info("Theorem can be applied")
                    return True

        #try with derivatives
        logger.info("Try with derivatives")
        if old_expression.solve_derivatives().simplify() == new_expression.simplify():
            logger.info("Derivatives were applied")
            return True
        
        only_one_derivative = old_expression.derivatives_solving_possibilities()
        for derivative_applied in only_one_derivative:
            if derivative_applied.simplify() == new_expression.simplify():
                return True
        
        #try simplifying the expression
        logger.info("Try simplifying")
        old_simplifications = old_expression.get_simplifications()
        for simplification in old_simplifications:
            new_simplifications = new_expression.get_simplifications()
            if simplification in new_simplifications:
                logger.info("Simplifications were applied")
                return True
        
        logger.info("Invalid next step: " + str(new_expression) + " - Old expression: " + str(old_expression))
        return False
        
    
    def validate_not_in_history(self, expr, history):
        for item in history:
            if expr == item:
                return False
        return True
