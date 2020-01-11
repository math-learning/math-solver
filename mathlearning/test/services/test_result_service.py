import unittest
import json

from mathlearning.mappers.theorem_mapper import TheoremMapper
from mathlearning.model.expression import Expression
from mathlearning.services.result_service import ResultService


def load_theorems():
    with open('../jsons/theorems.json', 'r') as theorems_file:
        return json.load(theorems_file)

class TestResultService(unittest.TestCase):

    def test_solution_tree(self):
        service = ResultService()
        theorems = load_theorems()
        theorem_mapper = TheoremMapper()
        processed_theorems = theorem_mapper.theorems(theorems)
        result = service.solution_tree(
            Expression("\\frac{d\\left(e^x.\\ x\\right)}{dx}\\ +\\ \\frac{d\\left(sen\\left(x\\right)\\cdot x^2\\right)}{dx}"),
            processed_theorems)
        print("============= RESULTADO ===============")
        result.explain_solution(0)


