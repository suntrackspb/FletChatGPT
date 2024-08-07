import flet as ft
from app.main import MyApp


def main(page: ft.Page):
    MyApp(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir='../assets')
    # ft.app(target=main, assets_dir="assets", view=ft.WEB_BROWSER, host='127.0.0.1', port=8009)
