#!flask/bin/python
import logging
from pickle import FALSE
logger = logging.getLogger('Logger')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info("Logger was initialized")

from flask import Flask, jsonify, request
from flask_restful import Api
import os
import sys
import json
import pyfiglet
from resources.events import Events
from resources.alarms import Alarms
from resources.measurements import Measurements 

app = Flask(__name__)
api = Api(app,catch_all_404s=True)
app.config['DEBUG'] = FALSE


logger.debug('Adding Measurements resources')
api.add_resource(Measurements, '/measurement/measurements')
logger.debug('Measurements resources added')

logger.debug('Adding Events resources')
api.add_resource(Events, '/event/events')
logger.debug('Events resources added')

logger.debug('Adding Alarms resources')
api.add_resource(Alarms, '/alarm/alarms')
logger.debug('Alarms resources added')

def print_banner():
    logger.info(pyfiglet.figlet_format("Source Transformator"))
    logger.info("Author:\t\tMurat Bayram")
    logger.info("Date:\t\t12th October 2022")
    logger.info("Description:\tA service that transforms the source to the internalId while given the externalId via arguements.")
    logger.info("Documentation:\tPlease refer to the c8y-documentation wiki to find service description")


# Verify the status of the microservice
@app.route('/health')
def health():
    return '{ "status" : "UP" }'

# Get environment details
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
    return jsonify(environment_data)

if __name__ == '__main__':
    logger.info("Starting")
    print_banner()
    app.run(host='0.0.0.0', port=80)