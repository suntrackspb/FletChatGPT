import json
import time
import urllib.request
import urllib.parse

import requests


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        req = urllib.request.Request(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            return data[0]['id']

    @staticmethod
    def get_styles():
        req = urllib.request.Request('https://cdn.fusionbrain.ai/static/styles/api')
        with urllib.request.urlopen(req) as response:
            return [x['name'] for x in json.loads(response.read())]

    def generate(self, prompt, model, negative='', images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "negativePromptUnclip": negative,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }

        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        # print(data)
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            print(data)
            if data['status'] == 'DONE':
                return data['images']
            if data['status'] == 404:
                return None

            attempts -= 1
            time.sleep(delay)
