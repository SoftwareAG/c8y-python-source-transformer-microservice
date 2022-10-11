from flask_restful import Resource
from utils.rest import check_body_is_json
from utils.rest import log
from flask import jsonify, make_response, request, abort, Flask

from datetime import datetime

import time
import logging
from functools import wraps
from API.inventory import get_internalId_from_externalId


class BaseRequest(Resource):
    logger = logging.getLogger('__main__.' + __name__)
    @log
    def __init__(self):
        pass
    @log
    @check_body_is_json
    def post(self):
        try:
            self.logger.debug(f'Received post in base class, extracting payload.')
            payload = request.get_json(force=True)
            self.logger.debug(f'The following payload was extracted: {payload}')
            # Adding arguments from externailId
            self.logger.debug(f'Extracting the argurments')
            id=request.args.get('externalId','')
            self.logger.debug(f'The extracted argument id is: {id}')
            type=request.args.get('type','')
            self.logger.debug(f'The extracted argument type is: {type}')
            self.logger.debug("Checking if id and type are both not empty")
            if not id or not type:
                self.logger.debug("Either id or type are empty, returning 500.")
                return make_response(jsonify({"message": str("externalId and type is missing as parameter")}),500)
            source = get_internalId_from_externalId(type,id)
            payload["source"] = {"id": source}
            return payload
        except Exception as e:
            self.logger.error(f'Received the following error: {e}. Can not proceed, returning error message and status_code 500.')
            return make_response(jsonify({"message": str(e)}),500)
    @log
    def __del__(self):
        pass