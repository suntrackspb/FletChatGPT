import flet as ft


class LogsPage(ft.Column):
    def __init__(self, page, on_route_change):
        super().__init__()
        self.page = page
        self.page.title = "Logs"
        self.on_route_change = on_route_change
        self.chats = ft.Column(
            expand=True,
            height=self.page.window.height - 200,
            scroll=ft.ScrollMode.ALWAYS,
        )
        self.on_load()

    def on_load(self):
        with open("out.log", "r") as f:
            log = f.readlines()

        for line in log:
            self.chats.controls.append(ft.Text(line))

    def get_view(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=self.chats,
                        height=self.page.window.height - 250
                    )
                ]
            )
        )
