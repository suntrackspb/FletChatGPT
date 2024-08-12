import os
import urllib.request
import urllib.parse
import json
from urllib.error import URLError, HTTPError
import flet as ft


class OpenAI:
    def __init__(self, page: ft.Page, messages: list = None):
        self.page = page
        self.base_url = self.page.client_storage.get('API_URL')
        self.api_key = self.page.client_storage.get('API_KEY')
        self.model = self.page.client_storage.get('GPT_MODEL')

        self.validate_config()

        self.url = f'{self.base_url}/chat/completions'
        self.messages = messages

    def validate_config(self):
        if not bool(self.model):
            self.model = os.getenv('GPT_API_MODEL')
        if not bool(self.base_url) and not bool(self.api_key):
            self.base_url = os.getenv('GPT_API_URL')
            self.api_key = os.getenv('GPT_API_KEY')

    def generate_completion(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": self.model,
            "messages": self.messages,
        }
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(self.url, data=json_data, headers=headers, method='POST')

        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    return json.loads(response.read().decode('utf-8'))
                else:
                    return {"error": response.read().decode('utf-8')}
        except HTTPError as e:
            return {"error": e.read().decode('utf-8')}
        except URLError as e:
            return {"error": str(e)}
