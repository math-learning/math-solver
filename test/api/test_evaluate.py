import json

from rest_framework import status
from rest_framework.test import APITestCase

from mathlearning.model.expression import Expression

success_cases = [{
  'problem_input': {'expression': 'x^2', 'variables': []},
  'derivative': {'expression': '2 x', 'variables': []}
}, {
  'problem_input': {'expression': 'x^3', 'variables': []},
  'derivative': {'expression': '3 x^{2}', 'variables': []}
}, {
  'problem_input': {'expression': '\\sin(x)', 'variables': []},
  'derivative': {'expression': '\\cos(x)', 'variables': []}
}, {
  'problem_input': {'expression': 'e^x', 'variables': []},
  'derivative': {'expression': 'e^x', 'variables': []}
}, {
  'problem_input': {'expression': '\\cos(x)', 'variables': []},
  'derivative': {'expression': '-\\sin(x)', 'variables': []}
}, {
  'problem_input': {'expression': '\\e^x * x + \\sin(x) * x^{2}', 'variables': []},
  'derivative': {'expression': 'x^2 * \\cos(x) + 2*x*\\sin(x) + x * e^x + e^x', 'variables': []}
}]

# problem_input = "\\frac{d(e^x*x)}{dx} + \\frac{d(sen(x)* x^2)}{dx}"

class APITests(APITestCase):
    def test_evaluate_success(self):

      for problem in success_cases:
        data = {
          'problem_input': problem['problem_input'],
          'type': 'derivative'
        }

        response = self.client.post(path='/validations/evaluate', data=data, format='json')

        body = json.loads(response.content)
        result_expression = Expression(body['result']['expression'], body['result']['variables'])
        expected_expression = Expression(problem['derivative']['expression'], problem['derivative']['variables'])
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertTrue(expected_expression.is_equivalent_to(result_expression))

    def test_evaluate_fails_because_expression(self):
        data = {
          'problem_input': {'expression': '//x', 'variables': []},
          'type': 'derivative'
        }

        response = self.client.post(path='/validations/evaluate', data=data, format='json')

        body = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(body['message'], 'Invalid expression')

    def test_evaluate_fails_because_type(self):
        data = {
          'problem_input': {'expression': 'x^2', 'variables': []},
          'type': 'pepe'
        }

        response = self.client.post(path='/validations/evaluate', data=data, format='json')

        body = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(body['message'], 'Invalid input type')
