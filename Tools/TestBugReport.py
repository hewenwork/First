# -*- coding: UTF-8 -*-
"""
@author: Hewen
@file:TestBugReport.py
@time:2020/09/11
"""

from os import path
from chardet import detect
from elevate import elevate
from subprocess import call
from configparser import RawConfigParser
from winreg import HKEY_LOCAL_MACHINE, KEY_READ, KEY_WOW64_32KEY, OpenKey, QueryValueEx
from tkinter import Tk
from tkinter.ttk import Button, Label, Frame
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo, askokcancel


def get_config(config_path):
    config = RawConfigParser()
    with open(config_path, "rb")as file:
        encoding = detect(file.read()).setdefault("encoding", "utf-8")
    config.read(config_path, encoding=encoding)
    main_dict = {section: {key: value for key, value in config.items(section)} for section in config.sections()}
    return main_dict


def run_bug(file_path=None, attr=None):
    assert any([file_path, attr]), "文件路径或报错参数为空"
    # attr = "/testbugreport"
    # file_path = r"C:\Program Files (x86)\IObit\IObit Malware Fighter\SafeBox7.exe"
    command = f"{file_path} {attr}"
    try:
        result = call(command, shell=False)
        return True if result == 1 else False
    except Exception as e:
        return e


def find_registry(registry_path, reg_name) -> tuple or str:
    r"""
    registry_path: SOFTWARE\IObit\IObit Malware Fighter, reg_name: AppPath
    :param
    :param
    :return: value or why
    """
    try:
        with OpenKey(HKEY_LOCAL_MACHINE, registry_path, 0, KEY_READ | KEY_WOW64_32KEY) as reg:
            value = QueryValueEx(reg, reg_name)
            return value
    except Exception as e:
        return e


def get_run_attr(config_dict):
    config_path = r"C:\Users\hewen\Desktop\bug.ini"
    config_dict = get_config(config_path)
    a = get_config(r"C:\Users\hewen\Desktop\bug.ini")
    b = a["IMF"]
    c = b["imf.exe"]
    d = find_registry(b["registry_path"], b["reg_name"])[0]
    file_pa = path.join(d, "imf.exe")
    print()
    print(file_pa, c)
    run_bug(file_pa, c)
    pass


class UI:

    def __init__(self):
        app = self.windows()
        # self.check_config(app)
        self.button_imf = self.get_button(app, text="IMF.exe", command=self.button_imf_function)
        self.button_imftips = self.get_button(app, text="imftips.exe", command=self.button_imf_function)
        self.button_IMFRegister = self.get_button(app, text="IMFRegister.exe", command=self.button_imf_function)
        self.button_AutoUpdate = self.get_button(app, text="IMFRegister.exe", command=self.button_imf_function)
        self.button_SafeBox7 = self.get_button(app, text="IMFRegister.exe", command=self.button_imf_function)
        self.button_IMFcore = self.get_button(app, text="IMFRegister.exe", command=self.button_imf_function)
        self.grid_widget()
        app.mainloop()

    @staticmethod
    def check_config(app: Tk):
        # def get_config_path():
        #     file_path = askopenfilename()
        #     return file_path

        config_path = "main.ini"
        if path.exists(config_path) is False:
            message = f"没有发现配置文件{config_path}, 请确认存在此文件"  # \n点击OK手动选择配置文件, 点击Cancel退出程序"
            showinfo(title="Error", message=message)
            app.destroy()

    @staticmethod
    def windows():
        app = Tk()
        app.geometry("600x600+200+100")
        app.title("Bugreport Tools")
        return app

    @staticmethod
    def get_button(app: Tk, **kwargs):
        button = Button(app, **kwargs)
        return button

    def button_imf_function(self):
        self.button_imf["text"] = "a"

    def grid_widget(self):
        self.button_imf.pack()


class Main:

    def __init__(self):
        app = self.windows()
        page = Frame(app)
        button_imf = self.get_button(app, text="IMF", command=lambda: PageIMF(page))
        button_iu = self.get_button(app, text="IU", command=lambda: PageIU(page))
        button_imf.grid(row=0, column=0)
        button_iu.grid(row=0, column=1)
        page.grid(row=1, column=0)
        #
        # PageIMF(app)
        # PageIU(app)
        app.mainloop()

    @staticmethod
    def windows():
        app = Tk()
        app.geometry("600x600+200+100")
        app.title("Bugreport Tools")
        return app

    @staticmethod
    def get_button(app: Tk, **kwargs):
        button = Button(app, **kwargs)
        return button


class PageIMF:

    def __init__(self, window: Frame):
        for widget in window.winfo_children():
            widget.destroy()
        # window.grid_forget()
        imf_test = Button(window, text="imf", command=lambda: self.change(window))
        imf_label = Label(window, text="im label")
        imf_test.grid(row=0, column=0)
        imf_label.grid(row=1, column=0)

    # def button_IMF(self):

    @staticmethod
    def change(page):
        page.grid_forget()


class PageIU:

    def __init__(self, window: Frame):
        for widget in window.winfo_children():
            widget.destroy()

        bb = Button(window, text="iu", command=lambda: self.change(window))
        bb.grid(row=0, column=0)

    # def button_IMF(self):

    @staticmethod
    def change(page):
        page.grid_forget()


if __name__ == "__main__":
    # elevate(show_console=False)  # False不显示调用窗口
    Main()
    # print(psutil.disk_usage("/"))
