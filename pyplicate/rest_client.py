import json
import logging
import requests
from .utils import base64encode, api_url_joiner, default_logger


log = default_logger(__name__)

class AttunityRestAPI(object):

    def __init__(self, url, username=None, password=None, domain=None, api_token=None, api_root='/attunityenterprisemanager/api/v1/', session=None, debug=None):
        self.url = url
        self.username = username
        self.password = password
        self.domain = domain
        self.api_root = api_root
        self.api_link = url + api_root
        self.debug = debug

        if session is None:
            self._session = requests.Session()
        else: 
            self._session = session
        
        if api_token is None:
            auth_headers = {
            'Authorization': 'Basic '+ base64encode(username=username, password=password, domain=domain)
            }
        else:
            auth_headers = {
                'Authorization': 'Basic '+ api_token
            }
        
        response = self._session.get(url=self.api_link+'login', headers=auth_headers, verify=False)

        if response.status_code == 200:
            session_id=response.headers.get('EnterpriseManager.APISessionID')
            self._session.headers.update({
                'EnterpriseManager.APISessionID': session_id
                })
        else:
            if self.debug == True:
                log.error(f'Authentication failed. Received response: {self._session.response.text}')
            print("Error: Response code: " + response.status.code) 

        
    def request(self, method=None, path='/', data=None, headers=None):
        
        if method is None:
            raise AttributeError("Must specify method input. Got 'None'")
        
        url = api_url_joiner(self.api_link,path)
        headers = headers or self._session.headers

        response = self._session.request(
            method = method,
            url = url,
            headers=headers
        )

        try:
            if response.text:
                response_content = response.json()
            else:
                response_content = response.content
        except ValueError:
            if self.debug == True:
                log.debug(f"Value Error on Response: Received: {response.status_code} & content: {response_content}")
            print(f"Value Error on Response: Received: {response.status_code} & content: {response_content}")
        
        if self.debug == True:
            if response.status_code == 200:
                log.info('Received: {0}\n {1}'.format(response.status_code, response_content))
            elif response.status_code == 201:
                log.info('Received: {0}\n "Created" response'.format(response.status_code))
            elif response.status_code == 204:
                log.debug('Received: {0}\n "No Content" response'.format(response.status_code))
            elif response.status_code == 400:
                log.error('Received: {0}\n Bad request \n {1}'.format(response.status_code, response_content))
            elif response.status_code == 401:
                log.error('Received: {0}\n "UNAUTHORIZED" response'.format(response.status_code))
            elif response.status_code == 404:
                log.error('Received: {0}\n Not Found'.format(response.status_code))
            elif response.status_code == 403:
                log.error('Received: {0}\n Forbidden. Please, check permissions'.format(response.status_code))
            elif response.status_code == 405:
                log.error('Received: {0}\n Method not allowed'.format(response.status_code))
            elif response.status_code == 409:
                log.error('Received: {0}\n Conflict \n {1}'.format(response.status_code, response_content))
            elif response.status_code == 413:
                log.error('Received: {0}\n Request entity too large'.format(response.status_code))
            else:
                log.info('Received: {0}\n {1}'.format(response.status_code, response))
                log.error(response_content)
                try:
                    response.raise_for_status()
                except requests.exceptions.HTTPError as err:
                    log.error("HTTP Error occurred")
                    log.error('Response is: {content}'.format(content=err.response.content))


        return response_content