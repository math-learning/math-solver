from sympy import *
from src.model.Theorem import Theorem
from sympy.parsing.sympy_parser import parse_expr
from src.mappers.TheoremMapper import TheoremMapper

class ValidateMapperException(Exception):
    pass

class ValidateMapper:
    def __init__(self):
        self.theoremMapper = TheoremMapper()

    
    def parse_validate_new_step_input(self, request_data):
        try:
            theorems = request_data['theorems']
            new_expression = request_data['new_expression']
            old_expression = request_data['old_expression']

            sympy_old_expr = parse_expr(old_expression, evaluate=False)
            parsed_theorems = self.theoremMapper.from_json_to_theorems(theorems)
            sympy_new_expr = parse_expr(new_expression, evaluate=False)
            
            return (sympy_new_expr, sympy_old_expr, parsed_theorems)
        except:
            raise ValidateMapperException