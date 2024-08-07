import flet as ft
from app.main import MyApp


def main(page: ft.Page):
    MyApp(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir='app/assets')
    # ft.app(target=main, assets_dir="app/assets", view=ft.WEB_BROWSER, host='127.0.0.1', port=8009)
    # ft.app(target=main, assets_dir="app/assets", view=ft.WEB_BROWSER, host='0.0.0.0', port=8009)
