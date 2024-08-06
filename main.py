import flet as ft
from app.navigation import Navigation


class MyApp:
    def __init__(self, page: ft.Page):
        self.page = page
        # self.page.adaptive = True
        self.page.title = "SNTRK GPT"
        self.page.theme_mode = self.set_theme()
        self.page.theme = ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.PRIMARY))
        # self.page.window.resizable = False
        self.page.window.width = 500
        self.page.window.height = 900
        page.vertical_alignment = ft.VerticalAlignment.END
        page.navigation_bar = Navigation(self.page)

        page.appbar = ft.CupertinoAppBar(
            leading=ft.Icon(ft.icons.GPP_MAYBE),
            bgcolor=ft.cupertino_colors.ON_PRIMARY,
            middle=ft.Text("Chat GPT by SNTRK"),
        )

    def set_theme(self):
        if bool(self.page.client_storage.get('THEME')):
            if self.page.client_storage.get('THEME') == "ThemeMode.DARK":
                return ft.ThemeMode.DARK
        return ft.ThemeMode.LIGHT


def main(page: ft.Page):
    MyApp(page)


ft.app(target=main, assets_dir="assets")
# ft.app(target=main, assets_dir="assets", view=ft.WEB_BROWSER, host='0.0.0.0', port=8009)
