import json

from rest_framework import status
from rest_framework.test import APITestCase

success_cases = [{
  'problem_input': 'x^2',
  'derivative': '2 x'
}, {
  'problem_input': 'x^3',
  'derivative': '3 x^{2}'
}, {
  'problem_input': '\sin(x)',
  'derivative': '\cos{\left(x \\right)}'
}, {
  'problem_input': '\exp(x)',
  'derivative': '\\frac{d}{d x} \operatorname{exp}{\left(x \\right)}'
}, {
  'problem_input': '\cos(x)',
  'derivative': '- \sin{\left(x \\right)}'
}, {
  'problem_input': 'e^x*x + \sen(x)*x^2',
  'derivative': 'e^{x} x \log{\left(e \\right)} + e^{x} + x^{2} \\frac{d}{d x} \operatorname{sen}{\left(x \\right)} + 2 x \operatorname{sen}{\left(x \\right)}'
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
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(body['result'], problem['derivative'])

    def test_evaluate_fails_because_expression(self):
        data = {
          'problem_input': '//x',
          'type': 'derivative'
        }

        response = self.client.post(path='/validations/evaluate', data=data, format='json')

        body = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(body['message'], 'Invalid expression')

    def test_evaluate_fails_because_type(self):
        data = {
          'problem_input': 'x^2',
          'type': 'pepe'
        }

        response = self.client.post(path='/validations/evaluate', data=data, format='json')

        body = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(body['message'], 'Invalid input type')
