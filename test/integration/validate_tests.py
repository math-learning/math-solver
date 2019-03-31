import requests
import json
import os
import webbrowser

SERVER_URL = "http://localhost:5000"


def validate(data):
    return requests.post(SERVER_URL + "/validations/new-step",json=data)

def testValidateTrue(json_file_path):

    with open(json_file_path, 'r') as json_file: 
        data = json.load(json_file)
        response = validate(data)
        if response.status_code == 200:
            print(response.content)
        assert(response.status_code == 200)
        is_valid = json.loads(response.content)
        assert(is_valid)

testValidateTrue('jsons/validate_step_one.json')

testValidateTrue('jsons/validate_step_two.json')

testValidateTrue('jsons/validate_step_three.json')

testValidateTrue('jsons/validate_variation.json')

