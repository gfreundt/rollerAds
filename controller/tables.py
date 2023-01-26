from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ListProperty
from kivy.graphics import Rectangle, Color


class TableColumnTitles(BoxLayout):

    color = ListProperty([0, 0, 0, 1])  # placeholder to avoid error

    def __init__(self, pos, size, **kwargs):
        super().__init__(**kwargs)
        self.color = MAIN.TITLE_COLOR
        with self.canvas:
            Color(0.4, 0.5, 0.7)
            Rectangle(pos=pos, size=size)


class TableRow(ButtonBehavior, BoxLayout):

    color = ListProperty([0, 0, 0, 1])  # placeholder to avoid error

    def __init__(self, row_num, pos, size, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.row = row_num
        self.colorUnselected1 = MAIN.ROW_COLOR_UNSEL1
        self.colorUnselected2 = MAIN.ROW_COLOR_UNSEL2
        self.colorSelected = MAIN.ROW_COLOR_SELECT
        self.color = self.row_color(row_num)
        with self.canvas:
            Color(0.2, 0.1, 0.9)
            Rectangle(pos=self.pos, size=self.size)

    def on_press(self):
        previous, MAIN.row_selected = MAIN.row_selected, self.row
        # switch color of previous selected back to regular
        self.color = self.row_color(self.row)
        # switch color of selected to specific color
        MAIN.TABLE.row_objects[previous].color = self.row_color(previous)

    def row_color(self, row):
        return (
            self.colorSelected
            if row == MAIN.row_selected
            else self.colorUnselected1
            if row % 2 == 0
            else self.colorUnselected2
        )


class Table(BoxLayout):
    def __init__(self, column_data, row_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.column_data = column_data
        self.row_data = row_data
        self.draw_table()

    def draw_table(self):
        num_rows, num_cols = len(self.row_data), len(self.column_data)

        # build Column Titles
        title = TableColumnTitles(self.pos, self.size)
        for col in range(num_cols):
            title.add_widget(Label(text=self.column_data[col]))
        self.add_widget(title)

        # build Rows and Row Data
        self.row_objects = []
        for row in range(num_rows):
            self.data_line = TableRow(row, self.pos, self.size)
            print(self.pos, self.size)
            for col in range(num_cols):
                self.data_line.add_widget(Label(text=self.row_data[row][col]))
            self.add_widget(self.data_line)
            self.row_objects.append(self.data_line)


class KivyApp(App):

    TITLE_COLOR = ListProperty([0.3, 0.3, 0.7, 1])
    ROW_COLOR_UNSEL1 = ListProperty([1, 0, 0, 1])
    ROW_COLOR_UNSEL2 = ListProperty([0, 1, 0, 1])
    ROW_COLOR_SELECT = ListProperty([0, 0, 1, 1])

    def build(self):
        self.row_selected = 0
        column_data = ["Name", "Age", "Gender", "Active"]
        row_data = [
            ["Gabriel", "48", "Male", "Yes"],
            ["Gabriel", "44", "Male", "Yes"],
            ["Gabriel", "12", "Male", "Yes"],
            ["Pepe", "34", "Female", "No"],
        ]
        self.TABLE = Table(column_data, row_data)  # Builder.load_file("table.kv")
        return self.TABLE


# Basic Kivy parameters
Window.size = (1200, 700)
Window.top, Window.left = 50, 50
MAIN = KivyApp()
MAIN.run()
