from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ListProperty
from kivy.graphics import Rectangle, Color


class TableColumnTitles(BoxLayout):
    color = ListProperty([0.004, 0, 0.125, 1])

    def __init__(self, pos, size, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(self.color[0], self.color[1], self.color[2])
            Rectangle(pos=pos, size=size)


class TableRow(ButtonBehavior, RelativeLayout):
    colorUnselected1 = ListProperty([0.792, 0.914, 0.961, 1])
    colorUnselected2 = ListProperty([0.95, 0.95, 0.95, 1])
    colorSelected = ListProperty([0.392, 0.629, 0.929, 1])
    row_selected = 0
    row_objects = []

    def __init__(self, row_num, total_rows, **kwargs):
        super().__init__(**kwargs)
        self.row_objects.append(self)
        self.orientation = "horizontal"
        self.row = row_num
        self.total_rows = total_rows
        self.color = self.row_color(row_num)
        with self.canvas:
            self.shape_color = Color(self.color[0], self.color[1], self.color[2])
            self.shape = Rectangle(
                pos=self.pos, size=(Window.width, Window.height / (self.total_rows + 1))
            )

    def row_color(self, row):
        return self.colorUnselected1 if row % 2 == 0 else self.colorUnselected2

    def on_background_color(self, *args):
        print("fdfdfdf")
        self.shape_color = self.colorUnselected2

    def on_press(self):
        print(f"pressed {self.row}")
        self.shape_color = self.colorUnselected2
        return
        self.color = self.colorSelected
        with self.canvas.after:
            self.shape_color = Color(self.color[0], self.color[1], self.color[2])
            Rectangle(pos=self.pos, size=self.size)

        """
        print(f"pressed {self.row}")
        print(self.row_objects)
        self.row_objects[self.row].canvas.clear()
        previous, self.row_selected = self.row_selected, self.row
        # switch color of previous selected back to regular
        # self.color = self.colorSelected  # self.row_color(self.row)
        # switch color of selected to specific color
        # self.row_objects[previous].color = self.row_color(previous)
        for k, i in enumerate(self.row_objects):
            print(k, i.color)
        """


class Table(BoxLayout):
    def __init__(self, column_data, row_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.column_data = column_data
        self.row_data = row_data
        self.draw_table()

    def draw_table(self):
        # build Column Titles
        title = TableColumnTitles(self.pos, self.size)
        for col in self.column_data:
            title.add_widget(Label(text=f"[size=18][b]{col}", markup=True))
        self.add_widget(title)
        # build Rows and Row Data
        self.row_objects = []
        for r, row in enumerate(self.row_data):
            self.data_line = TableRow(r, len(self.row_data))
            for c, col in enumerate(self.column_data):
                self.data_line.add_widget(
                    Label(
                        text=f"[size=16][color=000]{row[c]}",
                        markup=True,
                        pos_hint={"center_x": (c + 0.5) / 4, "center_y": 0.5},
                    )
                )
            self.add_widget(self.data_line)
            self.row_objects.append(self.data_line)


class KivyApp(App):

    TITLE_COLOR = ListProperty([0.004, 0, 0.125, 1])
    print(type(TITLE_COLOR))
    ROW_COLOR_UNSEL1 = ListProperty([0.792, 0.914, 0.961, 1])
    ROW_COLOR_UNSEL2 = ListProperty([0.95, 0.95, 0.95, 1])
    ROW_COLOR_SELECT = ListProperty([0.392, 0.629, 0.929, 1])

    def build(self):
        self.row_selected = 0
        column_data = ["Name", "Age", "Gender", "Active"]
        row_data = [
            ["Gabriel", "48", "Male", "Yes"],
            ["Juan", "44", "Female", "Yes"],
            ["Pedro", "12", "Male", "Yes"],
            ["Pepe", "34", "Female", "No"],
            ["Claudia", "23", "Female", "No"],
        ]
        self.TABLE = Table(column_data, row_data)  # Builder.load_file("table.kv")
        return self.TABLE


# Basic Kivy parameters
Window.size = (1200, 450)
Window.top, Window.left = 50, 50
MAIN = KivyApp()
MAIN.run()
