#from API import measurement
from resources.base import BaseRequest
from flask_restful import Api, Resource, reqparse
from utils.rest import log
from flask import jsonify, make_response, request, abort
from datetime import datetime
import time
import logging

from API.measurements import create_measurement

class Measurements(BaseRequest):
    logger = logging.getLogger(__name__)
    def __init__(self):
        self.logger.debug(f'Starting init of {__name__}.')
        # Use the init of the baseclass additionally with super
        super().__init__()
        self.url = "/measurement/measurements"

    @log
    def post(self):
        try:
            # Starting the initial post of the base class
            self.payload = super().post()
            self.logger.debug("Checking if payload is not a Response.")
            try:
                self.status_code = self.payload.status_code
                self.logger.debug("Payload from base class is a Response object, returning reponse object direct.")
                return self.payload
            except:
                self.logger.debug("Payload is not a response object.")
                self.logger.debug(f'The following payload is used to create the c8y measurment: {self.payload}')
                self.statusCode,self.responseText = create_measurement(self.payload)
                self.logger.debug(f'Received status code {self.statusCode} and text {self.responseText}.')
                return make_response(jsonify({"message": str(self.responseText)}),self.statusCode)
        except Exception as e:
                self.logger.error(f'Received the following error: {e}. Can not proceed, returning error message and status_code 500.')
                return make_response(jsonify({"messsage": str(e)}),500)
