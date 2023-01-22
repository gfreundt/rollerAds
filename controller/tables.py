import random

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.graphics import Rectangle, Color
from kivy.uix.behaviors import ButtonBehavior


from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.pickers import MDDatePicker


class LineLabel(ButtonBehavior, Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_press(self):
        MAIN.row_selected = list(self.ids.keys())[0]
        MAIN.update_table()


class Table(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        title = Label(text="Title")
        self.add_widget(title)
        with self.canvas:
            for i in range(6):
                a = 0.7 if i == MAIN.row_selected else 0.3 if i % 2 == 0 else 0.5
                Color(a, a, a)
                Rectangle(pos=(0, 500 - (100 * i)), size=(1200, 100))
        for i in range(6):
            data_line = BoxLayout(orientation="horizontal")
            for j in range(7):
                info = LineLabel(ids={i: ""}, text=f"Data {str(i)} - {str(j)}")
                data_line.add_widget(info)
            self.add_widget(data_line)


class KivyApp(App):

    row_selected = -1

    def build(self):
        return Table()

    def update_table(self):
        pass


# Basic Kivy parameters
Window.size = (1200, 700)
Window.top, Window.left = 50, 50
MAIN = KivyApp()
MAIN.run()
