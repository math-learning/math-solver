from mathlearning.mappers.validate_mapper import ValidateMapper, ValidateMapperException
from mathlearning.services.result_service import ResultService
from mathlearning.utils.logger import Logger
from mathlearning.utils.request_decorators import log_request
from mathlearning.model.expression import Expression

from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
import json

result_service = ResultService()
logger = Logger.getLogger()
validateMapper = ValidateMapper()


def bool_to_str(boolean_value):
    return "true" if boolean_value else "false"


@api_view(['POST'])
def compare_expressions(request: Request):
    if request.method == 'POST':
        body = json.loads(request.body)
        (expr_one, expr_two) = validateMapper.parse_compare_expressions_data(body)
        result = expr_one.is_equivalent_to(expr_two)
        logger.info('Returning the following response: {}'.format(result))
        return Response(data=bool_to_str(result), status=status.HTTP_200_OK)


comparison_paths = [path('compare', compare_expressions)]
