from flask import abort, request

from src.app import app
from src.mappers.validate_mapper import ValidateMapper, ValidateMapperException
from src.services.result_service import ResultService
from src.utils.logger import Logger
from src.utils.request_decorators import log_request
from src.model.expression import Expression

result_service = ResultService()
logger = Logger.getLogger()
validateMapper = ValidateMapper()

@app.route('/validations/result', methods=['POST'])
@log_request
def validate_result():
    request_data = request.get_json()
    (steps, exercise) = validateMapper.parse_validate_result_input(request_data)
    result = result_service.validate_result(steps, exercise)
    logger.info('Returning the following response: {}'.format(result))
    return "true" if result else "false"

@app.route('/solve-derivative', methods=['POST'])
@log_request
def solve_derivative():
    request_data = request.get_json()
    expression = Expression(request_data['expression'])
    result = result_service.get_derivative_result(expression)
    logger.info('Returning the following response: {}'.format(result))
    return result.to_latex()