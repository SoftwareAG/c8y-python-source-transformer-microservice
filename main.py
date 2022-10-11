#!flask/bin/python
import logging
logger = logging.getLogger('Logger')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info("Logger was initialized")

from flask import Flask, jsonify, request
from flask_restful import Api
import os
import sys
import json

from resources.events import Events
from resources.alarms import Alarms
from resources.measurements import Measurements 

app = Flask(__name__)
api = Api(app,catch_all_404s=True)
app.config['DEBUG'] = True


logger.debug('Adding Measurements resources')
api.add_resource(Measurements, '/measurement/measurements')
logger.debug('Measurements resources added')

logger.debug('Adding Events resources')
api.add_resource(Events, '/event/events')
logger.debug('Events resources added')

logger.debug('Adding Alarms resources')
api.add_resource(Alarms, '/alarm/alarms')
logger.debug('Alarms resources added')


# Verify the status of the microservice
@app.route('/health')
def health():
    return '{ "status" : "UP" }'

"""# Get environment details
@app.route('/environment')
def environment():
    environment_data = {
        'platformUrl': os.getenv('C8Y_BASEURL'),
        'mqttPlatformUrl': os.getenv('C8Y_BASEURL_MQTT'),
        'tenant': os.getenv('C8Y_BOOTSTRAP_TENANT'),
        'user': os.getenv('C8Y_BOOTSTRAP_USER'),
        'password': os.getenv('C8Y_BOOTSTRAP_PASSWORD'),
        'microserviceIsolation': os.getenv('C8Y_MICROSERVICE_ISOLATION')
    }
    return jsonify(environment_data)"""

if __name__ == '__main__':
    logger.info("Starting")
    app.run(host='0.0.0.0', port=80)