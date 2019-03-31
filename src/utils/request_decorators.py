from src.utils.Logger import Logger
from functools import wraps
from flask import request
import json

logger = Logger.getLogger()

def log_request(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        logger.info("json string: " + json.dumps(request.get_json()))
        return func(*args, **kwargs)
    return decorated_func