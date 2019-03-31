from src.services.ComparatorService import ComparatorService
from src.utils.Logger import Logger

from src.services.DerivativesService import DerivativeApplier
from src.model.TransformationResult import TransformationResult
from src.transformers.ExpressionTransformer import ExpressionTransformer
from sympy import simplify


RESULT_FOUND_TEMPLATE = "The new expression {} was the result of applying {} theorem to {}"

class ValidatorService:
    def __init__(self):
        self.comparatorService = ComparatorService()
        self.expression_transformer = ExpressionTransformer()
        self.derivatives_applier = DerivativeApplier()
        self.logger = Logger.getLogger()

    def is_a_valid_next_step(self, old_expression, new_expression, theorems):
        self.logger.info("Starting transition validation")
        # Try with theorems
        self.logger.info("Trying with theorems")
        for theo in theorems:
            self.logger.info("Checking if theorem: {} applies to {}".format(theo.name, new_expression))
            comparison = self.comparatorService.compare(theo.left, old_expression)
            self.logger.info("Result: {}".format(comparison.structures_match))
            if comparison.structures_match:
                new_step = self.expression_transformer.transform(theo.right, comparison.equalities)
                if new_step == simplify(new_expression):
                    self.logger.info(RESULT_FOUND_TEMPLATE.format(new_expression, theo.name, old_expression))
                    return True

        if new_expression != old_expression:
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
