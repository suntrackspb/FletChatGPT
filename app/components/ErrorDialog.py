import flet as ft


class ErrorDialog(ft.CupertinoAlertDialog):
    def __init__(self, page: ft.Page, title: str, message: str):
        self.title = title
        self.message = message
        super().__init__(
            title=ft.Text(self.title),
            content=ft.Text(self.message),
            actions=[
                ft.CupertinoDialogAction(
                    "OK", is_destructive_action=True, on_click=self.dismiss_dialog
                )
            ],
            open=True
        )
        self.page = page

    def show_dialog(self):
        self.page.overlay.append(self)
        self.page.update()

    def dismiss_dialog(self, e):
        self.open = False
        e.control.page.update()
        self.page.overlay.clear()
