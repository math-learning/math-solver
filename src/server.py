from flask import Flask, request,  abort
from functools import wraps
from collections import namedtuple

import sys
import json
import pprint
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

def log_request(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        app.logger.info("json string: " + json.dumps(request.get_json()))
        return func(*args, **kwargs)
    return decorated_func


if __name__ == '__main__':
    app.run()

