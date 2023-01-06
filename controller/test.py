import json
import os
import platform

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen, ScreenManager

# from kivy.properties import ListProperty, StringProperty, ObjectProperty
from kivy.clock import mainthread

from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable


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
            MAIN.selected_table[0] = self.active
        else:
            thumbnails = self.inactive_thumbnails
            MAIN.selected_rows[1] = row
            MAIN.selected_table[1] = self.inactive

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
        row = self.selected_row_active
        if row > 0:
            self.active[row]["position"], self.active[row - 1]["position"] = (
                self.active[row - 1]["position"],
                self.active[row]["position"],
            )
            self.update_tables()

    def move_down(self):
        row = self.selected_row_active
        if row < len(self.active_formatted):
            self.active[row]["position"], self.active[row + 1]["position"] = (
                self.active[row + 1]["position"],
                self.active[row]["position"],
            )
            self.update_tables()

    def deactivate(self):
        row = self.selected_row_active
        self.active[row]["active"] = False
        self.active[row]["position"] = 999
        self.update_tables()

    def activate(self):
        row = self.selected_row_inactive
        self.inactive[row]["active"] = True
        self.inactive[row]["position"] = 999
        self.update_tables()

    def unload(self):
        row = self.selected_row_active
        self.inactive.pop(row)
        self.update_tables()

    def save(self):
        pass

    def load_new_file(self):
        efiles = [i["playback"]["file_name"] for i in self.active + self.inactive]
        files = [
            i for i in os.listdir(self.MEDIA_LOCATION) if i not in efiles and "." in i
        ]

    def edit(self, table):
        if MAIN.selected_rows[table] < -1 or not MAIN.selected_table[table]:
            return

        row = MAIN.selected_rows[table]
        self.manager.current = "editProperties"
        idx = self.manager.get_screen("editProperties")
        idx.aka.text = MAIN.selected_table[table][row]["playback"]["aka"]
        idx.file_name.text = MAIN.selected_table[table][row]["playback"]["file_name"]
        idx.type.text = MAIN.selected_table[table][row]["playback"]["type"]
        idx.format.text = MAIN.selected_table[table][row]["playback"]["format"]
        idx.duration.text = str(MAIN.selected_table[table][row]["playback"]["duration"])
        idx.begin.text = MAIN.selected_table[table][row]["playback"][
            "datetime_start_str"
        ]
        idx.end.text = MAIN.selected_table[table][row]["playback"]["datetime_end_str"]
        EditProperties()

    def update_tables(self):
        self.split_active_and_inactive(reload=True)
        self.table_active.update_row_data(self, self.active_formatted)
        self.table_inactive.update_row_data(self, self.inactive_formatted)

    def auto_updater(self, _):
        if self.popup.response:
            if selected_table == 0:
                for k, d in enumerate(self.active):
                    if d["id"] == self.popup.response["id"]:
                        self.active[k] = self.popup.response
            else:
                for k, d in enumerate(self.inactive):
                    if d["id"] == self.popup.response["id"]:
                        self.inactive[k] = self.popup.response

            self.table_updater.cancel()
            self.update_tables()

    def auto_updater_new(self, _):
        if self.add_file.popup.response:
            print("gotcha")
            self.add_file.table_updater.cancel()
            self.update_tables()

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
        idx0 = self.manager.get_screen("loadedMedia")
        idx = self.manager.get_screen("editProperties")
        idx0.table_active.update_row(
            idx0.table_active.row_data[1],
            [
                idx.aka.text,
                idx.file_name.text,
                idx.type.text,
                idx.format.text,
                idx.duration.text,
                idx.begin.text,
                idx.end.text,
            ],
        )
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

        print("sdfsdfsdfsdf")
        self.ids.mineid.text = "Quick"
        """


class AddNewFile(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def func(self):
        print("sdfsdfsdfsdf")
        self.ids.mineid.text = "Quick"


class WindowManager(ScreenManager):
    pass


class KivyApp(MDApp):

    selected_rows = [-1, -1]
    selected_table = [None, None]

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
            f'{sz}{str(i["playback"]["duration"])} s',
            f'{sz}{i["playback"]["datetime_start_str"]}',
            f'{sz}{i["playback"]["datetime_end_str"]}',
        )
        for i in data
    ]


# Basic Kivy parameters
Window.size = (1500, 900)
Window.top, Window.left = 50, 50
Window.clearcolor = (0.5, 0.3, 0.2, 1)
MAIN = KivyApp()
MAIN.run()
