from resources.base import BaseRequest
from flask_restful import Api, Resource, reqparse
from utils.rest import check_body_is_json
from utils.rest import log
from flask import jsonify, make_response, request, abort
from datetime import datetime
import time
import logging
from API.events import create_event

class Events(BaseRequest):
    logger = logging.getLogger(__name__)
    def __init__(self):
        self.logger.debug(f'Starting init of {__name__}.')
        # Use the init of the baseclass additionally with super
        super().__init__()
        self.url = "/event/events"

    def post(self):
        try:
            payload = super().post()
            statusCode,responseText = create_event(payload)
            make_response(jsonify({"message": str(responseText)}),statusCode)
        except Exception as e:
                self.logger.error(f'Received the following error: {e}. Can not proceed, returning error message and status_code 500.')
                return make_response(jsonify({"message": str(e)}),500)