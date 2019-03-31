from src.services.comparator_service import ComparatorService

class HintsService:

    def __init__(self):
        self.comparatorService = ComparatorService()
        pass

    def get_theorems_that_apply_hint(self, expression, theorems):
        theorems_that_apply = []
        for theo in theorems:
            comparison = self.comparatorService.compare(theo.left, expression)
            if comparison.structures_match:
                theorems_that_apply.append(theo)
        
        return theorems_that_apply