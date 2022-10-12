from flask_restful import Resource
from utils.rest import check_body_is_json
from utils.rest import log
from flask import jsonify, make_response, request, abort, Flask

from datetime import datetime
from cacheout import Cache

import logging
import time
from functools import wraps
from API.inventory import get_internalId_from_externalId

cache = Cache(maxsize=1024, ttl=0, timer=time.time, default=None)
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
            self.payload = request.get_json(force=True)
            self.logger.debug(f'The following payload was extracted: {self.payload}')
            # Adding arguments from externailId
            self.logger.debug(f'Extracting the argurments')
            self.id=request.args.get('externalId','')
            self.logger.debug(f'The extracted argument id is: {self.id}')
            self.type=request.args.get('type','')
            self.logger.debug(f'The extracted argument type is: {self.type}')
            self.logger.debug("Checking if id and type are both not empty")
            if not self.id or not self.type:
                self.logger.debug("Either id or type are empty, returning 500.")
                return make_response(jsonify({"message": str("externalId and/or type is missing as parameter")}),500)
            # Creating a json string that contains the id and the type such that if the interal id was already queried there is no need to requery it.
            self.logger.debug("Creating the json string to validate with cache.")
            self.cache_key = str({"id": self.id, "type": self.type})
            self.logger.debug(f'The json string for cache looks: {self.cache_key}.')
            if cache.get(self.cache_key):
                self.logger.debug("Cache does contain the internal id already.")
                self.source = cache.get(self.cache_key)
                self.logger.debug(f'The internal id from cache is: {self.source}')
            else:
                self.logger.debug("Cache does not contain the internal id, query it from identity API.")
                self.source = get_internalId_from_externalId(self.type,self.id)
                cache.set(self.cache_key,self.source)
                self.logger.debug(f'The following internal id was written to cache: {self.source}')
            try:
                self.logger.debug(f'Checking if source is an response object or an real externalId.')
                self.status_code = self.source.status_code
                self.logger.debug(f'Received the following status code {self.status_code} from {__name__}, returning response object.')
                return self.source
            except:
                self.payload["source"] = {"id": self.source}
                return self.payload
        except Exception as e:
            self.logger.error(f'Received the following error: {e}. Can not proceed, returning error message and status_code 500.')
            return make_response(jsonify({str(e)}),500)
    @log
    def __del__(self):
        pass