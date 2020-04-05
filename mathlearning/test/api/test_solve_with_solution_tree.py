import json

from rest_framework import status
from rest_framework.test import APITestCase

from mathlearning.mappers.solution_tree_mapper import SolutionTreeMapper
from mathlearning.model.derivative_theorems import DerivativeTheorems
from mathlearning.model.expression import Expression
from test.testutils.solved_exercises import SolvedExercises, SolvedExercise

solution_tree_mapper = SolutionTreeMapper()


def get_solution_tree_broken_nodes(tree_dict):
    result = []
    for branch in tree_dict['branches']:
        try:
            Expression(branch['expression'])
            result += get_solution_tree_broken_nodes(branch)
        except:
            result.append({'before': tree_dict['expression'], 'after': branch['expression'], 'theorem': branch['theorem_applied']})
    return result

def theorem_to_json(theorem):
    return theorem.to_json()


class SolutionTreeAPITest(APITestCase):

    def solve_exercise_with_solution_tree(self, exercise: SolvedExercise):
        derivative_theorems = DerivativeTheorems.get_all()
        theorems = map(theorem_to_json, derivative_theorems)
        data = {
            'problem_input': exercise.steps[0],
            'theorems': theorems,
        }

        response = self.client.post(path='/results/solution-tree', data=data, format='json')

        tree_str = json.loads(response.content)
        #broken_nodes = get_solution_tree_broken_nodes(tree_dict)
        resolve_data = {
            'problem_input': exercise.steps[0],
            'math_tree': tree_str,
            'type': 'derivative',
            'step_list': json.dumps(exercise.steps),
            'current_expression': exercise.steps[-1],
            'theorems': theorems
        }

        response = self.client.post(path='/resolve', data=resolve_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)


    def test_solution_tree_cases_sum_of_two_derivatives(self):
        self.solve_exercise_with_solution_tree(SolvedExercises.derivative_e_plus_sin())
