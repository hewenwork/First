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
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.graphics.vertex_instructions import Rectangle

font_name = resources.resource_find("simfang.ttf")
source_background = r"background.png"


class UIMain(BoxLayout):

    def __init__(self, **kwargs):
        super(UIMain, self).__init__(**kwargs)
        with self.canvas.before:
            self.rect = Rectangle(size=Window.size, pos=self.pos, source=source_background)
        self.orientation = 'vertical'
        self.add_widget(UIAutoDownload())
        self.add_widget(UIAutoUpload())


class UIAutoDownload(BoxLayout):

    def __init__(self, **kwargs):
        super(UIAutoDownload, self).__init__(**kwargs)
        pb = ProgressBar(max=1000)
        pb.value = 0
        self.add_widget(Label(text=u"自动收集样本", font_name=font_name))
        self.add_widget(Label(text=u"状态:", font_name=font_name))
        self.add_widget(pb)
        self.add_widget(Button(text="aa"))


class UIAutoUpload(BoxLayout):

    def __init__(self, **kwargs):
        super(UIAutoUpload, self).__init__(**kwargs)
        self.add_widget(Button(text="bb"))


class UI(App):

    def build(self):
        root = UIMain()
        return root


if __name__ == "__main__":
    UI().run()
