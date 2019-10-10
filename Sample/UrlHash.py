# encoding = utf-8
# @Author: Hewen
# @Time: 9/30/2019 3:34 PM
# @File: UrlHash.py

import requests
import datetime
import threading
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.resources import resource_find
from kivy.uix.progressbar import ProgressBar
from kivy.graphics.vertex_instructions import Rectangle


font_name = resource_find(r"C:\Windows\Fonts\simfang.ttf")
source_background = r"background.png"


class UrlHash(GridLayout):

    def __init__(self):
        super().__init__()
        today = datetime.datetime.today()
        date_interval = datetime.timedelta(days=1)
        self.download_date = (today - date_interval).strftime("%Y-%m-%d")
        self.session = requests.session()
        self.cols = 3
        self.label = Label()
        self.button = Button()
        self.progressbar = ProgressBar()
        self.add_widget(self.addlabel())
        self.add_widget(self.addprogress())
        self.add_widget(self.addbutton())

    def addlabel(self):
        self.label.text = f"UrlHash: downlaod progerss 0"
        return self.label

    def addprogress(self):
        self.progressbar.max = 100
        self.progressbar.value = 0
        return self.progressbar

    def addbutton(self):
        self.button.text = "start"
        self.button.bind(on_press=self.buttons)
        return self.button

    def buttons(self, *args):
        self.button.text = "s"
        self.button.state = 'down'
        thread = threading.Thread(target=self.download)
        thread.setDaemon(True)
        thread.start()

    def download(self, *args):
        file_path = r"C:\Users\hewen\Desktop\AutoCo.zip"
        download_url = f"https://urlhaus-api.abuse.ch/downloads/{self.download_date}.zip"
        start_size = 0
        chunk_size = 1024 * 1024
        response = self.session.get(url=download_url, stream=True)
        if response.status_code == 200:
            total_size = int(response.headers["content-length"])
            with open(file_path, "wb")as file:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    file.write(chunk)
                    start_size += 1024
                    download_process = int(start_size / total_size * 100)
                    self.progressbar.value = download_process + 10
                    self.label.text = f"UrlHash: downlaod progerss {start_size} of {total_size}"
        else:
            self.label.text = f"UrlHash: Has`t Data Today"


class Main(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = root = UrlHash()
        with root.canvas.before:
            self.rect = Rectangle(size=root.size, pos=root.pos, source=source_background)
        self.root.bind(size=self._update_rect, pos=self._update_rect)
        self.build()

    def build(self):
        return self.root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


if __name__ == "__main__":
    Main().run()
