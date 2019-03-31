import requests
import json

SERVER_URL = "http://localhost:5000"

def get_theorems_hint(data):
    
    return requests.post(SERVER_URL + "/hints/theorems-that-apply", json=data)

def test_get_theorems_hint(data, expected_result):
    result = get_theorems_hint(json.loads(data))
    assert(result.status_code == 200)
    if result.status_code == 200 :
        assert(result.data == expected_result)

data = "{\r\n\t\"expression\": \"Derivative(x,x) + Derivative(x,x)\",\r\n\t\"theorems\": [{\r\n\t\t\t\"name\": \"derivada de la suma\",\r\n\t\t\t\"left\": \"Derivative(f(x) + g(x) , x)\",\r\n\t\t\t\"right\": \"Derivative(f(x), x) + Derivative(g(x), x)\"\r\n\t\t},\r\n\t\t{\r\n\t\t\t\"name\": \"derivada del producto\",\r\n\t\t\t\"left\": \"Derivative(f(x) * g(x) , x)\",\r\n\t\t\t\"right\": \"Derivative(f(x), x) * g(x) + Derivative(g(x), x) * f(x)\"\r\n\t\t},\r\n\t\t{\r\n\t\t\t\"name\": \"derivada de la division\",\r\n\t\t\t\"left\": \"Derivative(f(x) \/ g(x) , x)\",\r\n\t\t\t\"right\": \"Derivative(( f(x), x) * g(x) - Derivative(g(x), x) * f(x)) \/ ( g(x)** 2)\"\r\n\t\t}\r\n\t]\r\n}"
test_get_theorems_hint(data, "")