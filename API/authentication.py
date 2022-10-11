import logging
logger = logging.getLogger(__name__)
logger.info('Logger for authentication was initialized')
import os
from base64 import b64encode
from urllib.request import Request
from urllib.request import urlopen
import urllib.request, json, base64
from flask import Flask, jsonify, request


# values provided into environment by cumulocity platform during deployment
logger.debug("Extracting User, Tenant, URL and Password from ENV")
C8Y_BASEURL = os.getenv('C8Y_BASEURL')
C8Y_BOOTSTRAP_USER = os.getenv('C8Y_BOOTSTRAP_USER')
C8Y_BOOTSTRAP_TENANT = os.getenv('C8Y_BOOTSTRAP_TENANT')
C8Y_BOOTSTRAP_PASSWORD = os.getenv('C8Y_BOOTSTRAP_PASSWORD')
logger.debug(f'C8Y_BASEURL: {C8Y_BASEURL}')
logger.debug(f'C8Y_BOOTSTRAP_USER: {C8Y_BOOTSTRAP_USER}')
logger.debug(f'C8Y_BOOTSTRAP_TENANT: {C8Y_BOOTSTRAP_TENANT}')
logger.debug(f'C8Y_BOOTSTRAP_PASSWORD: {C8Y_BOOTSTRAP_PASSWORD}')

class Authentication(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug('Logger for authentication was initialised')
        self.logger.debug('Starting get_authorization')
        self.auth = self.get_authorization()
        self.logger.debug(f'Got auth: {self.auth}')
        self.logger.debug('Getting tenantID')
        self.tenantID = os.getenv('C8Y_BOOTSTRAP_TENANT')
        self.logger.debug(f'TenantID is: {self.tenantID}')
        self.logger.debug('Getting Base URL')
        self.tenant = C8Y_BASEURL
        self.logger.debug(f'Base URL is: {self.tenant}')
        self.payload = {}
        self.headers = {}
        self.headers['Authorization'] = self.auth
        self.headers['Content-Type'] = 'application/json'
        self.headers['Accept'] = 'application/json'
        for i in self.headers:
            self.logger.debug(f'Header infos at position {i} contains: {self.headers[i]}')


    def base64_credentials(self, tenant, user, password):
        str_credentials = tenant + "/" + user + ":" + password
        self.logger.debug(f'Returning {str_credentials}, which equals in base64: {base64.b64encode(str_credentials.encode()).decode()}')
        return 'Basic ' + base64.b64encode(str_credentials.encode()).decode()


    def get_subscriber_for(self, tenant_id):
        req = Request(C8Y_BASEURL + '/application/currentApplication/subscriptions')
        self.logger.debug(f'Creating request URL to: {C8Y_BASEURL}/application/currentApplication/subscriptions')
        self.logger.debug("Adding Accept Header")
        req.add_header('Accept', 'application/vnd.com.nsn.cumulocity.applicationUserCollection+json')
        self.logger.debug("Adding Authorization Header")
        req.add_header('Authorization', self.base64_credentials(C8Y_BOOTSTRAP_TENANT, C8Y_BOOTSTRAP_USER, C8Y_BOOTSTRAP_PASSWORD))
        response = urlopen(req)
        subscribers = json.loads(response.read().decode())["users"]
        self.logger.debug(subscribers)
        return [s for s in subscribers if s["tenant"] == tenant_id][0]

    
    def get_authorization(self):
        self.logger.debug("Extracting Tenant ID")
        tenant_id = os.getenv('C8Y_BOOTSTRAP_TENANT')
        self.logger.debug(f'Tenant ID is: {tenant_id}, handing tenant Id over to get subscriber')
        subscriber = self.get_subscriber_for(tenant_id)
        self.logger.debug(f'Received subsriber as: {subscriber}')
        self.logger.debug(f'Creating auth object with name, tenant and password from subscriber')
        auth = self.base64_credentials(subscriber["tenant"], subscriber["name"], subscriber["password"])
        return auth
    
    

if __name__ == '__main__':
    pass
