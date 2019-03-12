from sympy import *
from sympy.parsing.sympy_parser import parse_expr

class Expression:
    def __init__(self, formula):
        if self.validate_formula(formula):
            self.formula = parse_expr(formula)

    def validate_formula(self, formula):
        return True
