import json
import logging
import os
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import List, Optional, Any, Literal

import flet as ft
import requests


@dataclass
class ImageData:
    status: Literal['DONE', 'ERROR', 'CENSORED']
    image: List[str] | None = None


class Text2ImageAPI:
    """
    A class to interact with the Text-to-Image API.

    Attributes:
        page (ft.Page): The Flet page object.
        URL (str): Base URL for the API.
        api_key (str): API key for authentication.
        api_secret (str): API secret for authentication.
        AUTH_HEADERS (dict): Authentication headers.
    """

    def __init__(self, page: ft.Page):
        """
        Initializes the Text2ImageAPI with a Flet page.

        Args:
            page (ft.Page): The Flet page object.
        """
        self.page = page
        self.URL = "https://api-key.fusionbrain.ai/"
        self.api_key = self.page.client_storage.get('IMG_KEY')
        self.api_secret = self.page.client_storage.get('IMG_SECRET')

        self.validate_config()

        self.AUTH_HEADERS = {
            'X-Key': f'Key {self.api_key}',
            'X-Secret': f'Secret {self.api_secret}',
        }

    def validate_config(self) -> None:
        """
        Validates and sets the API key and secret from environment variables if not set.
        """
        if not bool(self.api_key) and not bool(self.api_secret):
            self.api_key = os.getenv('KANDINSKY_KEY')
            self.api_secret = os.getenv('KANDINSKY_SECRET')

    def get_model(self) -> str:
        """
        Retrieves the model ID from the API.

        Returns:
            str: The model ID.
        """
        req = urllib.request.Request(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            return data[0]['id']

    @staticmethod
    def get_styles() -> List[str]:
        """
        Retrieves available styles from the API.
        Returns:
            List[str]: A list of style names.
        """
        req = urllib.request.Request('https://cdn.fusionbrain.ai/static/styles/api')
        with urllib.request.urlopen(req) as response:
            return [x['name'] for x in json.loads(response.read())]

    @staticmethod
    def get_local_styles() -> List[dict]:
        with open('app/assets/kandinsky_styles.json', 'r', encoding='utf-8') as f:
            return json.load(f)

    def generate(
            self, prompt: str, model: str, style: str, negative: str = '',
            images: int = 1, width: int = 1024, height: int = 1024
    ) -> str:
        """
        Generates an image based on a text prompt.

        Args:
            prompt (str): The text prompt for image generation.
            model (str): The model ID to use.
            style (str): The style to use.
            negative (str, optional): Negative prompt. Defaults to ''.
            images (int, optional): Number of images to generate. Defaults to 1.
            width (int, optional): Width of the image. Defaults to 1024.
            height (int, optional): Height of the image. Defaults to 1024.

        Returns:
            str: The request UUID.
        """
        params = {
            "type": "GENERATE",
            "numImages": images,
            "style": style,
            "width": width,
            "height": height,
            "negativePromptUnclip": negative,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        logging.info(f'[CLIENT]: Image Request: {prompt, negative}')

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }

        print(prompt, style, negative)

        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id: str, counter: ft.Text, attempts: int = 10, delay: int = 10) -> ImageData:
        """
        Checks the status of an image generation request.

        Args:
            request_id (str): The UUID of the request.
            counter (ft.Page): Flet page for control view
            attempts (int, optional): Number of attempts to check status. Defaults to 10.
            delay (int, optional): Delay between attempts in seconds. Defaults to 10.

        Returns:
            Optional[List[str]]: List of image URLs if generation is done, None if not found.
        """
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            print(data)
            if data['censored']:
                return ImageData(
                    status='CENSORED',
                    image=data['images']
                )
            if data['status'] == 'DONE':
                return ImageData(
                    status='DONE',
                    image=data['images'],
                )
            if data['status'] == 404:
                return ImageData(
                    status='ERROR',
                    image=None,
                )
            if data['status'] == 'INITIAL':
                counter.value = f"Try: {attempts} / 10"
                counter.update()

            attempts -= 1
            time.sleep(delay)
