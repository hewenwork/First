# encoding = utf-8
# @Author: Hewen
# @Time: 11/29/2019 11:16 AM
# @File: INITTOOL.py
import os
import chardet
import logging
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import askopenfile
from configparser import ConfigParser

from PIL import ImageTk, Image

logging.basicConfig(**{
    "filemode": "a+",
    "filename": f"{os.path.basename(__file__)}_debug.log",
    "level": logging.INFO,
    "format": "%(asctime)s--: %(lineno)d: %(funcName)s: %(levelname)s - %(message)s"
})
log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())  # print in screen

con = ConfigParser()


def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        log.info(e)
    else:
        return True


def get_encoding(file_path):
    try:
        with open(file_path, "rb")as file:
            content = file.read()
        result = chardet.detect(content)["encoding"]
    except Exception as e:
        log.info(e)
    else:
        if result is None:
            result = "utf-8"
        return result


def messeagebox_(message):
    messagebox = showinfo(title="Information", message=message)
    return messagebox


def read_ini(ini_file):
    try:
        con.read(ini_file, encoding=get_encoding(ini_file))
        ini_dict = {section: {options: values for options, values in con.items(section)} for section in con.sections()}
    except Exception as e:
        log.info(e)
    else:
        return ini_dict


class INITTOOL:

    def __init__(self):
        self.app = self.window()
        self.ini_file = None
        self.ini_dict = None

        # init
        self.entry = Entry(self.app, {"width": 70})
        self.button_chose = Button(self.app, {"width": 10, "text": "选择路径", "command": self.chosse_file})

        self.label_section = Label(self.app, {"text": "Section"})
        self.label_option = Label(self.app, {"text": "Option"})
        self.button_confirm = Button(self.app, {"width": 10, "text": "Confirm", "command": self.func_confirm})

        self.listbox_section = Listbox(self.app)
        self.listbox_section.bind("<Button-1>", self.func_get_section)
        self.text = Text(self.app)

        # grid
        self.entry.grid(row=0, column=0, sticky="NW", padx=10, pady=10, rowspan=3)
        self.button_chose.grid(row=0, column=1, sticky="NW", padx=10, pady=10)

        self.label_section.grid(row=1, column=0, sticky="NW", padx=10)
        self.label_option.grid(row=1, column=1, sticky="NW", padx=10)
        self.button_confirm.grid(row=1, column=2, sticky="NW", padx=10)

        self.listbox_section.grid(row=2, column=0, sticky="e" + "w", padx=10, pady=10)
        self.text.grid(row=2, column=1, sticky="NW", padx=10, pady=10, columnspan=2)
        # start
        self.app.mainloop()

    @staticmethod
    def window():
        window_ = Tk()
        path = r"F:\我的收藏\ICO\background.png"
        canvas = Canvas(window_)

        canvas.create_image(800, 600, image=ImageTk.PhotoImage(Image.open(path)))
        # window_.geometry("600x400+200+200")
        return window_

    def chosse_file(self):
        try:
            file_path = askopenfile(initialdir=r"C:/Users/hewen/Desktop").name
            self.ini_file = file_path
        except Exception as e:
            log.info(e)
            messeagebox_(u"Pls rechoose")
        else:
            self.button_chose["text"] = "re choose"
            self.entry.delete(0, "end")
            self.entry.insert(0, file_path)
            self.ini_dict = read_ini(self.ini_file)
            for section in self.ini_dict.keys():
                self.listbox_section.insert("end", section)
            self.listbox_section.select_set(0)
            _first = self.listbox_section.get(0)
            for options, values in self.ini_dict[_first].items():
                self.text.insert("end", f"{options}={values}\n")

    def func_confirm(self):
        section_index = self.listbox_section.curselection()[0]
        options = self.ini_dict[self.listbox_section.get(section_index)]
        content = self.text.get("1.0", "end")
        options.clear()
        for line in content.split("\n")[0:-2]:
            line_ = line.split("=")
            key = line_[0]
            value = line_[-1]
            # if len(line_) == 1:
            #     key = line_[0]
            #     value = ""
            #     options[key] = value
            # else:
            #     for key, value in line.split("="):
            #         options[key] = value
        # options.clear()
        self.ini_dict.update(section_name_)

        print(self.ini_dict)
        for i in self.ini_dict:
            print(i)
        # self.ini_dict.update(options)

    def func_get_section(self, event):
        section_index = self.listbox_section.curselection()[0]
        options = self.ini_dict[self.listbox_section.get(section_index)]
        self.text.delete("1.0", "end")
        for options_, values in options.items():
            self.text.insert("end", f"{options_}={values}\n")


if __name__ == "__main__":
    INITTOOL()
