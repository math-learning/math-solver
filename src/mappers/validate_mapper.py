from sympy import *
from src.model.theorem import Theorem
from sympy.parsing.sympy_parser import parse_expr
from src.mappers.theorem_mapper import TheoremMapper
from src.utils.logger import Logger

class ValidateMapperException(Exception):
    pass

class ValidateMapper:
    def __init__(self):
        self.theoremMapper = TheoremMapper()
        self.logger = Logger.getLogger()
    
    def parse_validate_new_step_input(self, request_data):
        self.logger.info("Parsing validate new step request data: {}".format(request_data))
        try:
            theorems = request_data['theorems']
            new_expression = request_data['new_expression']
            old_expression = request_data['old_expression']

            sympy_old_expr = parse_expr(old_expression, evaluate=False)
            parsed_theorems = self.theoremMapper.from_json_to_theorems(theorems)
            sympy_new_expr = parse_expr(new_expression, evaluate=False)
            
            return (sympy_new_expr, sympy_old_expr, parsed_theorems)
        except Exception as e:
            self.logger.error("Error while parsing validate new step input: {}".format(e))
            raise ValidateMapperException(e)

    def parse_validate_result_input(self, request_data):
        self.logger.info("Parsing validate result request data: {}".format(request_data))
        try:
            theorems = request_data['theorems']
            result = request_data['result']
            input_data = request_data['input_data']

            sympy_result = parse_expr(result, evaluate=False)
            parsed_theorems = self.theoremMapper.from_json_to_theorems(theorems)
            sympy_input_data = parse_expr(input_data, evaluate=False)
            
            return (sympy_result, sympy_input_data, parsed_theorems)
        except Exception as e:
            self.logger.error("Error while parsing validate result input: {}".format(e))
            raise ValidateMapperException(e)