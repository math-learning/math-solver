from flask import Flask, request, send_from_directory

from src.services.ValidatorService import ValidatorService
import json
import logging
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from collections import namedtuple
from src.model.Theorem import Theorem
import sys
from src.mappers.TheoremMapper import TheoremMapper

import pprint


app = Flask(__name__)

app.logger.setLevel(logging.INFO)

validatorService = ValidatorService()
theoremMapper = TheoremMapper()
    

def parse_validate_input(request_data):
    theorems = request_data['theorems']
    new_expression = request_data['new_expression']
    old_expression = request_data['old_expression']
    sympy_old_expr = parse_expr(old_expression, evaluate=False)
    parsed_theorems = theoremMapper.from_json_to_theorems(theorems)
    sympy_new_expr = None
    try:
        sympy_new_expr = parse_expr(new_expression, evaluate=False)
    except:
        app.logger.error("Invalid new expression")
    finally:
        return (sympy_new_expr, sympy_old_expr, parsed_theorems)


@app.route('/validate', methods=['POST']) 
def validate():
    
    app.logger.info("json string: " + json.dumps(request.get_json()))

    request_data = request.get_json()
    (new_expression, old_expression, theorems) = parse_validate_input(request_data)
    if new_expression == None:
        return "Invalid new expressions"
    result = validatorService.validate_transition(old_expression,new_expression,theorems)
    return "true" if result else "false"


if __name__ == '__main__':
    app.run()

