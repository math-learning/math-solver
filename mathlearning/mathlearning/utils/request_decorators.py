from mathlearning.utils.logger import Logger
from functools import wraps
from flask import request
from mathlearning.utils.json_parser import JsonParser

logger = Logger.getLogger()


def log_request(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        logger.info("json string: " + JsonParser.dumps_pretty(request.get_json()))
        return func(*args, **kwargs)

    return decorated_func
