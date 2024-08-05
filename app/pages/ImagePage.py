import base64
import uuid

import flet as ft

from app.image_api import Text2ImageAPI
from app.s3_api import S3Api


class ImagePage(ft.Column):
    def __init__(self, page, on_route_change):
        super().__init__()
        self.page = page
        self.page.title = "Image"
        self.img_url = None
        self.img_data = None

        self.url = "https://api-key.fusionbrain.ai/"
        self.key = self.page.client_storage.get('IMG_KEY')
        self.secret = self.page.client_storage.get('IMG_SECRET')
        self.api = Text2ImageAPI(url=self.url, api_key=self.key, secret_key=self.secret)

        self.s3 = S3Api()

        self.img_prompt = ft.TextField(label="Prompt", border_color=ft.colors.PRIMARY, expand=True,
                                       on_submit=self.run_generate)
        self.img_negative = ft.TextField(label="Negative Prompt", border_color=ft.colors.PRIMARY, expand=True,
                                         on_submit=self.run_generate)
        self.img_model = ft.Dropdown(
            label="Select style",
            border_color=ft.colors.PRIMARY,
            expand=True,
            options=[],
        )
        self.generate_btn = ft.ElevatedButton(
            text="Generate",
            icon=ft.icons.GENERATING_TOKENS,
            color=ft.colors.ON_PRIMARY,
            bgcolor=ft.colors.PRIMARY,
            on_click=self.run_generate,
        )
        self.container = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.ALWAYS,
        )
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)

        page.overlay.append(self.pick_files_dialog)

        self.on_load()

    def on_load(self):
        models = self.api.get_styles()
        self.img_model.value = models[0]
        for model in models:
            self.img_model.options.append(ft.dropdown.Option(model))

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        if e.path:
            try:
                with open(e.path, 'wb') as f:
                    f.write(self.img_data)
            except Exception as e:
                print(e)
            self.page.update()

    def run_generate(self, e):
        if self.img_prompt.value == '':
            return

        req_id = self.api.generate(
            prompt=self.img_prompt.value,
            model=self.api.get_model(),
            negative=self.img_negative.value,
        )

        self.img_prompt.value = ''
        self.img_negative.value = ''

        self.container.controls.append(
            ft.Row(
                [
                    ft.ProgressRing(width=32, height=32, stroke_width=4)
                ],
                height=self.page.window.height / 2,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER
            )

        )
        self.page.update()

        base64_image_data = self.api.check_generation(req_id)
        self.img_data = base64.b64decode(base64_image_data[0])

        img_uid = uuid.uuid4()

        self.s3.put(key=f'{img_uid}.png', body=self.img_data)
        self.img_url = f'http://192.168.88.20:9000/sun-public/{img_uid}.png'

        self.container.controls.clear()
        self.container.controls.append(
            ft.Container(
                content=ft.CupertinoContextMenu(
                    enable_haptic_feedback=True,
                    content=ft.Column(
                        [
                            ft.Row(
                                height=30
                            ),
                            ft.Image(
                                src=self.img_url,
                                # src=f'http://192.168.88.20:9000/sun-public/last_image.png',
                                fit=ft.ImageFit.CONTAIN,
                                border_radius=10
                            ),
                        ],
                    ),
                    actions=[
                        ft.CupertinoContextMenuAction(
                            text="Save image",
                            is_default_action=True,
                            trailing_icon=ft.icons.CHECK,
                            on_click=lambda _: self.pick_files_dialog.save_file(
                                file_name=f"{img_uid}.png",
                                file_type=ft.FilePickerFileType.IMAGE
                            ),
                        ),
                        ft.CupertinoContextMenuAction(
                            text="Action 2",
                            trailing_icon=ft.icons.MORE,
                            on_click=lambda e: print("Action 2"),
                        ),
                        ft.CupertinoContextMenuAction(
                            text="Delete image",
                            is_destructive_action=True,
                            trailing_icon=ft.icons.CANCEL,
                            on_click=lambda _: self.delete_image(filename=f"{img_uid}.png")

                        ),
                    ],
                ),
                padding=ft.padding.all(10)
            )

        )
        self.page.update()

    def delete_image(self, filename):
        self.s3.delete(key=filename)
        self.container.controls.clear()
        self.page.update()

    def get_view(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            self.img_prompt,
                        ],
                    ),
                    ft.Row(
                        [
                            self.img_negative,
                        ],
                    ),
                    ft.Row(
                        [
                            self.img_model,
                            self.generate_btn,
                        ],
                    ),
                    ft.Container(
                        content=self.container,
                    )

                ],
                scroll=ft.ScrollMode.ALWAYS,
                expand=True,
            ),
        )
