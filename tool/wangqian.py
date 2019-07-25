import os
import pyperclip
import configparser
from pynput.keyboard import Listener


class WangQian:

    def __init__(self):
        self.init_num = 1#int(input("pls input your start picture num , the default is 1"))
        pyperclip.copy("%s.jpg" % self.init_num)
        with Listener(on_release=self.release) as listener:
            listener.join()

    def get_setting(self):
        con = configparser.ConfigParser()

    def release(self, key):
        try:
            if key.char == "q":
                input("quit this script")
                return False
            elif key.char == "v":
                self.init_num += 1
                pyperclip.copy("%s.jpg" % self.init_num)
            elif key.char == "z":
                self.init_num -= 1
                pyperclip.copy("%s.jpg" % self.init_num)
            elif key.type == "aaa":
                print(111)
        except AttributeError as e:
            pass


if __name__ == "__main__":
    WangQian()