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
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


def load_storyboard(flat):
    """Load JSON file that holds all media information"""

    color1 = [1, 0.1, 0.2, 1]

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

    # flatten information into plain list
    if flat:
        active = [
            (
                f'[anchor=center]{str(r["position"])}',
                f'[color=#65275d]{r["playback"]["aka"]}[/color]',
                ("alert", color1, r["playback"]["file_name"]),
                r["playback"]["type"],
                r["playback"]["format"],
                f"[anchor=center]{str(r['playback']['audio'])}",
                str(r["playback"]["duration"]),
                r["playback"]["datetime_start_str"],
                r["playback"]["datetime_end_str"],
            )
            for r in active
        ]
        inactive = [
            (
                str(r["position"]),
                r["playback"]["aka"],
                r["playback"]["file_name"],
                r["playback"]["type"],
                r["playback"]["format"],
                str(r["playback"]["audio"]),
                str(r["playback"]["duration"]),
                r["playback"]["datetime_start_str"],
                r["playback"]["datetime_end_str"],
            )
            for r in inactive
        ]

    return active, inactive


class Table(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # set orientation of main boxlayout
        self.orientation = "vertical"

        # split main box layout into two parts
        top_block = BoxLayout(
            orientation="vertical", spacing=15, padding=(10, 0, 10, 10)
        )
        bottom_block = BoxLayout(
            orientation="vertical", spacing=15, padding=(10, 20, 10, 10)
        )

        # load active and inactive data into flat table format
        active, inactive = load_storyboard(flat=True)

        # populate upper box with title and table
        new_widget = MDLabel(
            markup=True,
            text="[b]Loaded[/b]",
            size_hint=(1, 0.1),
            halign="center",
        )
        new_widget.font_size = 35
        top_block.add_widget(new_widget)
        top_block.add_widget(self.generate_table(active))

        # populate lower box with title and table
        new_widget = MDLabel(
            markup=True,
            text="[b]UnLoaded[/b]",
            size_hint=(1, 0.1),
            halign="center",
        )
        new_widget.font_size = 35
        bottom_block.add_widget(new_widget)
        bottom_block.add_widget(self.generate_table(inactive))

        # add both blocks to main box layout
        self.add_widget(top_block)
        self.add_widget(bottom_block)

    def generate_table(self, table_data):
        new_table = MDDataTable(
            column_data=[
                ("Position", dp(20)),
                ("Name", dp(30)),
                ("Filename", dp(30)),
                ("Type", dp(20)),
                ("Format", dp(30)),
                ("Audio", dp(20)),
                ("Duration", dp(30)),
                ("Start Date", dp(30)),
                ("End Date", dp(30)),
            ],
            background_color_header="#FF00FF",
            background_color_selected_cell="e4514f",
        )
        new_table.row_data = table_data
        new_table.size_hint = (1, 0.9)
        return new_table


class KivyApp(MDApp):
    def build(self):
        self.theme_cls.them_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        return Table()


def main():
    kivy.require("2.1.0")
    Window.size = (1200, 600)
    KivyApp().run()


main()
