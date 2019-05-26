import requests
import json

SERVER_URL = "http://localhost:5000"


def get_theorems_hint(data):
    return requests.post(SERVER_URL + "/hints/theorems-that-apply", json=data)


def test_get_theorems_hint(json_file_path, json_file_path_theorems, expected_result):
     with open(json_file_path, 'r') as json_file:
         with open(json_file_path_theorems, 'r') as json_file_theorems:
            data = json.load(json_file)
            thoerems = json.load(json_file_theorems)
            data['theorems'] = thoerems['theorems']
            result = get_theorems_hint(data)
            assert(result.status_code == 200)
            if result.status_code == 200 :
                print(result)
                print(result.text)
                assert(json.loads(result.text) == expected_result)


test_get_theorems_hint('jsons/hints_example_one.json', 'jsons/theorems.json',[
        {
            "left": "Derivative(a*f(x), x)",
            "name": "Derivada por un numero real",
            "right": "2*Derivative(x, x)"
        }
    ])