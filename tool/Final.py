# -*- coding: utf-8 -*-
# @Author: Hewen
# @Time: 9/27/2019 12:34 PM
# @File: Final.py
import time
from kivy.app import App
from kivy import resources
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.progressbar import ProgressBar
from kivy.graphics.vertex_instructions import Rectangle

font_name = resources.resource_find("simfang.ttf")
source_background = r"background.png"


class UIMain(GridLayout):

    def __init__(self):
        super().__init__()
        with self.canvas.before:
            self.rect = Rectangle(size=Window.size, pos=self.pos, source=source_background)
        self.cols = 3
        self.add_widget(UIAutoDownload())
        self.add_widget(UIAutoUpload())


class UIAutoDownload(GridLayout):

    def __init__(self, **kwargs):
        super(UIAutoDownload, self).__init__(**kwargs)
        self.cols = 4
        self.add_widget(self.label_title())
        self.add_widget(UIAutoDownloadUrlhash(size_hint=(.5, 1)))

    @staticmethod
    def label_title():
        label = Label()
        label.text = u"自动收集样本"
        label.font_name = font_name
        label.size_hint = (.1, 1)
        label.halign = "justify"
        return label


class UIAutoDownloadUrlhash(GridLayout):
    def __init__(self, **kwargs):
        super(UIAutoDownloadUrlhash, self).__init__(**kwargs)
        self.cols = 3
        self.add_widget(self.progress())

    @staticmethod
    def progress():
        pb = ProgressBar(max=1000)
        pb.value = 0
        return pb


class UIAutoUpload(GridLayout):

    pass
        # return self.layout

        # super(UIAutoUpload, self).__init__(**kwargs)
        # self.add_widget(Button(text="bb"))


class UI(App):

    def build(self):
        root = UIMain()
        return root


if __name__ == "__main__":
    UI().run()
