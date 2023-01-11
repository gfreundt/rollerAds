import json
import os
import platform
from datetime import datetime as dt

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.clock import mainthread

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu


class LoadedMedia(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # define media directory
        self.MEDIA_LOCATION = r"C:\pythonCode\rollerAds\media"

        # initial states of selected rows for both tables and selected table
        self.selected_row_active = 0
        self.selected_row_inactive = 0

        # load data from JSON file and create active and inactive lists
        self.load_storyboard()
        self.split_active_and_inactive()

        # load generated data into table and replace layout placeholder
        @mainthread
        def delayed():
            idx = MAIN.SCREEN.get_screen("loadedMedia").ids
            self.table_active = self.generate_table(
                idx.table_active,
                self.active_formatted,
            )
            self.table_inactive = self.generate_table(
                idx.table_inactive,
                self.inactive_formatted,
            )

        delayed()

    def row_selected(self, table, cell):
        row = cell.index // 8
        if table.parent.uid < 150:
            thumbnails = self.active_thumbnails
            MAIN.selected_rows[0] = row
            MAIN.selected_tables[0] = self.active
        else:
            thumbnails = self.inactive_thumbnails
            MAIN.selected_rows[1] = row
            MAIN.selected_tables[1] = self.inactive

        # idx = self.manager.get_screen("editProperties")
        # idx.aka.text = selected_table[row]["playback"]["aka"]
        # idx.file_name.text = selected_table[row]["playback"]["file_name"]
        # idx.type.text = selected_table[row]["playback"]["type"]
        # idx.format.text = selected_table[row]["playback"]["format"]
        # idx.duration.text = str(selected_table[row]["playback"]["duration"])
        # idx.begin.text = selected_table[row]["playback"]["datetime_start_str"]
        # idx.end.text = selected_table[row]["playback"]["datetime_end_str"]

        # copy complete information to reassemble record for json archive
        # self.full_record = row_data
        # extract playback information from full record
        # self.row_record = row_data["playback"]
        # define ids pointer

        # idx.aka.text = self.row_record["aka"]
        # idx.file_name.text = self.row_record["file_name"]
        # idx.type.text = self.full_record["type"]
        # idx.format.text = self.full_record["format"]
        # idx.duration.text = str(self.full_record["duration"])
        # idx.begin.text = self.full_record["datetime_start_str"]
        # idx.end.text = self.full_record["datetime_end_str"]

        self.ids.image_preview.source = os.path.join(
            self.MEDIA_LOCATION,
            "thumbnails",
            thumbnails[row],
        )

    def move_up(self):
        row = MAIN.selected_rows[0]
        if row > 0:
            self.active[row]["position"], self.active[row - 1]["position"] = (
                self.active[row - 1]["position"],
                self.active[row]["position"],
            )
            self.update_tables()

    def move_down(self):
        row = MAIN.selected_rows[0]
        if row < len(self.active_formatted):
            self.active[row]["position"], self.active[row + 1]["position"] = (
                self.active[row + 1]["position"],
                self.active[row]["position"],
            )
            self.update_tables()

    def deactivate(self):
        if len(self.active) > 0:
            row = MAIN.selected_rows[0]
            self.active[row]["active"] = False
            self.active[row]["position"] = 999
            self.update_tables()
            MAIN.selected_rows[0], MAIN.selected_tables[0] = -1, None

    def activate(self):
        if len(self.inactive) > 0:
            row = MAIN.selected_rows[1]
            self.inactive[row]["active"] = True
            self.inactive[row]["position"] = 999
            self.update_tables()
            MAIN.selected_rows[1], MAIN.selected_tables[1] = -1, None

    def unload(self):
        if len(self.inactive) > 0:
            row = MAIN.selected_rows[1]
            self.inactive.pop(row)
            self.update_tables()
            MAIN.selected_rows[1], MAIN.selected_tables[1] = -1, None

    def save(self):
        pass

    def load_new_file(self):
        efiles = [i["playback"]["file_name"] for i in self.active + self.inactive]
        files = [
            i for i in os.listdir(self.MEDIA_LOCATION) if i not in efiles and "." in i
        ]

    def edit(self, table):
        if MAIN.selected_rows[table] < -1 or not MAIN.selected_tables[table]:
            return

        row = MAIN.selected_rows[table]
        self.manager.current = "editProperties"
        idx = self.manager.get_screen("editProperties")
        idx.aka.text = MAIN.selected_tables[table][row]["playback"]["aka"]
        idx.file_name.text = MAIN.selected_tables[table][row]["playback"]["file_name"]
        idx.type.text = MAIN.selected_tables[table][row]["playback"]["type"]
        idx.format.text = MAIN.selected_tables[table][row]["playback"]["format"]
        idx.duration.text = str(
            MAIN.selected_tables[table][row]["playback"]["duration"]
        )
        idx.begin.text = MAIN.selected_tables[table][row]["playback"]["date_start"]
        idx.end.text = MAIN.selected_tables[table][row]["playback"]["date_end"]
        MAIN.table = table

    def update_tables(self):
        self.split_active_and_inactive(reload=True)
        self.table_active.update_row_data(self, self.active_formatted)
        self.table_inactive.update_row_data(self, self.inactive_formatted)

    def load_storyboard(self):
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
        self.active = sorted(
            [i for i in storyboard if i["active"]], key=lambda i: i["position"]
        )
        self.inactive = sorted(
            [i for i in storyboard if not i["active"]], key=lambda i: i["position"]
        )

    def split_active_and_inactive(self, reload=False):
        if reload:
            ai = self.active + self.inactive
            # select all active, sort them ascending and number consecutive from 1
            self.active = sorted(
                [i for i in ai if i["active"]], key=lambda i: i["position"]
            )
            for k, i in enumerate(self.active, start=1):
                i["position"] = k
            # select all inactive, sort them ascending and number consecutive from 1
            self.inactive = sorted(
                [i for i in ai if not i["active"]], key=lambda i: i["position"]
            )
            for k, i in enumerate(self.inactive, start=1):
                i["position"] = k

        # create list of images for use with thumbnails
        self.active_thumbnails = [i["thumbnail"] for i in self.active]
        self.inactive_thumbnails = [i["thumbnail"] for i in self.inactive]

        # flatten information into plain list and add markup formatting
        self.active_formatted = flatten_and_format(self.active, 14)
        self.inactive_formatted = flatten_and_format(self.inactive, 14)

    def generate_table(self, table_id, table_data):
        new_table = MDDataTable(
            column_data=[
                ("#", dp(15)),
                ("Name", dp(30)),
                ("Filename", dp(35)),
                ("Type", dp(15)),
                ("Format", dp(15)),
                ("Duration", dp(25)),
                ("Start Date", dp(30)),
                ("End Date", dp(30)),
            ],
            background_color_header="#b0bec5",
            background_color_selected_cell="#FFFFFF",
            elevation=0,
            use_pagination=True,
        )
        new_table.row_data = table_data
        new_table.bind(on_row_press=self.row_selected)
        table_id.add_widget(new_table)
        return new_table


class EditProperties(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.type_values = list(MAIN.format_options.keys())
        self.format_values = ""  # MAIN.format_options[self.ids.type.text]

        """
        self.dropdown = MDDropdownMenu()
        self.dropdown.items = [
            {
                "viewclass": "MDMenuItem",
                "icon": "git",
                "text": "Example",
                "callback": self.test,
            },
            {
                "viewclass": "MDMenuItem",
                "icon": "git",
                "text": "Test",
                "callback": self.test,
            },
        ]
        """

        # copy complete information to reassemble record for json archive
        # self.full_record = row_data
        # extract playback information from full record
        # self.row_record = row_data["playback"]
        # define ids pointer

        # idx.aka.text = self.row_record["aka"]
        # idx.file_name.text = self.row_record["file_name"]
        # idx.type.text = self.full_record["type"]
        # idx.format.text = self.full_record["format"]
        # idx.duration.text = str(self.full_record["duration"])
        # idx.begin.text = self.full_record["datetime_start_str"]
        # idx.end.text = self.full_record["datetime_end_str"]

    def edit_save(self):
        # validate data entered
        error_message = ""
        if len(self.ids.aka.text) < 1:
            error_message += "- Name cannot be empty.\n"
        if not self.ids.format.text:
            error_message += "- Format not selected.\n"
        if float(self.ids.duration.text) <= 0:
            error_message += "- Duration must be greater than 0.\n"
        if dt.strptime(self.ids.end.text, "%a, %d %b %Y") < dt.now():
            error_message += "- End date must be in the future."
        if error_message:
            alert = AlertPopup()
            alert.ids.error_message.text = error_message
            alert.open()
            return

        sz = "[size=14]"
        idx = self.manager.get_screen("loadedMedia")
        t = idx.table_active if MAIN.table == 0 else idx.table_inactive
        t.update_row(
            t.row_data[MAIN.selected_rows[MAIN.table]],
            [
                f"{sz}{MAIN.selected_rows[MAIN.table] + 1}",
                f"{sz}{self.ids.aka.text}",
                f"{sz}{self.ids.file_name.text}",
                f"{sz}{self.ids.type.text}",
                f"{sz}{self.ids.format.text}",
                f"{sz}{float(self.ids.duration.text):.1f}",
                f"{sz}{self.ids.begin.text}",
                f"{sz}{self.ids.end.text}",
            ],
        )
        self.manager.current = "loadedMedia"

        """
        self.response = self.full_record | (
            {
                "playback": {
                    "aka": self.ids.aka.text,
                    "file_name": self.ids.file_name.text,
                    "type": self.ids.type.text,
                    "format": self.ids.format.text,
                    "duration": self.ids.duration.text,
                    "datetime_start_num": dt.strptime(
                        self.ids.begin.text, "%H:%M:%S %d/%m/%Y"
                    ),
                    "datetime_end_num": dt.strptime(
                        self.ids.end.text, "%H:%M:%S %d/%m/%Y"
                    ),
                    "datetime_start_str": self.ids.begin.text,
                    "datetime_end_str": self.ids.end.text,
                }
            }
        )

        
        """

    def date_picker(self):
        today = dt.now()
        dialog = MDDatePicker(
            mode="range", year=today.year, month=today.month, day=today.day
        )
        dialog.bind(on_save=self.on_date_picker_ok)
        dialog.open()

    def on_date_picker_ok(self, _, value, date_range):
        self.ids.begin.text = dt.strftime(date_range[0], "%a, %d %b %Y")
        self.ids.end.text = dt.strftime(date_range[-1], "%a, %d %b %Y")

    def on_selected_type(self):
        self.ids.format.text = ""
        self.ids.format.values = MAIN.format_options[self.ids.type.text]


class AddNewFile(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drives = [
            i for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{i}:")
        ]

    def on_selection(self, _, filename):
        if not filename:
            return

        bs = "\\"
        path = bs.join(filename[0].split(bs)[:-1])
        self.ids.selected_file_name.text = f"File Name: {filename[0].split(bs)[-1]}"
        self.ids.selected_file_path.text = f"File Path: {path}"
        self.ids.selected_file_size.text = (
            f"File Size: {os.path.getsize(filename[0])//1024:,} Kb"
        )
        self.ids.selected_file_created.text = f"Created on: {dt.fromtimestamp(os.path.getctime(filename[0])).strftime('%a, %d %b %Y')}"
        self.ids.selected_file_image.source = filename[0]


class AlertPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class WindowManager(ScreenManager):
    pass


class KivyApp(MDApp):
    selected_rows = [-1, -1]
    selected_tables = [None, None]
    format_options = {
        "Video": ["MOV", "MKV", "MP4", "AVI", "GIF"],
        "Image": ["JPG", "PNG", "BMP"],
        "Document": ["PDF", "PPT"],
    }

    def build(self):
        self.SCREEN = Builder.load_file("test.kv")
        return self.SCREEN


def flatten_and_format(data, size):
    # ("alert", color1, r["playback"]["file_name"]),
    sz = f"[size={str(size)}]"
    return [
        (
            f'{sz}{str(i["position"])}',
            f'{sz}{i["playback"]["aka"]}',
            f'{sz}{i["playback"]["file_name"]}',
            f'{sz}{i["playback"]["type"]}',
            f'{sz}{i["playback"]["format"]}',
            f'{sz}{str(i["playback"]["duration"])}',
            f'{sz}{i["playback"]["date_start"]}',
            f'{sz}{i["playback"]["date_end"]}',
        )
        for i in data
    ]


# Basic Kivy parameters
Window.size = (1500, 900)
Window.top, Window.left = 50, 50
Window.clearcolor = (0.5, 0.3, 0.2, 1)
MAIN = KivyApp()
MAIN.run()
