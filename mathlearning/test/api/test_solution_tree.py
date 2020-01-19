import json

from rest_framework import status
from rest_framework.test import APITestCase

from mathlearning.mappers.solution_tree_mapper import SolutionTreeMapper

solution_tree_mapper = SolutionTreeMapper()

def load_theorems(theorems_path):
    with open(theorems_path, 'r') as theorems_file:
        return json.load(theorems_file)


class APITests(APITestCase):


    def test_solution_tree(self):
        theorems = load_theorems("test/api/jsons/theorems.json")
        problem_input = "\\frac{d\\left(e^x.\\ x\\right)}{dx}\\ +\\ \\frac{d\\left(sen\\left(x\\right)\\cdot x^2\\right)}{dx}"
        data = {
            'problemInput': problem_input,
            'theorems': theorems
        }
        response = self.client.post(path='/results/solution-tree', data=data, format='json')

        tree = SolutionTreeMapper.parse(response.content)
        theorem_names = tree.get_theorem_names()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(theorem_names, {"derivada del producto", "resolver derivadas"})

    def test_solution_tree_derivative_part(self):
        theorems = load_theorems("test/api/jsons/theorems.json")
        problem_input = "\\frac{d\\left(x\\right)}{dx}"
        data = {
            'problemInput': problem_input,
            'theorems': theorems
        }
        response = self.client.post(path='/results/solution-tree', data=data, format='json')

        tree = SolutionTreeMapper.parse(json.loads(response.content))
        theorem_names = tree.get_theorem_names()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(theorem_names, {"resolver derivadas"})
