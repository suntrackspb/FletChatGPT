import json
import logging

import flet as ft
import requests

models_list = ['gpt-4o-2024-05-13', 'gpt-4o-mini-2024-07-18', 'gpt-4-turbo-2024-04-09', 'gemini-1.5-pro-latest',
               'llama-3.1-405b-instruct', 'llama-3.1-70b-instruct', 'gpt-3.5-turbo-1106', 'claude-3.5-sonnet-20240620',
               'claude-3-opus-20240229', 'gemini-pro', 'llama-2-70b-chat']


class SettingsPage(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.page.title = "Settings"
        self.api_key = ft.TextField(label="API KEY", border_color=ft.colors.PRIMARY,
                                    expand=True, password=True)
        self.api_url = ft.TextField(label="API URL", border_color=ft.colors.PRIMARY, expand=True)

        self.img_secret = ft.TextField(label="Fusion Brain Secret", border_color=ft.colors.PRIMARY, expand=True,
                                       password=True)
        self.img_key = ft.TextField(label="Fusion Brain Api Key", border_color=ft.colors.PRIMARY, expand=True,
                                    password=True)

        self.bucket = ft.TextField(label="Bucket name", border_color=ft.colors.PRIMARY, expand=True)
        self.region_name = ft.TextField(label="Region Name", border_color=ft.colors.PRIMARY, expand=True)
        self.aws_access_key_id = ft.TextField(label="Access Key Id", border_color=ft.colors.PRIMARY, expand=True,
                                              password=True)
        self.aws_secret_key = ft.TextField(label="Secret Key", border_color=ft.colors.PRIMARY, expand=True,
                                           password=True)
        self.endpoint_url = ft.TextField(label="Endpoint URL", border_color=ft.colors.PRIMARY, expand=True)
        self.api_model = ft.Dropdown(
            label="Select model",
            border_color=ft.colors.PRIMARY,
            expand=True,
            options=[],
        )
        # self.c = ft.Switch(label="Light theme", on_change=self.theme_changed)
        self.dev_switch = ft.Switch(label="DEV Mode",
                                    disabled=bool(not self.page.client_storage.get('DEV_MODE')),
                                    on_change=self.dev_mode_switch
                                    )
        self.cupertino_alert_dialog = ft.CupertinoAlertDialog(
            title=ft.Text("Complete"),
            content=ft.Text("Settings was been saved to storage!"),
            actions=[
                ft.CupertinoDialogAction(
                    "OK", is_destructive_action=True, on_click=self.dismiss_dialog
                ),
            ],
        )

        self.content = ft.Column(
            controls=
            [
                ft.Column(
                    [
                        ft.Text("GPT Settings", style=ft.TextThemeStyle.TITLE_MEDIUM),
                        ft.Row(
                            [
                                self.api_url,
                            ],
                        ),
                        ft.Row(
                            [
                                self.api_key,
                            ],
                        ),
                        ft.Row(
                            [
                                self.api_model,
                            ],
                        ),
                        ft.Divider(),
                        ft.Text("Kandinsky Settings", style=ft.TextThemeStyle.TITLE_MEDIUM),
                        ft.Row(
                            [
                                self.img_key,
                            ],
                        ),
                        ft.Row(
                            [
                                self.img_secret,
                            ],
                        ),
                        ft.Divider(),
                        ft.Text("S3 Object Storage", style=ft.TextThemeStyle.TITLE_MEDIUM),
                        ft.Row(
                            [
                                self.region_name,
                            ],
                        ),
                        ft.Row(
                            [
                                self.aws_access_key_id,
                            ],
                        ),
                        ft.Row(
                            [
                                self.aws_secret_key,
                            ],
                        ),
                        ft.Row(
                            [
                                self.endpoint_url,
                            ],
                        ),
                        ft.Row(
                            [
                                self.bucket,
                            ],
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(text="Save", icon=ft.icons.SAVE, expand=True,
                                                  color=ft.colors.ON_PRIMARY, bgcolor=ft.colors.PRIMARY,
                                                  on_click=self.on_click_save),
                                ft.ElevatedButton(text="Load", icon=ft.icons.CLOUD, expand=True,
                                                  color=ft.colors.ON_PRIMARY, bgcolor=ft.colors.PRIMARY,
                                                  on_click=self.load_config_from_url),
                                ft.ElevatedButton(text="Reset", icon=ft.icons.CANCEL, expand=True,
                                                  color=ft.colors.ON_PRIMARY, bgcolor=ft.colors.PRIMARY,
                                                  on_click=self.on_click_reset),
                            ],
                        ),
                        ft.Divider(),
                        ft.Row(
                            [
                                # ft.Column(
                                #     [
                                #         self.c,
                                #     ]
                                # ),
                                ft.Column(
                                    [
                                        self.dev_switch
                                    ]
                                ),
                            ],
                        ),
                    ],
                ),
            ],
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
            alignment=ft.MainAxisAlignment.END
        )

        self.on_load()

    def on_load(self):
        for model in models_list:
            self.api_model.options.append(ft.dropdown.Option(model))
        self.api_key.value = self.page.client_storage.get('API_KEY')
        self.api_url.value = self.page.client_storage.get('API_URL')
        self.api_model.value = self.page.client_storage.get('GPT_MODEL')
        self.img_key.value = self.page.client_storage.get('IMG_KEY')
        self.img_secret.value = self.page.client_storage.get('IMG_SECRET')
        self.dev_switch.value = bool(self.page.client_storage.get('DEV_MODE'))

        self.region_name.value = self.page.client_storage.get('S3_REGION')
        self.aws_access_key_id.value = self.page.client_storage.get('S3_ACCESS')
        self.aws_secret_key.value = self.page.client_storage.get('S3_SECRET')
        self.endpoint_url.value = self.page.client_storage.get('S3_ENDPOINT')
        self.bucket.value = self.page.client_storage.get('S3_BUCKET')

    def on_click_save(self, e):
        self.page.client_storage.set('API_KEY', self.api_key.value)
        self.page.client_storage.set('API_URL', self.api_url.value)
        self.page.client_storage.set('GPT_MODEL', self.api_model.value)
        self.page.client_storage.set('IMG_KEY', self.img_key.value)
        self.page.client_storage.set('IMG_SECRET', self.img_secret.value)

        self.page.client_storage.set('S3_REGION', self.region_name.value)
        self.page.client_storage.set('S3_ACCESS', self.aws_access_key_id.value)
        self.page.client_storage.set('S3_SECRET', self.aws_secret_key.value)
        self.page.client_storage.set('S3_ENDPOINT', self.endpoint_url.value)
        self.page.client_storage.set('S3_BUCKET', self.bucket.value)
        e.control.page.dialog = self.cupertino_alert_dialog
        self.cupertino_alert_dialog.open = True
        keys = self.page.client_storage.get_keys("")
        for key in keys:
            logging.info(f'[CLIENT]: Save settings: Key: {key}, Value: {self.page.client_storage.get(key)}')
        self.page.update()

    def on_click_reset(self, e):
        self.api_key.value = ''
        self.api_url.value = ''
        self.api_model.value = ''
        self.img_key.value = ''
        self.img_secret.value = ''
        self.region_name.value = ''
        self.aws_access_key_id.value = ''
        self.aws_secret_key.value = ''
        self.endpoint_url.value = ''
        self.bucket.value = ''
        self.page.client_storage.remove('API_KEY')
        self.page.client_storage.remove('API_URL')
        self.page.client_storage.remove('GPT_MODEL')
        self.page.client_storage.remove('IMG_KEY')
        self.page.client_storage.remove('IMG_SECRET')
        self.page.client_storage.remove('S3_REGION')
        self.page.client_storage.remove('S3_ACCESS')
        self.page.client_storage.remove('S3_SECRET')
        self.page.client_storage.remove('S3_ENDPOINT')
        self.page.client_storage.remove('S3_BUCKET')
        self.page.update()

    def dismiss_dialog(self, e):
        self.cupertino_alert_dialog.open = False
        e.control.page.update()

    def load_config_from_url(self, e):
        response = requests.get('https://sntrk.ru/73g4f387v/gsdisgi.json')
        if response.status_code == 200:
            config = response.json()
            self.api_key.value = config['api_key']
            self.api_url.value = config['api_url']
            self.api_model.value = config['api_model']
            self.img_key.value = config['img_key']
            self.img_secret.value = config['img_secret']

            self.region_name.value = config['region_name']
            self.aws_access_key_id.value = config['aws_access_key_id']
            self.aws_secret_key.value = config['aws_secret_access_key']
            self.endpoint_url.value = config['endpoint_url']
            self.bucket.value = config['bucket']
            self.page.update()
            # print(config)
        else:
            print(f"Failed to load config. Status code: {response.status_code}")

    # def theme_changed(self, e):
    #     self.page.theme_mode = (
    #         ft.ThemeMode.DARK
    #         if self.page.theme_mode == ft.ThemeMode.LIGHT
    #         else ft.ThemeMode.LIGHT
    #     )
    #     self.page.client_storage.set('THEME', str(self.page.theme_mode))
    #     self.c.label = (
    #         "Light theme" if self.page.theme_mode == ft.ThemeMode.LIGHT else "Dark theme"
    #     )
    #     self.page.update()

    def dev_mode_switch(self, e):
        self.page.client_storage.set('DEV_MODE', int(self.dev_switch.value))
        self.dev_switch.label = (
            "DEV ON" if self.dev_switch.value else "DEV OFF"
        )
        self.page.navigation_bar.update()
        self.page.update()
