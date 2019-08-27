from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout


def get_user(instance, value):
    print(f"{instance}, {value}")

class Test(GridLayout):

    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)
        self.rows = 3
        self.add_widget(Label(text="username"))
        self.username = TextInput(multiline=False, focus=True)
        self.username.bind(on_text_validate=get_user)
        self.add_widget(self.username)
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(Label(text="password"))
        self.add_widget(self.password)
        layout = FloatLayout(size=(100, 200))
        bt = Button(text="aa", size_hint=(.6, .6))
        layout.add_widget(bt)
        self.add_widget(layout)



class Demo(App):

    def build(self):
        return Test()


if __name__ == "__main__":
    Demo().run()
