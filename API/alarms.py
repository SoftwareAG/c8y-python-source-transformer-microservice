import logging
logger = logging.getLogger(__name__)
logger.info('Logger for Alarms API was initialised')

import requests
from flask import Flask, jsonify, request
from datetime import datetime, date, time, timedelta
from base64 import b64encode
import API.authentication as auth
import json
from flask import abort, current_app, jsonify, request, make_response

Auth = auth.Authentication()


def create_alarm(payload):
    logger.info('Creating alarm in c8y')
    try:
        logger.debug(f'Received the following payload for sending: {payload}')
        url = "%s/alarm/alarms"%(Auth.tenant)
        Auth.headers['Accept'] = 'application/vnd.com.nsn.cumulocity.alarm+json'            
        response = requests.request("POST", url, headers=Auth.headers, data = json.dumps(payload))
        logger.debug('Sending data to the following url: ' + str(url))
        logger.debug('Response from request: ' + str(response.text))
        logger.debug('Response from request with code : ' + str(response.status_code))
        if response.status_code == 200 or 201:
            logger.debug('Alarm send')
        else:
            logger.warning('Response from request: ' + str(response.text))
            logger.warning('Got response with status_code: ' +
                           str(response.status_code))
        return response.status_code, response.text
    except Exception as e:
        logger.error('The following error occured: %s' % (str(e)))
        return make_response(jsonify({"message": str(e)}),500)

if __name__ == '__main__':
    pass

