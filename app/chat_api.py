import urllib.request
import urllib.parse
import json
from urllib.error import URLError, HTTPError


class OpenAI:
    def __init__(self, url: str, key: str, messages: list = None):
        self.url = f'{url}/chat/completions'
        self.key = key
        self.messages = messages

    def generate_completion(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.key}"
        }
        data = {
            "model": "gpt-3.5-turbo",
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
