import json
import logging
import os
import urllib.parse
import urllib.request
from typing import List, Optional, Dict, Any
from urllib.error import URLError, HTTPError

import flet as ft


class OpenAI:
    """
    A class to interact with the OpenAI API for generating chat completions.

    Attributes:
        page (ft.Page): The page object containing client storage.
        messages (List[Dict[str, str]]): A list of message dictionaries for the chat model.
    """

    def __init__(self, page: ft.Page, messages: Optional[List[Dict[str, str]]] = None):
        """
        Initializes the OpenAI object with the given page and messages.

        Args:
            page (ft.Page): The page object containing client storage.
            messages (Optional[List[Dict[str, str]]]): A list of message dictionaries for the chat model.
        """
        self.page = page
        self.base_url = self.page.client_storage.get('API_URL')
        self.api_key = self.page.client_storage.get('API_KEY')
        self.model = self.page.client_storage.get('GPT_MODEL')

        self.validate_config()

        self.url = f'{self.base_url}/chat/completions'
        self.messages = messages if messages is not None else []

    def validate_config(self) -> None:
        """
        Validates and sets the configuration for the API URL, API key, and model.
        """
        if not self.model:
            self.model = os.getenv('GPT_API_MODEL')
        if not self.base_url:
            self.base_url = os.getenv('GPT_API_URL')
        if not self.api_key:
            self.api_key = os.getenv('GPT_API_KEY')

    def generate_completion(self) -> Dict[str, Any]:
        """
        Generates a chat completion using the OpenAI API.

        Returns:
            Dict[str, Any]: The response from the API, containing either the result or an error message.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": self.model,
            "messages": self.messages,
        }

        logging.info(f'[CLIENT]: Client connect from IP: {json.dumps(data, ensure_ascii=False)}')

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

