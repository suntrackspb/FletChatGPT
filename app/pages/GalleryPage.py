import json

import flet as ft
import requests

from app.s3_api import S3Api


class GalleryPage(ft.Column):
    def __init__(self, page, on_route_change):
        super().__init__()
        self.page = page
        self.page.title = "Gallery"
        self.s3 = S3Api(
            region=self.page.client_storage.get('S3_REGION'),
            access_key=self.page.client_storage.get('S3_ACCESS'),
            secret_key=self.page.client_storage.get('S3_SECRET'),
            endpoint=self.page.client_storage.get('S3_ENDPOINT'),
            bucket=self.page.client_storage.get('S3_BUCKET'),
        )

        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        page.overlay.append(self.pick_files_dialog)

        self.current_image = ''

        self.dlg = ft.AlertDialog(
            on_dismiss=lambda e: print("Dialog dismissed!"),
        )
        self.images = ft.GridView(
            height=self.page.window.height,
            width=self.page.window.width,
            runs_count=5,
            max_extent=150,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
        )
        self.on_load()

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        if e.path:
            image = requests.get(self.current_image)
            try:
                with open(e.path, 'wb') as f:
                    f.write(image.content)
            except Exception as e:
                print(e)

    def on_load(self):
        images_list = self.s3.list()
        for image in images_list:
            url = f'http://192.168.88.20:9000/{self.page.client_storage.get("S3_BUCKET")}/{image["Key"]}'
            self.images.controls.append(
                ft.Container(
                    content=ft.Image(
                        src=url,
                        fit=ft.ImageFit.FILL,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        border_radius=ft.border_radius.all(10),
                    ),
                    data=url,
                    on_click=self.onclick_container
                )
            )
        self.page.update()

    def onclick_container(self, e: ft.ControlEvent):
        self.current_image = e.control.data
        image_name = e.control.data.split("/")[-1]
        self.dlg.content = ft.Stack(
            controls=[
                ft.Image(
                    src=e.control.content.src,
                    fit=ft.ImageFit.FILL,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    border_radius=ft.border_radius.all(10),
                ),
                ft.IconButton(
                    icon=ft.icons.DOWNLOAD,
                    top=10,
                    right=10,
                    bgcolor=ft.colors.GREY_300,
                    opacity=0.5,
                    on_click=lambda _: self.pick_files_dialog.save_file(
                                file_name=image_name,
                                file_type=ft.FilePickerFileType.IMAGE
                            ),

                )
            ]
        )
        e.control.page.dialog = self.dlg
        self.dlg.open = True
        self.page.update()

    def get_view(self):
        return ft.Container(
            content=ft.Column(
                [
                    self.images,
                ],
                scroll=ft.ScrollMode.ALWAYS,
                expand=True,
            ),
        )
