from src.services.ComparatorService import ComparatorService
import logging

class ValidatorService:
    def __init__(self):
        self.comparatorService = ComparatorService()
        self.logger = logging.getLogger("flask.app")

    def validate_transition(self, old_expression, new_expression, theorems):
        self.logger.info("Validate")
        return self.comparatorService.compare_equality(old_expression,new_expression, theorems)
