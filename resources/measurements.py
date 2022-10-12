#from API import measurement
from resources.base import BaseRequest
from flask_restful import Api, Resource, reqparse
from utils.rest import check_body_is_json
from utils.rest import log
from flask import jsonify, make_response, request, abort
from datetime import datetime
import time
import logging

from API.measurements import create_measurement
from API.inventory import get_internalId_from_externalId

class Measurements(BaseRequest):
    logger = logging.getLogger(__name__)
    def __init__(self):
        self.logger.debug(f'Starting init of {__name__}.')
        # Use the init of the baseclass additionally with super
        super().__init__()
        self.url = "/measurement/measurements"

    def post(self):
        try:
            payload = super().post()
            self.logger.debug(type(payload))
            if type(payload) == 'Response':
                return payload
            else:
                statusCode,responseText = create_measurement(payload)
                make_response(jsonify({"message": str(responseText)}),statusCode)
        except Exception as e:
                self.logger.error(f'Received the following error: {e}. Can not proceed, returning error message and status_code 500.')
                return make_response(jsonify({"message": str(e)}),500)
