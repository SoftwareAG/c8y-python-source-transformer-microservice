import logging
logger = logging.getLogger(__name__)
logger.info('Logger for Inventory was initialised')

import requests
import json
import API.authentication as auth
from flask import abort, current_app, jsonify, request, make_response

Auth = auth.Authentication()


def get_internalId_from_externalId(type,id):
    logger.info('Checking if external ID exists')
    try:
        url = f'{Auth.tenant}/identity/externalIds/{type}/{id}'
        for i in Auth.headers:
            logger.debug(f'Header infos at position {i} contains: {Auth.headers[i]}')
        response = requests.request("GET", url, headers=Auth.headers)
        logger.debug('Sending data to the following url: ' + str(url))
        logger.debug('Response from request: ' + str(response.text))
        logger.debug('Response from request with code : ' + str(response.status_code))
        if response.status_code == 200 or response.status_code == 201:
            logger.info('Inventory exists')
            logger.info(json.loads(response.text))
            internal_id = json.loads(response.text)['managedObject']['id']
            logger.debug(f'The following internal_id was received: {internal_id}')
            return str(internal_id)
        elif response.status_code == 404:
            logger.error('Device does not exist.')
            return make_response(jsonify({"message": "Device with that identifier and type does not exist."}),404)
        else:
            logger.warning('Response from request: ' + str(response.text))
            logger.warning('Got response with status_code: ' + str(response.status_code))
            return make_response(jsonify({"message": str(response.text)}),response.status_code)
    except Exception as e:
        logger.error('The following error occured: %s' % (str(e)))
        return make_response(jsonify({"message": str(e)}),500)

if __name__ == '__main__':
    pass

