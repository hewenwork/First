# coding: utf-8
from kivy.app import App
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.behaviors import CoverBehavior, ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image, AsyncImage
from kivy.graphics.instructions import CanvasBase
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


class Test(BoxLayout):

    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.add_widget(LeftMenu(size_hint=(.05, 1)))
        self.add_widget(RightMenu(size_hint=(.95, 1)))


class LeftMenu(BoxLayout):
    def __init__(self, **kwargs):
        super(LeftMenu, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Button(text="lft"))


class RightMenu(BoxLayout):
    def __init__(self, **kwargs):
        super(RightMenu, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(ButtonScan(source=r"C:\Users\hewen\Desktop\images\btn_bdengine_on_over.png", allow_stretch=False,keep_ratio=False))


class ButtonScan(ButtonBehavior, Image):

    def on_press(self):
        print(1)

    def on_release(self):
        print(2)


class CoverImage(CoverBehavior, Image):

    def __init__(self, **kwargs):
        super(CoverImage, self).__init__(**kwargs)
        texture = self._coreimage.texture
        self.reference_size = texture.size
        self.texture = texture


class Demo(App):

    def build(self):
        root = Test()
        return root


if __name__ == "__main__":
    Demo().run()
