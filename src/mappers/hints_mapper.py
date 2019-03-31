from src.mappers.theorem_mapper import TheoremMapper
from sympy.parsing.sympy_parser import parse_expr
from src.utils.logger import Logger

class HintsMapper:

    def __init__(self):
        self.theorem_mapper = TheoremMapper()
        self.logger = Logger.getLogger()

    def map_theorems_that_apply_input(self, request_data):
        try:
            expression_json = request_data['expression']
            expression = parse_expr(expression_json, evaluate=False)
            theorems_json = request_data['theorems']
            theorems = self.theorem_mapper.from_json_to_theorems(theorems_json)
        except Exception as e:
            self.logger.error("Error while trying to map theorems that apply input: {}".format(e))
            raise e
        return (expression, theorems)
