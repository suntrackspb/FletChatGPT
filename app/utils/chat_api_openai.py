import os
import flet as ft
from openai import OpenAI


class OfficialOpenAI:
    def __init__(self, page: ft.Page, messages: list = None):
        self.page = page

        self.page = page
        self.base_url = self.page.client_storage.get('API_URL')
        self.api_key = self.page.client_storage.get('API_KEY')
        self.model = self.page.client_storage.get('GPT_MODEL')

        self.validate_config()

        self.messages = messages

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def validate_config(self):
        if not bool(self.model):
            self.model = os.getenv('GPT_API_MODEL')
        if not bool(self.base_url) and not bool(self.api_key):
            self.base_url = os.getenv('GPT_API_URL')
            self.api_key = os.getenv('GPT_API_KEY')

    def send_request(self):
        chat_completion = self.client.chat.completions.create(
            messages=self.messages,
            model=self.model,
        )
        return chat_completion
