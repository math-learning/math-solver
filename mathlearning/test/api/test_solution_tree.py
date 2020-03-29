import json

from rest_framework import status
from rest_framework.test import APITestCase

from mathlearning.mappers.solution_tree_mapper import SolutionTreeMapper
from mathlearning.model.expression import Expression

solution_tree_mapper = SolutionTreeMapper()

def load_theorems():
    with open("test/jsons/theorems.json", 'r') as theorems_file:
        return json.load(theorems_file)

def get_solution_tree_broken_nodes(tree_dict):
    result = []
    for branch in tree_dict['branches']:
        try:
            Expression(branch['expression'])
            result += get_solution_tree_broken_nodes(branch)
        except:
            result.append({'before': tree_dict['expression'], 'after': branch['expression'], 'theorem': branch['theorem_applied']})
    return result


D_SUMA = "derivada de la suma"
D_PRODUCTO = "derivada del producto"
SIMPLIFICACION = "simplificacion"
RESOLVER_DERIV = "resolver derivadas"
D_DIVISION = "derivada de la division"



sum_of_two_derivatives = {
    "name": "d(e) + d(sen)",
    "problemInput": "\\frac{d(e^x*x)}{dx}*+*\\frac{d(sen(x)*x^2)}{dx}",
    "theorems": {D_PRODUCTO, RESOLVER_DERIV},
    "result": "e^x* (1+x)+\\cos (x)* x^2+\\sin(x)* 2** x",
}

derivative_sen_divided_by_cos = {
    "name": "sen / cos",
    "problemInput": "\\frac{d(\\frac{sen(x)}{\\cos(x)})} {dx}",
    "theorems": {D_DIVISION, SIMPLIFICACION, D_PRODUCTO, RESOLVER_DERIV},
    "result": "\\frac{1}{\\cos^2(x)}",
}

derivative_of_a_multiplication = {
    "name": "deriv suma x + x2 + cos",
    "problemInput": "\\frac{d(x^2)}{dx} +\\frac{d(x*\\cos(x))}{dx}",
    "theorems": {D_PRODUCTO, RESOLVER_DERIV},
    "result": "2* x+1-\\sin (x)",
}

derivative_multiplication = {
    "name": "multiplication of 3 elem",
    "problemInput": "x^2 * \\sin(x) * \\frac{d(\\cos(x))}{dx} + \\cos(x) * \\frac{d(x^2 * \\sin(x))}{dx}",
    "theorems": {D_PRODUCTO, RESOLVER_DERIV, SIMPLIFICACION},
    "result": "x^2\\sin(x)\\frac{d(\\cos(x))}{dx} + \\cos(x) * (\\frac{d(x^2)}{dx} * \\sin(x) + \\frac{d(\\sin(x))}{dx} * x^2)"
}

derivative_inside_cos = {
    "name": "derivative inside cos",
    "problemInput": "x^2 * sin(x) *\\frac{d( cos(x))}{dx}+ cos(x) * \\frac{d(x^2* sin(x))}{dx}",
    "theorems": {D_PRODUCTO, RESOLVER_DERIV, SIMPLIFICACION},
    "result": "cos(\\frac{d(\\cos(x) * x)}{dx})"
}




class APITests(APITestCase):


    def test_solution_tree(self):
        derivative_theorems = load_theorems()
        problem_input = "\\frac{d(e^x*x)}{dx} + \\frac{d(sen(x)* x^2)}{dx}"
        data = {
            'problemInput': problem_input,
            'theorems': derivative_theorems
        }
        response = self.client.post(path='/results/solution-tree', data=data, format='json')

        tree = SolutionTreeMapper.parse(json.loads(response.content))
        theorem_names = tree.get_theorem_names()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(theorem_names, {D_PRODUCTO, RESOLVER_DERIV, SIMPLIFICACION})

    def test_solution_tree_derivative_part(self):
        derivative_theorems = load_theorems()
        problem_input = "\\frac{d(x)}{dx}"
        data = {
            'problemInput': problem_input,
            'theorems': derivative_theorems
        }
        response = self.client.post(path='/results/solution-tree', data=data, format='json')

        tree = SolutionTreeMapper.parse(json.loads(response.content))
        theorem_names = tree.get_theorem_names()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(theorem_names, {RESOLVER_DERIV})


    def test_solution_tree_derivative_part(self):
        derivative_theorems = load_theorems()
        problem_input = "\\frac{d(x)}{dx}"
        data = {
            'problemInput': problem_input,
            'theorems': derivative_theorems
        }
        response = self.client.post(path='/results/solution-tree', data=data, format='json')

        tree = SolutionTreeMapper.parse(json.loads(response.content))
        theorem_names = tree.get_theorem_names()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(theorem_names, {RESOLVER_DERIV})

    def solution_tree_derivative_case(self, case):
        print(case['name'])
        derivative_theorems = load_theorems()
        data = {
            'problemInput': case["problemInput"],
            'theorems': derivative_theorems
        }

        response = self.client.post(path='/results/solution-tree', data=data, format='json')

        tree_dict = json.loads(json.loads(response.content))
        #broken_nodes = get_solution_tree_broken_nodes(tree_dict)
        tree = SolutionTreeMapper.parse(json.loads(response.content))
        theorem_names = tree.get_theorem_names()

        print('Test case: ' + case['name'] + '\n')
        print('Resulting theorems: ' + str(theorem_names) + '\n')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(theorem_names, case["theorems"])

    def test_solution_tree_cases_sum_of_two_derivatives(self):
        self.solution_tree_derivative_case(sum_of_two_derivatives)

    def test_solution_tree_cases_derivative_sen_divided_by_cos(self):
        self.solution_tree_derivative_case(derivative_sen_divided_by_cos)

    def test_solution_tree_cases_derivative_of_a_multiplication(self):
        self.solution_tree_derivative_case(derivative_of_a_multiplication)

    def test_solution_tree_cases_derivative_multiplication(self):
        self.solution_tree_derivative_case(derivative_multiplication)

    def test_solution_tree_cases_derivative_inside_cos(self):
        self.solution_tree_derivative_case(derivative_inside_cos)
