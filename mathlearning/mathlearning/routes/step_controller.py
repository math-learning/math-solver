from mathlearning.mappers.validate_mapper import ValidateMapper, ValidateMapperException
from mathlearning.services.step_service import StepService
from mathlearning.utils.logger import Logger
from mathlearning.utils.request_decorators import log_request

step_service = StepService()
logger = Logger.getLogger()
validateMapper = ValidateMapper()

@app.route('/validations/new-step', methods=['POST'])
@log_request
def validate_new_step():
    request_data = request.get_json()
    (new_expression, old_expression, theorems) = validateMapper.parse_validate_new_step_input(request_data)
    result = step_service.is_a_valid_next_step(old_expression,new_expression,theorems)
    logger.info('Returning the following response: {}'.format(result))
    return "true" if result else "false"

@app.route('/validations/not-in-history', methods=['POST'])
@log_request
def validate_not_in_history():
    request_data = request.get_json()
    (expr, history) = validateMapper.parse_validate_not_in_history_input(request_data)
    result = step_service.validate_not_in_history(expr, history)
    logger.info('Returning the following response: {}'.format(result))
    return "true" if result else "false"

@app.route('/expressions/compare', methods=['POST'])
@log_request
def compare_expressions():
    request_data = request.get_json()
    (expr_one, expr_two) = validateMapper.parse_compare_expressions_data(request_data)
    result = expr_one.is_equivalent_to(expr_two)
    logger.info('Returning the following response: {}'.format(result))
    return "true" if result else "false"
