import requests
import json
import os
import webbrowser

SERVER_URL = "http://localhost:5000"


def validate_result(data):
    return requests.post(SERVER_URL + "/validations/result",json=data)

def testValidateTrue(json_file_path,json_file_path_theorems):

    with open(json_file_path, 'r') as json_file_data: 
        with open(json_file_path_theorems, 'r') as json_file_theorems:
            data = json.load(json_file_data)
            theorems = json.load(json_file_theorems)
            data['exercise']['theorems'] = theorems['theorems']
            response = validate_result(data)
            if response.status_code == 200:
                print(response.content)
            assert(response.status_code == 200)
            is_valid = json.loads(response.content)
            assert(is_valid)

testValidateTrue('jsons/result_one.json', 'jsons/theorems.json')
