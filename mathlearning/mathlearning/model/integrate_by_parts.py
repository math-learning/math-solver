from mathlearning.model.expression_variable import ExpressionVariable
from mathlearning.model.theorem import Theorem
from mathlearning.model.template_match_analyzer import TemplateMatchAnalyzer
from mathlearning.model.expression import Expression
from mathlearning.utils.logger import Logger
from sympy.parsing.sympy_parser import parse_expr
from typing import List
from sympy import Integral

from sympy.integrals.manualintegrate import (integral_steps, parts_rule, IntegralInfo)

logger = Logger.getLogger()

class IntegrateByPartsTheorem(Theorem):
    def __init__(self):
        self.name = 'IntegrateByPartsTheorem'
        self.left = None
        self.right = None
        self.conditions = {}
        self.analyzer = TemplateMatchAnalyzer() # TODO: que rayos es esto?

    def there_is_a_chance_to_apply_to(self, expression: Expression):
        if not expression.is_integral():
            return False

        integral_info = IntegralInfo(expression.sympy_expr.function, parse_expr('x'))
        by_parts_rule = parts_rule(integral_info)

        return True if by_parts_rule is not None else False

    # Returns the application possibilities (could be more than 1)
    def apply_to(self, expression: Expression) -> List[Expression]:
        if not expression.is_integral():
            return False

        integral_info = IntegralInfo(expression.sympy_expr.function, parse_expr('x'))
        by_parts_rule = parts_rule(integral_info)

        if by_parts_rule is None:
            # Can not be applied by parts
            return []

        u = by_parts_rule.u
        dv = by_parts_rule.dv
        v = Integral(dv).doit() # TODO Lucas: Buscar si hay una manera menos cochina de hacer esto
        variables = [
            ExpressionVariable('u(x)', Expression(u)),
            ExpressionVariable('v(x)', Expression(v)),
        ]

        main_expression = Expression('u(x) * v(x) - \\int (\\frac{d(u(x))}{dx} * v(x)) dx', variables)
        equivalent_expression = Expression('\\int (u(x) * \\frac{d(v(x))}{dx}) dx', variables)

        #main_expression == Expression('x * cos(x) - \\int (\\frac{d(x)}{dx} * cos(x)) dx')
        #main_expression = Expression('x * cos(x) - \\int (\\frac{d(x)}{dx} * cos(x)) dx', variables)
        # TODO: investigar dx

        #Expression('\\int u * \\frac{d(v)}{dx}', variables)
        # \\int(x * sen(x)) dx + \\int(x * cos(x)) dx
        # \\int(x * sen(x)) dx + POR PARTES(\\int(x * cos(x)) dx)
        # POR PARTES(\\int(x * sen(x)) dx) + \\int(x * cos(x)) dx

        return [
            main_expression,
            equivalent_expression
        ]

    def __str__(self):
        return self.name
