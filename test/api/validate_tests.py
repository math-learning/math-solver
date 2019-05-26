import requests
import json
import os
import webbrowser

SERVER_URL = "http://localhost:5000"


def validate(json_file_path_data, json_file_path_theorems):
    with open(json_file_path_data, 'r') as json_file_data:
        with open(json_file_path_theorems, 'r') as json_file_theorems:
            data = json.load(json_file_data)
            theorems = json.load(json_file_theorems)
            data['theorems'] = theorems['theorems']
            return requests.post(SERVER_URL + "/validations/new-step",json=data)

def testValidateTrue(json_file_path_data, json_file_path_theorems):
        response = validate(json_file_path_data, json_file_path_theorems)
        if response.status_code == 200:
            print(response.content)
        assert(response.status_code == 200)
        is_valid = json.loads(response.content)
        assert(is_valid)

testValidateTrue('jsons/validate_step_one.json', 'jsons/theorems.json')

testValidateTrue('jsons/validate_step_two.json', 'jsons/theorems.json')

testValidateTrue('jsons/validate_step_three.json', 'jsons/theorems.json')

testValidateTrue('jsons/validate_variation.json', 'jsons/theorems.json')

