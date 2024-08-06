import flet as ft
from app.pages.HistoryPage import HistoryPage
from app.pages.ImagePage import ImagePage
from app.pages.GalleryPage import GalleryPage
from app.pages.SettingsPage import SettingsPage
from app.pages.HomePage import HomePage
from app.pages.DevPage import DevPage
from app.pages.LogsPage import LogsPage


def get_destinations(mode: int):
    destinations = [
        ft.NavigationDestination(icon=ft.icons.CHAT, label="Chat"),
        ft.NavigationDestination(icon=ft.icons.HISTORY, label="History"),
        ft.NavigationDestination(icon=ft.icons.PREVIEW, label="Image"),
        ft.NavigationDestination(icon=ft.icons.IMAGE_SEARCH, label="Gallery"),
        ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Settings"),
    ]
    if mode:
        destinations.append(
            ft.NavigationDestination(icon=ft.icons.DEVELOPER_MODE, label="DEV")
        )
        destinations.append(
            ft.NavigationDestination(icon=ft.icons.FILE_UPLOAD, label="logs")
        )
    return destinations


class Navigation(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.count = 0
        self.mode = self.page.client_storage.get('DEV_MODE')
        self.destinations = get_destinations(self.mode)

        self.cupertino_navigation_bar = ft.NavigationBar(
            bgcolor=ft.cupertino_colors.ON_PRIMARY,
            on_change=lambda e: self.on_route_change(e),
            elevation=10,
            destinations=self.destinations,
        )
        self.routes = {
            '0': HomePage,
            '1': HistoryPage,
            '2': ImagePage,
            '3': GalleryPage,
            '4': SettingsPage,
            '5': DevPage,
            '6': LogsPage,
        }

        self.page.on_route_change = self.on_route_change
        self.page.go('0')

    def on_route_change(self, e):
        route = e.data
        if route == '4':  # Settings page
            self.count += 1
            if self.count >= 10 and self.mode == 0:
                self.mode = 1
                self.page.client_storage.set('DEV_MODE', 1)
                self.destinations = get_destinations(self.mode)
                self.cupertino_navigation_bar.destinations = self.destinations
                self.count = 0  # Reset count after enabling DEV Mode

        self.page.controls.clear()
        self.page.controls.append(self.cupertino_navigation_bar)
        self.page.controls.append(self.routes[route](self.page, self.on_route_change).get_view())
        self.page.appbar.middle = ft.Text(self.page.title)
        self.page.update()

    def __call__(self):
        return self.cupertino_navigation_bar
