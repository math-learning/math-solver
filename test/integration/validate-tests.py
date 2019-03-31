import requests
import json
import os
import webbrowser

SERVER_URL = "http://localhost:5000/v1"


def validate(data):
    return requests.post(SERVER_URL + "/validate",json=data)


def testValidateTrue(json_data):
    response = validate(json.loads(json_data))
    
    if response.status_code == 200:
        print(response.content)
    # else:
    #     path = os.path.abspath('temp.html')
    #     url = 'file://' + path

    #     with open(path, 'w') as f:
    #         f.write(str(response.content))
    #     webbrowser.open(url)
    assert(response.status_code == 200)
    is_valid = json.loads(response.content)
    assert(is_valid)

first_step_json = "{\r\n\t\"new_expression\": \"Derivative(x,x) + Derivative(x,x)\",\r\n\t\"old_expression\": \"Derivative(x + x ,x)\",\r\n\t\"theorems\": [{\r\n\t\t\t\"name\": \"derivada de la suma\",\r\n\t\t\t\"left\": \"Derivative(f(x) + g(x) , x)\",\r\n\t\t\t\"right\": \"Derivative(f(x), x) + Derivative(g(x), x)\"\r\n\t\t},\r\n\t\t{\r\n\t\t\t\"name\": \"derivada del producto\",\r\n\t\t\t\"left\": \"Derivative(f(x) * g(x) , x)\",\r\n\t\t\t\"right\": \"Derivative(f(x), x) * g(x) + Derivative(g(x), x) * f(x)\"\r\n\t\t},\r\n\t\t{\r\n\t\t\t\"name\": \"derivada de la division\",\r\n\t\t\t\"left\": \"Derivative(f(x) \/ g(x) , x)\",\r\n\t\t\t\"right\": \"Derivative(( f(x), x) * g(x) - Derivative(g(x), x) * f(x)) \/ ( g(x)** 2)\"\r\n\t\t}\r\n\t]\r\n}"
testValidateTrue(first_step_json)

second_step_json = "{\r\n\t\"new_expression\": \"1 + 1\",\r\n\t\"old_expression\": \"Derivative(x,x) + Derivative(x,x)\",\r\n\t\"theorems\": [{\r\n\t\t\t\"name\": \"derivada de la suma\",\r\n\t\t\t\"left\": \"Derivative(f(x) + g(x) , x)\",\r\n\t\t\t\"right\": \"Derivative(f(x), x) + Derivative(g(x), x)\"\r\n\t\t},\r\n\t\t{\r\n\t\t\t\"name\": \"derivada del producto\",\r\n\t\t\t\"left\": \"Derivative(f(x) * g(x) , x)\",\r\n\t\t\t\"right\": \"Derivative(f(x), x) * g(x) + Derivative(g(x), x) * f(x)\"\r\n\t\t},\r\n\t\t{\r\n\t\t\t\"name\": \"derivada de la division\",\r\n\t\t\t\"left\": \"Derivative(f(x) \/ g(x) , x)\",\r\n\t\t\t\"right\": \"Derivative(( f(x), x) * g(x) - Derivative(g(x), x) * f(x)) \/ ( g(x)** 2)\"\r\n\t\t}\r\n\t]\r\n}"
testValidateTrue(second_step_json)

third_step_json = "{\r\n\t\"new_expression\": \"2\",\r\n\t\"old_expression\": \"1 + 1\",\r\n\t\"theorems\": [{\r\n\t\t\t\"name\": \"derivada de la suma\",\r\n\t\t\t\"left\": \"Derivative(f(x) + g(x) , x)\",\r\n\t\t\t\"right\": \"Derivative(f(x), x) + Derivative(g(x), x)\"\r\n\t\t},\r\n\t\t{\r\n\t\t\t\"name\": \"derivada del producto\",\r\n\t\t\t\"left\": \"Derivative(f(x) * g(x) , x)\",\r\n\t\t\t\"right\": \"Derivative(f(x), x) * g(x) + Derivative(g(x), x) * f(x)\"\r\n\t\t},\r\n\t\t{\r\n\t\t\t\"name\": \"derivada de la division\",\r\n\t\t\t\"left\": \"Derivative(f(x) \/ g(x) , x)\",\r\n\t\t\t\"right\": \"Derivative(( f(x), x) * g(x) - Derivative(g(x), x) * f(x)) \/ ( g(x)** 2)\"\r\n\t\t}\r\n\t]\r\n}"
testValidateTrue(third_step_json)

variant_json = "{\r\n\t\"new_expression\": \" 2 \",\r\n\t\"old_expression\": \"Derivative(x,x) + Derivative(x,x)\",\r\n\t\"theorems\": [{\r\n\t\t\t\"name\": \"derivada de la suma\",\r\n\t\t\t\"left\": \"Derivative(f(x) + g(x) , x)\",\r\n\t\t\t\"right\": \"Derivative(f(x), x) + Derivative(g(x), x)\"\r\n\t\t},\r\n\t\t{\r\n\t\t\t\"name\": \"derivada del producto\",\r\n\t\t\t\"left\": \"Derivative(f(x) * g(x) , x)\",\r\n\t\t\t\"right\": \"Derivative(f(x), x) * g(x) + Derivative(g(x), x) * f(x)\"\r\n\t\t},\r\n\t\t{\r\n\t\t\t\"name\": \"derivada de la division\",\r\n\t\t\t\"left\": \"Derivative(f(x) \/ g(x) , x)\",\r\n\t\t\t\"right\": \"Derivative(( f(x), x) * g(x) - Derivative(g(x), x) * f(x)) \/ ( g(x)** 2)\"\r\n\t\t}\r\n\t]\r\n}"
testValidateTrue(variant_json)

