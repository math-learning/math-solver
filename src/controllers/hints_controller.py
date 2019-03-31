import json
from logging import info

from flask import request, jsonify

from src.app import app
from src.mappers.hints_mapper import HintsMapper
from src.services.hints_service import HintsService
from src.utils.request_decorators import log_request
from src.model.theorem import Theorem

from src.utils.json_parser import JsonParser

hints_service = HintsService()
hints_mapper = HintsMapper()

@app.route('/hints/theorems-that-apply', methods=['POST'])
@log_request
def get_theorems_that_apply_hint():
    request_data = request.get_json()
    (expression, theorems) = hints_mapper.map_theorems_that_apply_input(request_data)
    result = hints_service.get_theorems_that_apply_hint(expression, theorems)
    
    res = JsonParser.dumps_pretty(result)
    app.logger.info("Theorems that apply: {}".format(res))
    
    return res