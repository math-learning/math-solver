from src.app import app
from src.utils.request_decorators import log_request 
from flask import request, abort
from src.services.validator_service import ValidatorService
from src.utils.logger import Logger
from src.mappers.validate_mapper import ValidateMapper, ValidateMapperException

validatorService = ValidatorService()
logger = Logger.getLogger()
validateMapper = ValidateMapper()

@app.route('/validations/new-step', methods=['POST'])
@log_request
def validate_new_step():
    request_data = request.get_json()

    (new_expression, old_expression, theorems) = validateMapper.parse_validate_new_step_input(request_data)
    
    result = validatorService.is_a_valid_next_step(old_expression,new_expression,theorems)

    logger.info('Returning the following response: {}'.format(result))
    return "true" if result else "false"

@app.route('/validations/result', methods=['POST'])
@log_request
def validate_result():
    request_data = request.get_json()

    (result, input_expression, theorems) = validateMapper.parse_validate_result_input(request_data)
    
    result = validatorService.validate_result(result, input_expression, theorems)

    logger.info('Returning the following response: {}'.format(result))
    return "true" if result else "false"
