import requests
import json

SERVER_URL = "http://localhost:5000"

def get_theorems_hint(data):
    
    return requests.post(SERVER_URL + "/hints/theorems-that-apply", json=data)

def test_get_theorems_hint(json_file_path, expected_result):
     with open(json_file_path, 'r') as json_file: 
        data = json.load(json_file)
        result = get_theorems_hint(data)
        assert(result.status_code == 200)
        if result.status_code == 200 :
            print(result)
            print(json.dumps(result.content.__dict__))
            assert(json.loads(result.content) == expected_result)

test_get_theorems_hint('jsons/hints_example_one.json', [])