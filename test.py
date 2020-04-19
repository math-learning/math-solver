from sympy.core.function import Derivative
from sympy import symbols, diff
from sympy import Integral
from sympy.abc import x, s
from sympy import latex
import random
from sympy.parsing.latex import parse_latex
# from process_latex import process_sympy

# https://github.com/augustt198/latex2sympy

# python3 manage.py test --pattern="*test_evaluate.py"
# python3 mathlearning/manage.py runserver 0.0.0.0:5000


parsed_expression = parse_latex('\\cos{\\left(x \\right)}')

print(parsed_expression)

print(latex(parsed_expression))


# derivative = diff('x^2', 'x')

# print(derivative)

# print(latex(derivative))

# from mathlearning.test.utils.random_generator import generateDerivativeCase

# print(generateDerivativeCase(4))
