from mathlearning.mappers.theorem_mapper import TheoremMapper
from mathlearning.model.expression import Expression
from mathlearning.utils.logger import Logger
from typing import List
from mathlearning.model.theorem import Theorem

class HintsMapper:

    def __init__(self):
        self.theorem_mapper = TheoremMapper()
        self.logger = Logger.getLogger()

    def map_theorems_that_apply_input(self, request_data: dict) -> List[Theorem]:
        try:
            formula = request_data['expression']
            expression = Expression(formula)
            theorems_json = request_data['theorems']
            theorems = self.theorem_mapper.theorems(theorems_json)
            return expression, theorems
            
        except Exception as e:
            self.logger.error("Error while trying to map theorems that apply input: {}".format(e))
            raise e
