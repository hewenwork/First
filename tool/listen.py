import datetime
import os

import pyperclip
import pytesseract
from PIL import ImageGrab, Image
from pynput.keyboard import Listener, Key
import win32con
import win32clipboard as wincld


def get_text():
    wincld.OpenClipboard()
    text_result = wincld.GetClipboardData(win32con.CF_UNICODETEXT)
    wincld.CloseClipboard()
    return text_result


def set_text(info):
    wincld.OpenClipboard()
    wincld.EmptyClipboard()
    wincld.SetClipboardData(win32con.CF_UNICODETEXT, info)
    wincld.CloseClipboard()


def log_(func):
    def aa(*args, **kwargs):
        result = func(*args, **kwargs)
        with open("Error.log", "a+")as file:
            file.write(f"{datetime.datetime.now()}:{result}\n")

    return aa


class Demo:

    def __init__(self):
        self.before_key = None
        with Listener(on_release=self.press) as self.listener:
            self.listener.join()

    @log_
    def press(self, key):
        if key in Key:
            if key == key.print_screen:
                os.system(f"C:\\WINDOWS\\system32\\mspaint.exe {self.clipbord_copy()}")
            self.before_key = key
        else:
            if self.before_key in Key and key.char == "a":
                print(1)
            self.before_key = key
        return key

    def clipbord_copy(self):
        a = ImageGrab.grabclipboard()
        pp = r"C:\Users\hewen\Desktop\aa.png"

        a.save(pp)
        dd = Image.open(pp)
        dd.crop((0, 0, 400, 400)).save(r"C:\Users\hewen\Desktop\aaa.png")
        yy = Image.open(r"C:\Users\hewen\Desktop\aaa.png")
        text = pytesseract.image_to_string(yy, lang='chi_sim')
        print(text)
        # with open(pp, "w")as file:
        #     file.write(a)
        return pp


if __name__ == "__main__":
    Demo()
