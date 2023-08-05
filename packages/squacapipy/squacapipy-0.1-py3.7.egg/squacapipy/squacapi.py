import requests
import os
import json
from squacapipy.errors import APITokenMissingError, APIBaseUrlError


API_TOKEN = os.getenv('SQUAC_API_TOKEN')
API_BASE_URL = os.getenv('SQUAC_API_BASE')


if API_TOKEN is None:
    raise APITokenMissingError(
        "All methods require an API key"
    )

if API_BASE_URL is None:
    raise APIBaseUrlError(
        "All methods require a base API url"
    )

HEADERS = {'Content-Type': 'application/json',
           'Authorization': API_TOKEN}


class Response():
    '''simple custom response object

        takes requests obj text and turns into
        python dict
    '''
    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = body


class Squacapi():
    def __init__(self, app, resource):
        self. app = app
        self.resource = resource

    def uri(self):
        return API_BASE_URL + "/" + self.app + "/" + self.resource + "/"

    def make_response(self, response):
        '''raise for errors, returns Response obj'''
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return Response(e.response.status_code,
                            json.loads(e.response.text))

        return Response(response.status_code,
                        json.loads(response.text))

    def get(self, **kwargs):
        '''return resources object'''
        uri = self.uri()
        response = requests.get(uri, headers=HEADERS, params=kwargs)
        return self.make_response(response)

    def post(self, payload):
        '''create resources'''
        uri = self.uri()
        response = requests.post(uri, headers=HEADERS,
                                 data=json.dumps(payload))
        return self.make_response(response)

    def put(self, id, payload):
        '''update resources'''
        uri = self.uri() + id + "/"
        print(uri)
        print(payload)
        response = requests.put(uri, headers=HEADERS,
                                data=json.dumps(payload))

        return self.make_response(response)


class Nslc(Squacapi):
    def __init__(self, resource):
        app = "nslc"
        super().__init__(app, resource)


class Network(Nslc):
    def __init__(self):
        resource = "networks"
        super().__init__(resource)
