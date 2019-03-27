import requests
import json

SERVER_URL = "http://localhost:5000"

json_data = "{\r\n\t\"old_expression\": \"Derivative(x,x) + Derivative(x,x)\",\r\n\t\"new_expression\": \"Derivative(x + x ,x)\",\r\n\t\"theorems\": [{\r\n\t\t\t\"name\": \"derivada de la suma\",\r\n\t\t\t\"left\": \"Derivative(f(x) + g(x) , x)\",\r\n\t\t\t\"right\": \"Derivative(f(x), x) + Derivative(g(x), x)\"\r\n\t\t},\r\n\t\t{\r\n\t\t\t\"name\": \"derivada del producto\",\r\n\t\t\t\"left\": \"Derivative(f(x) * g(x) , x)\",\r\n\t\t\t\"right\": \"Derivative(f(x), x) * g(x) + Derivative(g(x), x) * f(x)\"\r\n\t\t},\r\n\t\t{\r\n\t\t\t\"name\": \"derivada de la division\",\r\n\t\t\t\"left\": \"Derivative(f(x) \/ g(x) , x)\",\r\n\t\t\t\"right\": \"Derivative(( f(x), x) * g(x) - Derivative(g(x), x) * f(x)) \/ ( g(x)** 2)\"\r\n\t\t}\r\n\t]\r\n}"

def validate(data):
    return requests.post(SERVER_URL + "/validate",json=data)



response = validate(json.loads(json_data))
print(response)