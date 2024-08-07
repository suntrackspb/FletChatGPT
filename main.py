import flet as ft
from app.pages.HistoryPage import HistoryPage
from app.pages.ImagePage import ImagePage
from app.pages.GalleryPage import GalleryPage
from app.pages.SettingsPage import SettingsPage
from app.pages.HomePage import HomePage
from app.pages.DevPage import DevPage
from app.pages.LogsPage import LogsPage
from app.pages.Test import TestPage


class MyApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Flet App"
        self.page.window.width = 500
        self.page.window.height = 900
        self.page.theme_mode = self.set_theme()
        self.page.theme = ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.PRIMARY))
        self.page.on_route_change = self.route_change
        self.appbar = ft.AppBar(
            actions=[
                ft.Container(
                    content=ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(
                                icon=ft.icons.SETTINGS,
                                text="Settings",
                                on_click=lambda _: page.go("/settings")
                            ),
                            ft.PopupMenuItem(
                                icon=ft.icons.DEVELOPER_MODE,
                                text="Dev",
                                on_click=lambda _: page.go("/dev")
                            ),
                            ft.PopupMenuItem(
                                icon=ft.icons.FILE_UPLOAD,
                                text="Logs",
                                on_click=lambda _: page.go("/logs")
                            ),
                        ],

                    ),
                    padding=ft.padding.only(right=20)
                )
            ],
            title_spacing=20,
            bgcolor=ft.colors.SECONDARY_CONTAINER
        )

        self.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.CHAT, label="Chat"),
                ft.NavigationBarDestination(icon=ft.icons.HISTORY, label="History"),
                ft.NavigationBarDestination(icon=ft.icons.PREVIEW, label="Image"),
                ft.NavigationBarDestination(icon=ft.icons.IMAGE_SEARCH, label="Gallery"),
                # ft.NavigationBarDestination(icon=ft.icons.SETTINGS, label="Settings"),
            ],
            on_change=lambda e: self.nav_change(e),
            bgcolor=ft.colors.SECONDARY_CONTAINER
        )
        self.page.appbar = self.appbar
        self.page.navigation_bar = self.navigation_bar
        self.page.on_view_pop = lambda e: print(e)
        self.page.go("/home")

    def route_change(self, route):
        self.page.views.clear()
        if route.route == "/home":
            self.page.views.append(ft.View(route="/home", controls=[
                self.appbar,
                HomePage(self.page).get_view(),
                self.navigation_bar
            ]))
            self.page.appbar.title = ft.Text("Chat GPT")

        elif route.route == "/history":
            self.page.views.append(ft.View(route="/history", controls=[
                self.appbar,
                HistoryPage(self.page),
                self.navigation_bar
            ], scroll=ft.ScrollMode.HIDDEN))
            self.page.appbar.title = ft.Text("Chats history")

        elif route.route == "/image_gen":
            self.page.views.append(ft.View(route="/image_gen", controls=[
                self.appbar,
                ImagePage(self.page),
                self.navigation_bar
            ]))
            self.page.appbar.title = ft.Text("Generate Image")

        elif route.route == "/gallery":
            self.page.views.append(ft.View(route="/gallery", controls=[
                self.appbar,
                GalleryPage(self.page).get_view(),
                self.navigation_bar
            ], scroll=ft.ScrollMode.HIDDEN))
            self.page.appbar.title = ft.Text("Images Gallery")

        elif route.route == "/settings":
            self.page.views.append(ft.View(route="/settings", controls=[
                self.appbar,
                SettingsPage(self.page),
                self.navigation_bar
            ], scroll=ft.ScrollMode.HIDDEN))
            self.page.appbar.title = ft.Text("Settings")

        self.page.update()

    def nav_change(self, event):
        routes = ["/home", "/history", "/image_gen", "/gallery", "/settings"]
        self.page.go(routes[int(event.data)])

    def set_theme(self):
        if bool(self.page.client_storage.get('THEME')):
            if self.page.client_storage.get('THEME') == "ThemeMode.DARK":
                return ft.ThemeMode.DARK
        return ft.ThemeMode.LIGHT


def main(page: ft.Page):
    MyApp(page)


ft.app(target=main)
# ft.app(target=main, assets_dir="assets", view=ft.WEB_BROWSER, host='127.0.0.1', port=8009)
