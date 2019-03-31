from src.app import app
from flask import request
from src.services.HintsService import HintsService
from src.mappers.HintsMapper import HintsMapper
from src.utils.request_decorators import log_request

hints_service = HintsService()
hints_mapper = HintsMapper()


@app.route('/hints/theorems-that-apply', methods=['POST'])
@log_request
def get_theorems_that_apply_hint():
    request_data = request.get_json()
    (expression, theorems) = hints_mapper.map_theorems_that_apply_input(request_data)
    return hints_service.get_theorems_that_apply_hint(expression, theorems)