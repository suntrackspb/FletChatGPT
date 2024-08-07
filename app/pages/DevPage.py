import subprocess
import platform
import flet as ft


class DevPage(ft.View):
    def __init__(self, page, on_route_change):
        super().__init__()
        self.page = page
        self.page.title = "History"
        self.on_route_change = on_route_change
        self.file_picker = ft.FilePicker(on_result=self.file_picker_result)
        self.page.overlay.append(self.file_picker)
        self.files = ft.Column()
        self.chats = ft.Column(
            expand=True,
            height=self.page.window.height - 200,
            scroll=ft.ScrollMode.ALWAYS,
        )
        self.command = ft.TextField(
            label="Command",
            border_color=ft.colors.PRIMARY,
            expand=True
        )
        self.command_btn = ft.ElevatedButton(
            text="Run",
            on_click=self.on_click_run
        )
        self.storage_values = ft.Column()
        self.get_storage = ft.ElevatedButton(
            text="Get Values",
            on_click=self.on_click_get_storage
        )
        self.on_load()

    def on_load(self):
        pass

    def file_picker_result(self, e):
        self.files.controls.clear()
        if e.files is not None:
            for f in e.files:
                size = round(f.size / (1024 ** 2), 2)
                self.files.controls.append(ft.Row([ft.Text(f.path), ft.Text(f'{size} Mb')]))
        self.page.update()

    def on_click_get_storage(self, e):
        keys = self.page.client_storage.get_keys("")
        for key in keys:
            self.storage_values.controls.append(ft.Row([ft.Text(f"Key: {key}, Value: {self.page.client_storage.get(key)}")]))

        self.page.update()


    def on_click_run(self, e):
        current_os = platform.system()
        if current_os == 'Windows':
            encoding = 'cp866'
        else:
            encoding = 'utf-8'
        self.chats.controls.clear()
        comm = self.command.value.split(" ")
        self.command.value = ''
        result = subprocess.run(comm, capture_output=True, text=True, shell=True, encoding=encoding)
        for line in result.stdout.split("\n"):
            self.chats.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(line)
                    ]
                )
            )
            self.page.update()

    def get_view(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Column(
                        [
                            self.files,
                            ft.ElevatedButton(
                                "Select files...",
                                icon=ft.icons.FOLDER_OPEN,
                                on_click=lambda _: self.file_picker.pick_files(allow_multiple=True),
                            ),
                            self.storage_values,
                            self.get_storage
                        ]
                    ),
                    ft.Row(
                        [
                            self.command,
                            self.command_btn
                        ]
                    ),
                    ft.Container(
                        content=self.chats,
                        height=self.page.window.height - 250
                    )
                ]
            )
        )
