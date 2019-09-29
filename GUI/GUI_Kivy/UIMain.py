# encoding = utf-8
# @Author: Hewen
# @Time: 9/29/2019 9:22 AM
# @File: Test.py
import time
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics.vertex_instructions import Rectangle
from kivy.resources import resource_find
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar

font_name = resource_find(r"C:\Windows\Fonts\simfang.ttf")
source_background = r"background.png"


class UIMain(GridLayout):

    def __init__(self):
        super().__init__()
        self.progress = ProgressBar()
        with self.canvas.before:
            self.rect = Rectangle(size=Window.size, pos=self.pos, source=source_background)
        self.cols = 3
        self.add_widget(self.label_title())
        self.add_widget(self.progressbar())
        self.add_widget(self.button_status())

    @staticmethod
    def label_title():
        label = Label()
        label.text = u"自动收集样本"
        label.font_name = font_name
        return label

    def test_p(self, *args, **kwargs):
        if self.progress.value != 1000:
            time.sleep(1)
            self.progress.value += 100
        else:
            return

    def progressbar(self):
        self.progress.max = 1000
        self.progress.value = 100
        return self.progress

    def button_status(self):
        button = Button()
        button.text = u"哎哎"
        button.font_name = font_name
        button.background_color = (1, 0, 0, 1)
        button.bind(on_press=self.test_p)
        return button


class Main(App):

    def build(self):
        root = UIMain()
        root.title = "Smart Ccl"
        return root


if __name__ == "__main__":
    Main().run()
