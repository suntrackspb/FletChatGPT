import flet as ft
from flet_core import ControlEvent


class HistoryPage(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.title = "History"
        self.chats = ft.Column()
        self.content = self.chats
        self.on_load()


    def on_load(self):
        self.chats.controls.clear()
        chats = self.page.client_storage.get_keys('msg')
        for chat in chats:
            data = self.page.client_storage.get(chat)
            self.chats.controls.append(
                ft.CupertinoListTile(
                    additional_info=ft.Text(data[0]['date']),
                    bgcolor_activated=ft.colors.AMBER_ACCENT,
                    title=ft.Text(data[0]['content']),
                    subtitle=ft.Text(data[1]['content']),
                    bgcolor=ft.colors.PRIMARY_CONTAINER,
                    # on_click=lambda e: self.tile_clicked(e),
                    on_click=lambda e: self.show_cupertino_action_sheet(e),
                    data=chat
                )
            )

    def show_cupertino_action_sheet(self, e):
        e.control.page.show_bottom_sheet(
            ft.CupertinoBottomSheet(
                ft.CupertinoActionSheet(
                    title=e.control.title,
                    message=ft.Text(e.control.data),
                    cancel=ft.CupertinoActionSheetAction(
                        content=ft.Text("Cancel"),
                        on_click=self.close_cupertino_action_sheet,
                    ),
                    actions=[
                        ft.CupertinoActionSheetAction(
                            content=ft.Text("Open Chat"),
                            is_default_action=True,
                            data=e.control.data,
                            on_click=lambda e: self.open_chat(e),
                        ),
                        # ft.CupertinoActionSheetAction(
                        #     content=ft.Text("Normal Action"),
                        #     on_click=lambda e: print("Normal Action clicked"),
                        # ),
                        ft.CupertinoActionSheetAction(
                            content=ft.Text("Delete Chat"),
                            is_destructive_action=True,
                            data=e.control.data,
                            on_click=lambda e: self.remove_chat(e),
                        ),
                    ],
                )
            )
        )

    def open_chat(self, e):
        e.data = '0'
        self.page.data = e.control.data
        self.page.navigation_bar.selected_index = 0
        self.on_route_change(e)
        self.update()
        self.close_cupertino_action_sheet(e)

    def remove_chat(self, e):
        self.page.client_storage.remove(e.control.data)
        e.control.page.close_bottom_sheet()
        self.on_load()
        self.page.update()

    @staticmethod
    def close_cupertino_action_sheet(e):
        e.control.page.close_bottom_sheet()

    # def tile_clicked(self, e: ControlEvent):
    #     e.data = '0'
    #     self.page.data = e.control.data
    #     self.page.navigation_bar.selected_index = 0
    #     self.on_route_change(e)
    #     self.update()

