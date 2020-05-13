from mathlearning.mappers.solution_tree_mapper import SolutionTreeMapper
from mathlearning.mappers.theorem_mapper import TheoremMapper
from mathlearning.mappers.validate_mapper import ValidateMapper, ValidateMapperException
from mathlearning.services.result_service import ResultService
from mathlearning.utils.logger import Logger
from mathlearning.model.expression import Expression
from rest_framework.request import Request

from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json

result_service = ResultService()
logger = Logger.getLogger()
validateMapper = ValidateMapper()
theoremMapper = TheoremMapper()
solutionTreeMapper = SolutionTreeMapper()


@api_view(['POST'])
def solve_derivative(request: Request):
    if request.method == 'POST':
        body = json.loads(request.body)
        expression = Expression(body['expression'])
        result = result_service.get_derivative_result(expression)
        logger.info('Returning the following response: {}'.format(result))
        return Response(result.to_latex(), status=status.HTTP_200_OK)

@api_view(['POST'])
def solution_tree(request: Request):
    if request.method == 'POST':
        body = json.loads(request.body)
        expression = Expression(body['problem_input'])
        theorems = theoremMapper.theorems(body['theorems'])
        result = result_service.solution_tree(expression, theorems)
        result = result.to_json()
        logger.info('Returning the following response: {}'.format(result))
        return Response(json.dumps(result), status=status.HTTP_200_OK, content_type='application/json')


@api_view(['POST'])
def resolve(request: Request):
    if request.method == 'POST':
        body = json.loads(request.body)

        problem_input = Expression(body['problem_input'])
        solution_tree = solutionTreeMapper.parse(body['math_tree'])
        exercise_type = body['type']
        step_list = list(map(lambda expression: Expression(expression), json.loads(body['step_list'])))
        current_expression = Expression(body['current_expression'])
        theorems = theoremMapper.theorems(body['theorems'])

        (result, hints) = result_service.resolve(problem_input, solution_tree, exercise_type, step_list, current_expression, theorems)
        logger.info('Returning the following response: {}'.format(result))

        response_data = {
            'exerciseStatus': result,
            'hints': hints
        }
        return Response(response_data, status=status.HTTP_200_OK, content_type='application/json')


result_paths = [path('results/solve-derivative', solve_derivative)]
result_paths += [path('results/solution-tree', solution_tree)]
result_paths += [path('resolve', resolve)]
