from sympy.integrals.manualintegrate import integral_steps
from sympy.parsing.sympy_parser import parse_expr

steps = integral_steps(parse_expr('x + x**2'), parse_expr('x'))
print(steps)

