from sympy import Symbol
from sympy.core.function import UndefinedFunction

from src.comparators.ComparisonResult import ComparisonResult


class UserDefinedFunctionComparator:

    def compare(self, structure, expression, equalities):
        print("comparing user defined function")
        if self.user_defined_function_match(structure, expression):
            return ComparisonResult(True, equalities + [[structure, expression]])
        else:
            return ComparisonResult(False, [])

    def user_defined_function_match(self, expression, structure):
        for free_symbol in expression.expr_free_symbols:
            if free_symbol.func == Symbol:
                if not structure.has(free_symbol):
                    return False
        return True

    def is_user_defined_function(self, structure):
        return isinstance(structure.func, UndefinedFunction)

    def contains_user_defined_function(self, expression):
        for arg in expression.args:
            if self.is_user_defined_function(arg):
                return True
        return False
