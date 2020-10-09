# -*- coding: UTF-8 -*-
"""
@author: Hewen
@file:Gui.py
@time:2020/08/05
"""
from os import path
from re import match
from tkinter import Tk
from tkinter.messagebox import showwarning
from tkinter.filedialog import asksaveasfilename
from tkinter.ttk import Label, Progressbar, Button, Entry
from pyperclip import paste
from datetime import datetime
from urllib.parse import unquote
from requests_html import HTMLSession
from threading import Thread


def thread_function(function, *args):
    Thread(target=function, *args).start()


def thread_action(function):
    # 回调
    def mu(*args, **kwargs):
        # 多线程
        thread = Thread(target=function, args=args, kwargs=kwargs)
        return thread.start()

    return mu


def log(function):
    def run(*args, **kwargs):
        function_name = function.__name__
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            result = "function: {}, Exception:{}".format(function_name, e)
        with open("Gui.log", "a+")as file:
            line = "{}: {}\n".format(datetime.today(), result)
            file.write(line)
        return result

    return run


class Main:

    def __init__(self):
        self.app = self.root()
        self.label_progressbar = self.label(text="进度")
        self.progressbar_download = self.progressbar()
        self.label_speed = self.label(text="Speed: ", state="disable")
        self.button_start = self.button(command=lambda: thread_function(self.function_button))
        self.entry_url = self.entry(width=100)
        self.bind_mouse()
        self.app_grid()
        self.app.mainloop()

    @staticmethod
    def root():
        app = Tk()
        screenheight = app.winfo_screenheight()
        screenwidth = app.winfo_screenwidth()
        app_width = int(screenwidth * 0.4)
        app_height = int(screenheight * 0.4)
        app_y = int((screenheight - app_height) / 2)
        app_x = int((screenwidth - app_width) / 2)
        app.geometry("{}x{}+{}+{}".format(app_width, app_height, app_x, app_y))
        app["bg"] = "pink"  # 背景色
        app.attributes("-alpha", 0.8)  # 虚化
        app.attributes("-toolwindow", True)  # 关闭按钮
        app.wm_attributes('-topmost', 1)  # 置顶
        app.resizable(False, False)  # 窗口不可调整大小
        return app

    def label(self, **kwargs):
        kwargs.setdefault("state", "disable")
        lab = Label(self.app, **kwargs)
        return lab

    def progressbar(self, **kwargs):
        kwargs.setdefault("orient", "horizontal")
        kwargs.setdefault("mode", "determinate")
        kwargs.setdefault("maximum", 100)
        kwargs.setdefault("length", 460)
        kwargs.setdefault("value", 0)
        bar = Progressbar(self.app, **kwargs)
        return bar

    def button(self, **kwargs):
        kwargs.setdefault("text", "点击")
        but = Button(self.app, **kwargs)
        return but

    def entry(self, **kwargs):
        entry_ = Entry(self.app, **kwargs)
        entry_.insert("end", "输入下载地址URL")
        return entry_

    def app_grid(self):
        # self.canvas_.grid(column=0, row=0, columnspan=3)
        self.entry_url.place(x=1, y=1)  # grid(column=0, row=0, padx=10, pady=25, columnspan=3, sticky="w")
        self.label_progressbar.place(x=1, y=30)  # grid(column=0, row=1, padx=10, pady=5)
        self.progressbar_download.place(x=60, y=30)  # grid(column=1, row=1, padx=10, pady=5)
        self.button_start.place(x=200, y=30)  # grid(column=2, row=1, padx=10)
        self.label_speed.place(x=1, y=60)  # grid(column=0, row=2, padx=10, columnspan=3, sticky="w")

    def bind_mouse(self):
        # 鼠标移动到界面上, 界面就取消强制置顶
        self.app.bind("<Enter>", lambda event: self.app.wm_attributes("-topmost", 0))
        self.entry_url.bind("<Button-1>", self.mouse_action)  # lambda event: self.entry_url.delete(0, "end"))

    def function_button(self):
        url = self.entry_url.get()
        re = r"(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]"
        assert match(re, url), showwarning(message=f"不是符合规范的URL:\n{url}")
        func = Download()
        file_name = func.get_file_name(url)
        self.entry_url["state"] = "disable"
        desktop = path.join(path.expanduser("~"), "Desktop")
        file_path = asksaveasfilename(initialdir=desktop, initialfile=file_name)
        self.button_start["state"] = "disable"
        if func.run(url, file_path):
            self.button_start["state"] = "normal"
            self.entry_url["state"] = "normal"
        value = self.progressbar_download["value"]
        maximum = self.progressbar_download["maximum"]
        self.progressbar_download["value"] = (1 + value) if value < maximum else 0
        self.label_speed["text"] = "Speed: 10MB/S, 123/541564"
        self.progressbar_download.update()
        showwarning(message="OK")

    def mouse_action(self, event):
        self.entry_url.delete(0, "end")
        self.entry_url.insert("end", paste())


class Download:
    session = HTMLSession()

    @log
    def get_file_name(self, url: str):
        head = self.session.head(url)
        status_code = head.status_code
        if head.status_code != 200:
            return "status_code: {}".format(status_code)
        headers = head.headers
        disposition = headers.setdefault("Content-Disposition")
        file_name = unquote(disposition.split("filename= ")[-1]) if disposition else unquote(url.split("/")[-1])
        return file_name

    @log
    def run(self, url, file_path):
        chunk_size = 1024 * 1024
        with open(file_path, "wb")as file:
            for chunk in self.session.get(url).iter_content(chunk_size=chunk_size):
                print(1)
                file.write(chunk)
        return True


if __name__ == "__main__":
    Main()
