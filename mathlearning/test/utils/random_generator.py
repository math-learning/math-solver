import random

single_functions = [{
  'f': 'x',
  'd': '1'
}, {
  'f': 'x^2',
  'd': '2 x'
}, {
  'f': 'x^3',
  'd': '3 x^{2}'
}, {
  'f': '\sin(x)',
  'd': '\cos{\left(x \\right)}'
}, {
  'f': '\cos(x)',
  'd': '- \sin{\left(x \\right)}'
}, {
  'f': '\\tag(x)',
  'd': '- \\tag{\left(x \\right)}'
}, {
  'f': '\exp(x)',
  'd': '\\frac{d}{d x} \operatorname{exp}{\left(x \\right)}'
}]

def generateDerivativeCase(amount):
  first_function = single_functions[random.randint(0, len(single_functions) - 1)]

  complete_function = {
    'f': first_function['f'],
    'd': first_function['d']
  }

  for i in range(amount):
    function = single_functions[random.randint(0, len(single_functions) - 1)]

    complete_function['f'] = complete_function['f'] + ' + ' + function['f']
    complete_function['d'] = complete_function['d'] + ' + ' + function['d']

  return complete_function

