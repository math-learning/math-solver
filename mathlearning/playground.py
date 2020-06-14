from sympy.parsing.sympy_parser import parse_expr

from mathlearning.model.expression import Expression

from sympy.integrals.manualintegrate import (
   manualintegrate, _manualintegrate, integral_steps, evaluates,
   ConstantRule, ConstantTimesRule, PowerRule, AddRule, URule,
   PartsRule, CyclicPartsRule, TrigRule, ExpRule, ArctanRule,
   AlternativeRule, DontKnowRule, RewriteRule, integral_steps, parts_rule, IntegralInfo,
   substitution_rule)

steps = integral_steps(parse_expr('(exp(x) / (1 + exp(2 * x))+ x**2 ) - x'), parse_expr('x'))
steps_other = integral_steps(parse_expr('exp(x) / (1 + exp(2 * x))'), parse_expr('x'))
print(steps)

# this returns None if not apply
parts_rule_application = parts_rule(IntegralInfo(parse_expr('x**2*cos(x)'), parse_expr('x')))
parts_rule_application_invalid = parts_rule(IntegralInfo(parse_expr('x'), parse_expr('x')))
parts_rule_application_invalida = parts_rule(IntegralInfo(parse_expr('Derivative(x**2)* cos(x)'), parse_expr('x')))

a = parts_rule_application
# int u * v dx = u. int v - int u' (int v dx) dx
u = str(a.u)
v = str(a.v_step.context)
x = str(a.symbol)

res_step = parse_expr(f'{u} * Integral({v},{x}) - Integral(Derivative({u},{x})* Integral({v},{x}), {x})')
print(f'res_step: {res_step}')
print(steps)


subs = substitution_rule(IntegralInfo(parse_expr('sin(3*x + 5)'), parse_expr('x')))
print(subs)