import flet as ft
import requests

from app.utils.s3_api import S3Api
from app.components.ErrorDialog import ErrorDialog


class GalleryPage(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.page.title = "Gallery"

        self.s3 = None

        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        page.overlay.append(self.pick_files_dialog)

        self.current_image = ''

        self.dlg = ft.AlertDialog()

        self.images = ft.GridView(
            # height=self.page.window.height,
            # width=self.page.window.width,
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
        self.s3 = S3Api(self.page)
        is_connect = self.s3.bucket_list()
        if is_connect['success'] is False:
            ErrorDialog(self.page, title="S3 Connection Error", message=is_connect['message']).show_dialog()
            return
        images_list = self.s3.list()
        images_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
        for image in images_list:
            url = f'{self.s3.s3_endpoint_url}/{self.s3.s3_bucket_name}/{image["Key"]}'
            if any(image["Key"].lower().endswith(ext) for ext in images_extensions):
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
            ],
            expand=True
        )

        self.dlg.content.controls.append(
            ft.IconButton(
                icon=ft.icons.OPEN_IN_NEW,
                bottom=10,
                right=10,
                icon_color=ft.colors.ON_PRIMARY,
                hover_color=ft.colors.SECONDARY,
                bgcolor=ft.colors.ON_PRIMARY_CONTAINER,
                opacity=0.7,
                on_click=lambda _: self.open_url(e.control.content.src)

            )
        )

        self.page.overlay.append(self.dlg)
        # self.page.dialog = self.dlg
        self.dlg.open = True
        self.page.update()

    def open_url(self, url: str):
        if self.page.platform in [ft.PagePlatform.IOS, ft.PagePlatform.ANDROID]:
            self.page.launch_url(
                url=url,
                web_window_name=ft.UrlTarget.SELF.value,
                web_popup_window=True
            )
        else:
            self.page.launch_url(
                url=url,
                web_window_name=ft.UrlTarget.BLANK.value,
                web_popup_window=True
            )

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
