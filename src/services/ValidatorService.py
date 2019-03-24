from src.services.ComparatorService import ComparatorService

class ValidatorService:
    def __init__(self):
        self.comparatorService = ComparatorService()

    def validate_transition(self, old_expression, new_expression, theorems):
        return self.comparatorService.compare_equality(old_expression,new_expression, theorems)
