import logging

import flet as ft

from app.pages.DevPage import DevPage
from app.pages.GalleryPage import GalleryPage
from app.pages.GenerateImage import ImagePage
from app.pages.HistoryPage import HistoryPage
from app.pages.HomePage import HomePage
from app.pages.LogsPage import LogsPage
from app.pages.SettingsPage import SettingsPage
from dotenv import load_dotenv

load_dotenv()
# logging.basicConfig(filename="flet.log", level=logging.DEBUG)


class MyApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Flet App"
        self.page.window.width = 500
        self.page.window.height = 900
        self.count = 0
        self.is_enable_dev = None
        self.page.theme_mode = self.set_theme()
        self.page.theme = ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.PRIMARY))
        self.page.on_route_change = self.route_change
        self.theme_switcher = ft.PopupMenuItem(
            icon=ft.icons.SUNNY if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.DARK_MODE,
            text="Light theme" if self.page.theme_mode == ft.ThemeMode.LIGHT else "Dark theme",
            on_click=self.theme_changed
        )
        self.dev_menu_btn = ft.PopupMenuItem(
                                icon=ft.icons.DEVELOPER_MODE,
                                text="Dev",
                                on_click=lambda _: page.go("/dev")
                            )
        self.logs_menu_btn = ft.PopupMenuItem(
                            icon=ft.icons.FILE_UPLOAD,
                            text="Logs",
                            on_click=lambda _: page.go("/logs")
                        )
        self.popup_menu = ft.PopupMenuButton(
                        items=[
                            self.theme_switcher,
                            ft.PopupMenuItem(
                                icon=ft.icons.SETTINGS,
                                text="Settings",
                                on_click=lambda _: page.go("/settings")
                            ),
                        ],

                    )
        self.appbar = ft.AppBar(
            actions=[
                ft.Container(
                    content=self.popup_menu,
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
        self.page.go("/home")

    def activate_dev_mode(self):
        self.popup_menu.items.append(self.dev_menu_btn)
        self.popup_menu.items.append(self.is_enable_dev)
        self.is_enable_dev = 1
        self.page.update()

    def route_change(self, route):
        self.page.views.clear()
        if route.route == "/home":

            self.page.views.append(ft.View(route="/home", controls=[
                self.appbar,
                HomePage(self.page).get_view(),
                self.navigation_bar
            ]))
            print(self.count)
            self.page.appbar.title = ft.Text("Chat GPT")

        elif route.route == "/history":
            self.count = 0
            self.page.views.append(ft.View(route="/history", controls=[
                self.appbar,
                HistoryPage(self.page),
                self.navigation_bar
            ], scroll=ft.ScrollMode.HIDDEN))
            self.page.appbar.title = ft.Text("Chats history")

        elif route.route == "/image_gen":
            self.count = 0
            self.page.views.append(ft.View(route="/image_gen", controls=[
                self.appbar,
                ImagePage(self.page).get_view(),
                self.navigation_bar
            ]))
            self.page.appbar.title = ft.Text("Generate Image")

        elif route.route == "/gallery":
            self.count = 0
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

        elif route.route == "/dev":
            if self.is_enable_dev is not None:
                self.page.views.append(ft.View(route="/dev", controls=[
                    self.appbar,
                    DevPage(self.page).get_view(),
                    self.navigation_bar
                ], scroll=ft.ScrollMode.HIDDEN))
                self.page.appbar.title = ft.Text("Dev")

        elif route.route == "/logs":
            if self.is_enable_dev is not None:
                self.page.views.append(ft.View(route="/logs", controls=[
                    self.appbar,
                    LogsPage(self.page).get_view(),
                    self.navigation_bar
                ], scroll=ft.ScrollMode.HIDDEN))
                self.page.appbar.title = ft.Text("Logs")

        self.page.update()

    def nav_change(self, event):
        self.count += 1
        if self.count >= 10:
            print("MODE TRUE")
            self.activate_dev_mode()
            self.count = 0
        routes = ["/home", "/history", "/image_gen", "/gallery", "/settings", "/dev", "/logs"]
        self.page.go(routes[int(event.data)])

    def set_theme(self):
        if bool(self.page.client_storage.get('THEME')):
            if self.page.client_storage.get('THEME') == "ThemeMode.DARK":
                return ft.ThemeMode.DARK
        return ft.ThemeMode.LIGHT

    def theme_changed(self, e):
        self.page.theme_mode = (
            ft.ThemeMode.DARK
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.theme_switcher.text = "Light theme"
            self.theme_switcher.icon = ft.icons.LIGHT_MODE
        else:
            self.theme_switcher.text = "Dark theme"
            self.theme_switcher.icon = ft.icons.DARK_MODE

        self.page.client_storage.set('THEME', str(self.page.theme_mode))
        self.page.update()


def main(page: ft.Page):
    MyApp(page)


ft.app(target=main, assets_dir='app/assets')
# ft.app(target=main, assets_dir="app/assets", view=ft.WEB_BROWSER, host='127.0.0.1', port=8009)
# ft.app(target=main, assets_dir="app/assets", view=ft.WEB_BROWSER, host='0.0.0.0', port=8009)
