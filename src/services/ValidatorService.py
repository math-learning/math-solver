from src.services.ComparatorService import ComparatorService
from src.utils.Logger import Logger

class ValidatorService:
    def __init__(self):
        self.comparatorService = ComparatorService()
        self.logger = Logger.getLogger()

    def validate_transition(self, old_expression, new_expression, theorems):
        self.logger.info("Starting transition validation")
        return self.comparatorService.compare_equality(old_expression,new_expression, theorems)
