from mathlearning.services.theorems_service import TheoremsService
from mathlearning.utils.logger import Logger
from sympy.core.function import Derivative
from sympy.abc import x
from typing import List
from sympy import latex
from sympy import Integral

from sympy.printing.latex import LatexPrinter, print_latex
from sympy.parsing.latex import parse_latex # TODO: cambiar por https://github.com/augustt198/latex2sympy
from mathlearning.model.theorem import Theorem
from mathlearning.model.expression import Expression
from django.core.exceptions import SuspiciousOperation

logger = Logger.getLogger()

class EvaluateService:
    def evaluate_problem_input(self, problem_input, problem_type):
        logger.info("Starting problem input validation")

        sanitized_input = problem_input.replace('\\ ', '')

        if problem_type != 'derivative' and problem_type != 'integral':
            raise SuspiciousOperation('Invalid input type')

        try:
            parsed_expression = parse_latex(sanitized_input)

            if problem_type == 'derivative':
                derivative = Derivative(parsed_expression, 'x')
                return latex(derivative.doit())

            integral = Integral(parsed_expression, x)
            return latex(integral.doit())

        except:
            logger.info("Invalid expression")
            raise SuspiciousOperation('Invalid expression')
