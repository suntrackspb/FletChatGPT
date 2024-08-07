import flet as ft


class LogsPage(ft.View):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.page.title = "Logs"
        self.chats = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.ALWAYS,
        )
        self.clear_logs_btn = ft.ElevatedButton(
            icon=ft.icons.CANCEL,
            text="Clear Logs",
            expand=True,
            on_click=self.clear_logs
        )
        self.on_load()

    def on_load(self):
        with open("flet.log", "r") as f:
            log = f.readlines()

        for line in log:
            self.chats.controls.append(ft.Text(line))

    def clear_logs(self, e):
        self.chats.controls.clear()
        with open("flet.log", "w") as f:
            f.write('')
        self.page.update()

    def get_view(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        [
                            self.clear_logs_btn
                        ]
                    ),
                    ft.Container(
                        content=self.chats,
                    )
                ]
            )
        )
