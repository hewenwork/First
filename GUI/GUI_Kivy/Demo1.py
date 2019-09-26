# coding: utf-8
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class Main(BoxLayout):

    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        source = r"background.png"
        with self.canvas.before:
            self.rect = Rectangle(size=Window.size, pos=self.pos, source=source)
        self.orientation = 'vertical'
        self.add_widget(AutoDownload())
        self.add_widget(AutoUpload())


class AutoDownload(BoxLayout):

    def __init__(self, **kwargs):
        super(AutoDownload, self).__init__(**kwargs)
        self.add_widget(Button(text="aa"))


class AutoUpload(BoxLayout):

    def __init__(self, **kwargs):
        super(AutoUpload, self).__init__(**kwargs)
        self.add_widget(Button(text="bb"))


class Demo(App):

    def build(self):
        root = Main()
        return root


if __name__ == "__main__":
    Demo().run()
    # a = "0x6495ED"
    #
    # for i in range(int(len(str(a)) / 2)):
    #     print(
    #         str(a)[
    #             (2 * (i + 1)):(2 * (i + 2))
    #     ]
    #     )
    # print(int(a))
