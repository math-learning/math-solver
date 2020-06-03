from mathlearning.model.expression_variable import ExpressionVariable
from mathlearning.model.theorem import Theorem
from mathlearning.model.template_match_analyzer import TemplateMatchAnalyzer
from mathlearning.model.expression import Expression
from mathlearning.utils.logger import Logger
from sympy.parsing.sympy_parser import parse_expr
from typing import List
from sympy import Integral, Derivative, solve

from sympy.integrals.manualintegrate import (substitution_rule, IntegralInfo)

logger = Logger.getLogger()

class IntegrateBySubstitutionDefineUAndDUTheorem(Theorem):
    def __init__(self):
        self.name = 'Integrar por sustitucion definir U y DU'
        self.left = None
        self.right = None
        self.conditions = {}
        self.analyzer = TemplateMatchAnalyzer() # TODO: que rayos es esto?

    def there_is_a_chance_to_apply_to(self, expression: Expression):
        if not expression.is_integral():
            return False

        integral_info = IntegralInfo(expression.sympy_expr.function, parse_expr('x'))
        subs_rule = substitution_rule(integral_info)

        return True if subs_rule is not None else False

    # Returns the application possibilities (could be more than 1)
    def apply_to(self, expression: Expression) -> List[Expression]:
        if not expression.is_integral():
            return False

        integral_info = IntegralInfo(expression.sympy_expr.function, parse_expr('x'))
        subs_rule = substitution_rule(integral_info)

        if subs_rule is None:
            # Can not be applied by parts
            return []

        u = subs_rule.u_func
        du = Derivative(u, subs_rule.symbol).doit()
        variables = [
            ExpressionVariable('u', Expression(u)),
            ExpressionVariable('du', Expression(du)),
        ]

        equivalent_expression = subs_rule.substep.context.xreplace({subs_rule.u_var: parse_expr('u')})
        equivalent_expression = equivalent_expression * subs_rule.constant


        result = Expression(f'Integral({str(equivalent_expression)}, u)', variables, is_latex=False, should_replace=False)

        return [
            result
        ]

    def __str__(self):
        return self.name


class IntegrateBySubstitutionReplaceUAndDUTheorem(Theorem):
    def __init__(self):
        self.name = 'Integrar por sustitucion reemplazar U y DU en la formula'
        self.left = None
        self.right = None
        self.conditions = {}
        self.analyzer = None

    def there_is_a_chance_to_apply_to(self, expression: Expression):
        contains_u = False
        contains_du = False
        for variable in expression.variables:
            if variable.tag == 'u':
                contains_u = True
            if variable.tag == 'du':
                contains_du = True

        return not expression.contains_integral() and contains_du and contains_u

    def apply_to(self, expression: Expression) -> List[Expression]:
        if self.there_is_a_chance_to_apply_to(expression):
            return [expression.replace_variables()]
        return []