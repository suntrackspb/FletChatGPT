import flet as ft


class Appbar(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
