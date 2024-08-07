from datetime import datetime

import flet as ft

from app.chat_api import OpenAI
import uuid


messages = []
chat_id = uuid.uuid4()


class HomePage(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.page.title = "Chat"
        self.search = ft.TextField(
            label="Message",
            border_color=ft.colors.PRIMARY,
            expand=True,
            on_submit=self.on_click_search
        )
        self.search_btn = ft.IconButton(icon=ft.icons.SEND, icon_color=ft.colors.PRIMARY, on_click=self.on_click_search)
        self.clear_btn = ft.IconButton(icon=ft.icons.CLEAR, icon_color=ft.colors.PRIMARY, on_click=self.on_click_clear)
        self.msg_view = ft.Column(
            # height=int(self.page.window.height - 240),
            spacing=10,
        )

        page.fonts = {
            "Roboto Mono": "RobotoMono-VariableFont_wght.ttf",
        }

        self.on_load()

    def format_message(self, message):
        row = ft.MainAxisAlignment.END
        bg = ft.colors.SECONDARY_CONTAINER
        if message['role'] == 'assistant':
            row = ft.MainAxisAlignment.START
            bg = ft.colors.TERTIARY_CONTAINER

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Markdown(
                        message['content'],
                        selectable=True,
                        code_theme="atom-one-dark",
                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                        code_style=ft.TextStyle(font_family="Roboto Mono"),
                        width=(self.page.window.width / 3) * 2,
                    )
                ],
                alignment=row,
            ),
            bgcolor=bg,
            border_radius=10,
            padding=ft.padding.only(left=10, right=20, top=10, bottom=10)
        )

    def on_load(self):
        if bool(self.page.data):
            messages = self.page.client_storage.get(self.page.data)
            for message in messages:
                self.msg_view.controls.append(self.format_message(message))

    def on_click_clear(self, e):
        # for chat in self.page.client_storage.get_keys('msg'):
        #     self.page.client_storage.remove(chat)
        messages = []
        self.page.data = None
        self.msg_view.controls.clear()
        self.page.update()

    def on_click_search(self, e):
        url = self.page.client_storage.get('API_URL')
        key = self.page.client_storage.get('API_KEY')

        self.msg_view.controls.append(self.format_message({"role": "user", "content": self.search.value}))
        self.page.update()

        messages.append(
            {"role": "user", "content": self.search.value, "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S")})

        api = OpenAI(url=url, key=key, messages=messages)
        choices = api.generate_completion()
        # print(choices)
        messages.append(choices['choices'][0]['message'])

        self.msg_view.controls.append(self.format_message(choices['choices'][0]['message']))
        self.search.value = ''
        self.page.update()
        self.search.focus()
        self.page.client_storage.set(f'msg-{chat_id}', messages)

    def get_view(self):
        return ft.Column(
            [
                ft.Column(
                    [
                        ft.Container(
                            self.msg_view,
                        ),
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.HIDDEN,
                ),
                ft.Container(
                    ft.Row(
                        [
                            self.search,
                            self.search_btn,
                            self.clear_btn,
                        ],
                    ),
                ),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.END
        )