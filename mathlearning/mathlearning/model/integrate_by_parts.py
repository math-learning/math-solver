from mathlearning.model.theorem import Theorem
from mathlearning.model.template_match_analyzer import TemplateMatchAnalyzer
from mathlearning.model.expression import Expression
from mathlearning.utils.logger import Logger
from typing import List
from sympy.parsing.sympy_parser import parse_expr

from mathlearning.model.template_match_analyzer import Equality
import sympy
from typing import Union

from sympy import Integral


from sympy.integrals.manualintegrate import (
    integral_steps, parts_rule, IntegralInfo
)

logger = Logger.getLogger()

class IntegrateByPartsTheorem(Theorem):
    def __init__(self):
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

        u = Integral(by_parts_rule.u)
        dv = by_parts_rule.dv
        v = Integral(dv).doit() # Buscar si hay una manera menos cochina de hacer esto

        main_expression = Expression('u * v - \\int (\\frac{d(u)}{dx} * v)', u, v)

        return [main_expression]

    def __str__(self):
        return self.name
