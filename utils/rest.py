from flask import abort, current_app, jsonify, request, make_response
import json
import logging
from functools import wraps



logger = logging.getLogger(__name__)


def check_body_is_json(function):
    
    @wraps(function)
    def validated_json(*args, **kwargs):
        logging.debug(f'Checking that the following data is a valid json object: {request.get_data()}')
        try:
            json.loads(request.get_data())
            logging.debug(f'Data is valid json')
            return function(*args, **kwargs)
        except ValueError as err:
            logging.debug(f'Data is not a valid json, received the following error: {err}')
            return make_response(jsonify({"message": "Data is not a valid json"}),400)
    return validated_json

def log(orig_func):

    @wraps(orig_func)
    def wrapper(self,*args, **kwargs):
        self.logger.debug(f'Ran the function "{orig_func.__name__}" in {type(self).__name__} from {type(self).__module__} with args: {args}, and kwargs: {kwargs}')
        return orig_func(self,*args, **kwargs)
    return wrapper