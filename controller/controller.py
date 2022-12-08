import json
import os
import platform
from datetime import datetime as dt
from datetime import timedelta as td

import kivy
from kivy.app import App
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRoundFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image


def load_storyboard(flat):
    """Load JSON file that holds all media information"""

    # get absolute path depending on OS
    directories = {
        "Windows": r"C:\pythonCode\rollerAds\static",
        "Linux": r"/home/pi/pythonCode/rollerAds\static",
    }

    # open storyboard JSON data and split into active and not active
    with open(
        os.path.join(directories[platform.system()], "json", "storyboard.json"),
        mode="r",
    ) as json_file:
        storyboard = json.load(json_file)["loaded_media"]
    active = [i for i in storyboard if i["active"]]
    inactive = [i for i in storyboard if not i["active"]]

    # create list of images for use with thumbnails
    active_thumbnails = [i["thumbnail"] for i in active]
    inactive_thumbnails = [i["thumbnail"] for i in inactive]

    # flatten information into plain list
    active = flatten(active, 14)
    inactive = flatten(inactive, 14)

    return active, inactive, active_thumbnails, inactive_thumbnails


def flatten(data, size):
    # ("alert", color1, r["playback"]["file_name"]),
    sz = f"[size={str(size)}]"
    return [
        (
            f'{sz}{str(i["position"])}',
            f'{sz}{i["playback"]["aka"]}',
            f'{sz}{i["playback"]["file_name"]}',
            f'{sz}{i["playback"]["type"]}',
            f'{sz}{i["playback"]["format"]}',
            f'{sz}{str(i["playback"]["audio"])}',
            f'{sz}{str(i["playback"]["duration"])} s',
            f'{sz}{i["playback"]["datetime_start_str"]}',
            f'{sz}{i["playback"]["datetime_end_str"]}',
        )
        for i in data
    ]


class Table(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # set orientation of main boxlayout
        self.orientation = "vertical"

        # load active and inactive data into flat table format
        (
            active,
            inactive,
            self.active_thumbnails,
            self.inactive_thumbnails,
        ) = load_storyboard(flat=True)
        sh_top = len(active) / (len(active) + len(inactive))
        sh_bottom = 1 - sh_top

        # split main box layout into two parts (Widget A, Widget B)
        top_block = BoxLayout(
            orientation="vertical",
            spacing=15,
            padding=(10, 0, 10, 10),
            size_hint=(1, sh_top),
        )
        bottom_block = BoxLayout(
            orientation="vertical",
            spacing=15,
            padding=(10, 20, 10, 10),
            size_hint=(1, sh_bottom),
        )

        # populate upper box with title, table and button section
        new_title = MDLabel(
            markup=True,
            text="[b]Loaded[/b]",
            size_hint=(1, 0.1),
            halign="center",
        )
        new_title.font_size = 30
        new_midsection = BoxLayout(
            orientation="horizontal",
            spacing=5,
            padding=(5, 5, 5, 5),
            size_hint=(1, 0.8),
        )
        new_widget = BoxLayout(
            orientation="horizontal",
            spacing=5,
            padding=(5, 5, 5, 5),
            size_hint=(1, 0.1),
        )

        # insert table and preview zone in midsection
        self.image_preview = Image(
            source=os.path.join(
                MEDIA_LOCATION, "thumbnails", self.active_thumbnails[0]
            ),
        )
        self.image_preview.size_hint = (0.25, 1)

        new_midsection.add_widget(self.generate_table(active))
        new_midsection.add_widget(self.image_preview)

        # insert buttons into button section
        new_widget.add_widget(MDRoundFlatButton(text="UnLoad"))
        new_widget.add_widget(MDRoundFlatButton(text="Move Up"))
        new_widget.add_widget(MDRoundFlatButton(text="Move Down"))

        # combine all three pieces of Widget A
        top_block.add_widget(new_title)
        top_block.add_widget(new_midsection)
        top_block.add_widget(new_widget)

        # populate upper box with title, table and button section
        new_title = MDLabel(
            markup=True,
            text="[b]UnLoaded[/b]",
            size_hint=(1, 0.1),
            halign="center",
        )
        new_title.font_size = 30
        new_widget = BoxLayout(
            orientation="horizontal",
            spacing=5,
            padding=(5, 5, 5, 5),
            size_hint=(1, 0.1),
        )

        # insert buttons into button section
        new_widget.add_widget(MDRoundFlatButton(text="Load", on_press=self.click))
        new_widget.add_widget(MDRoundFlatButton(text="Discard"))

        # combine all three pieces of Widget B
        bottom_block.add_widget(new_title)
        bottom_block.add_widget(self.generate_table(inactive))
        bottom_block.add_widget(new_widget)

        # combine Widget A and Widget B
        self.add_widget(top_block)
        self.add_widget(bottom_block)

    def generate_table(self, table_data):
        new_table = MDDataTable(
            column_data=[
                ("#", dp(15)),
                ("Name", dp(30)),
                ("Filename", dp(35)),
                ("Type", dp(10)),
                ("Format", dp(15)),
                ("Audio", dp(10)),
                ("Duration", dp(20)),
                ("Start Date", dp(30)),
                ("End Date", dp(30)),
            ],
            background_color_header="#b0bec5",
            background_color_selected_cell="#e6b400",
            elevation=2,
        )
        new_table.row_data = table_data
        new_table.bind(on_row_press=self.row_selected)
        new_table.size_hint = (0.75, 1)
        return new_table

    def click(self, k):
        print("dfdfdf")
        print(k)
        self.image_preview.source = os.path.join(
            MEDIA_LOCATION, "thumbnails", self.active_thumbnails[1]
        )

    def row_selected(self, table, row):
        self.image_preview.source = os.path.join(
            MEDIA_LOCATION, "thumbnails", self.active_thumbnails[row.index // 9]
        )


class KivyApp(MDApp):
    def build(self):
        #     self.theme_cls.them_style = "Light"
        #     self.theme_cls.primary_palette = "BlueGray"
        return Table()


def main():
    global MEDIA_LOCATION
    MEDIA_LOCATION = r"C:\pythonCode\rollerAds\media"
    kivy.require("2.1.0")
    Window.size = (1500, 900)
    Window.top = 50
    Window.left = 50
    Window.clearcolor = (1, 0, 0, 1)
    KivyApp().run()


main()
