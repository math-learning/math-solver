from flask import Flask, request, send_from_directory
from src.services.ValidatorService import ValidatorService
import logging
import json
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from collections import namedtuple
from src.model.Theorem import Theorem

app = Flask(__name__, static_folder="static/static", template_folder="static")

validatorService = ValidatorService()


@app.route('/')
def index():
    logging.info('Index')
    return send_from_directory('static', 'index.html')

def create_theorems(theorems):
    parsed_theorems = []
    for theo in theorems:
        theo_object = Theorem(theo.get("name"), parse_expr(theo.get("left")), parse_expr(theo.get("right")))
        parsed_theorems.append(theo_object)
    return parsed_theorems

def parse_validate_input(request_data):
    theorems = request_data['theorems']
    new_expression = request_data['new_expression']
    old_expression = request_data['old_expression']
    sympy_old_expr = parse_expr(old_expression)
    parsed_theorems = create_theorems(theorems)
    sympy_new_expr = None
    try:
        sympy_new_expr = parse_expr("new_expression")
    except:
        print("Invalid new expression")
    finally:
        return (sympy_new_expr, sympy_old_expr, parsed_theorems)


@app.route('/validate', methods=['POST']) 
def validate():
    logging.info(request.form)
    request_data = request.get_json()
    (new_expression, old_expression, theorems) = parse_validate_input(request_data)
    if new_expression == None:
        return "Invalid new expressions"
    result = validatorService.validate_transition(old_expression,new_expression,theorems)
    return "true" if result else "false"


if __name__ == '__main__':
    app.run()

