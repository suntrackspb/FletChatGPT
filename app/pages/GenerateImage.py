import base64
import uuid

import flet as ft

from app.utils.image_api import Text2ImageAPI
from app.utils.s3_api import S3Api


class ImagePage(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.page.title = "Image"
        self.img_url = None
        self.img_data = None
        self.api = Text2ImageAPI(page=self.page)
        self.s3 = S3Api(page=self.page)

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
        self.img_url = f'{self.s3.s3_endpoint_url}/{self.s3.s3_bucket_name}/{img_uid}.png'

        self.container.controls.clear()
        self.container.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.ElevatedButton(text="Save", icon=ft.icons.SAVE, expand=True,
                                                  color=ft.colors.ON_PRIMARY, bgcolor=ft.colors.PRIMARY,
                                                  on_click=lambda _: self.pick_files_dialog.save_file(
                                                      file_name=f"{img_uid}.png",
                                                      file_type=ft.FilePickerFileType.IMAGE
                                                  ), ),
                                ft.ElevatedButton(text="Reset", icon=ft.icons.CANCEL, expand=True,
                                                  color=ft.colors.ON_PRIMARY, bgcolor=ft.colors.PRIMARY,
                                                  on_click=lambda _: self.delete_image(filename=f"{img_uid}.png")),
                            ]

                        ),
                        ft.Image(
                            src=self.img_url,
                            fit=ft.ImageFit.CONTAIN,
                            border_radius=10
                        ),
                    ],
                ),
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
