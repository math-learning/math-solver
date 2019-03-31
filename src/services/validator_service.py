from sympy import simplify

from src.model.transformation_result import TransformationResult
from src.services.comparator_service import ComparatorService
from src.services.derivative_service import DerivativeApplier
from src.transformers.expression_transformer import ExpressionTransformer
from src.utils.logger import Logger

RESULT_FOUND_TEMPLATE = "The new expression {} was the result of applying {} theorem to {}"

class ValidatorService:

    def __init__(self):
        self.comparator_service = ComparatorService()
        self.expression_transformer = ExpressionTransformer()
        self.derivatives_applier = DerivativeApplier()
        self.logger = Logger.getLogger()

    def is_a_valid_next_step(self, old_expression, new_expression, theorems):
        self.logger.info("Starting transition validation")

        theorem_can_be_applied = False

        # Try with theorems
        self.logger.info("Trying with theorems")
        for theo in theorems:
            self.logger.info("Checking if theorem: {} applies to {}".format(theo.name, new_expression))
            comparison = self.comparator_service.compare(theo.left, old_expression)
            self.logger.info("Result: {}".format(comparison.structures_match))
            if comparison.structures_match:
                theorem_can_be_applied = True
                new_step = self.expression_transformer.transform(theo.right, comparison.equalities)
                if new_step == simplify(new_expression):
                    self.logger.info(RESULT_FOUND_TEMPLATE.format(new_expression, theo.name, old_expression))
                    return True

        if new_expression != old_expression and not theorem_can_be_applied:
            self.logger.info("New expression wont match theorems")
            self.logger.info("Try to apply derivatives")
            # Try applying derivatives:
            new_step = self.derivatives_applier.apply_derivatives(old_expression)
            if new_step == simplify(new_expression):
                self.logger.info(RESULT_FOUND_TEMPLATE.format(new_expression, "derivatives", old_expression))
                return True
            
            # Try simplifying
            if simplify(new_expression) == simplify(old_expression):
                self.logger.info(RESULT_FOUND_TEMPLATE.format(new_expression, "simplifications", old_expression))
                return True
        self.logger.info("The new expression {} is not a valid next step of {}".format(new_expression,old_expression))
        return False

    def validate_result(self, result, input_expression, theorems):
        solution = self.comparator_service.get_solution_if_possible(input_expression, theorems)
        return result == solution[-1].expression
    
    def validate_not_in_history(self, expr, history):
        for item in history:
            if expr == item:
                return False
        return True
