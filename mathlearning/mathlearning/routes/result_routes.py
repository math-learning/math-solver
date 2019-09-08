from mathlearning.mappers.validate_mapper import ValidateMapper, ValidateMapperException
from mathlearning.services.result_service import ResultService
from mathlearning.utils.logger import Logger
from mathlearning.utils.request_decorators import log_request
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

@api_view(['POST'])
def solve_derivative(request: Request):
    if request.method == 'POST':
        body = json.loads(request.body)
        expression = Expression(body['expression'])
        result = result_service.get_derivative_result(expression)
        logger.info('Returning the following response: {}'.format(result))
        return Response(result.to_latex(), status= status.HTTP_200_OK)

result_paths = [path('results/solve-derivative', solve_derivative)]
