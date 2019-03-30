from src.server import app, log_request
from flask import request, abort
from src.services.ValidatorService import ValidatorService
from src.utils.Logger import Logger
from src.mappers.ValidateMapper import ValidateMapper

validatorService = ValidatorService()
logger = Logger.getLogger
validateMapper = ValidateMapper()

@app.route('/v1/validate', methods=['POST'])
@log_request
def validate_new_step():
    request_data = request.get_json()
    try:
        (new_expression, old_expression, theorems) = parse_validate_input(request_data)
    except:
        logger.error("Invalid new expression")
        abort(404)

    result = validatorService.validate_transition(old_expression,new_expression,theorems)
    logger.info('Returning the following response: {}'.format(result))
    return "true" if result else "false"
