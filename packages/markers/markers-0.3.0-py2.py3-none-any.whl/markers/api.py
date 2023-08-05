from . import __version__
from typing import Dict
import requests, urllib.parse

class Api:
    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.api_url = api_url
        self.version = __version__

    def post(self, uri, data):
        # NOTE: still used for file upload
        params = { 'api_key': self.api_key }
        uri = '/'.join([self.api_url, 'api', uri])
        headers = {'user-agent': f'markers-python/{self.version}'}

        res = requests.post(uri, params=params, json=data, headers=headers)
        res.raise_for_status()

        data = res.json()
        return data

    def graphql(self, query, variables={}) -> Dict:
        params = { 'api_key': self.api_key }
        uri = '/'.join([self.api_url, 'graphql'])
        headers = {'user-agent': f'markers-python/{self.version}'}

        payload = {
            'query': query,
            'variables': variables
        }

        res = requests.post(uri, params=params, json=payload, headers=headers)
        res.raise_for_status()

        data = res.json()
        return data
