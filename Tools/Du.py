# encoding = utf-8
# @Author: Hewen
# @Time: 12/3/2019 1:13 PM
# @File: Dupl.py
import os
import re
import sys
import chardet
from tkinter import Tk, Button
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo

re_md5 = r"^[a-zA-Z.]*?,[a-z0-9]*?,\d*?$"
re_sign = r"^[a-zA-Z.]*?,[0-9]*?,[a-zA-Z0-9]*?,[0-9]*?,[a-zA-Z0-9]*$"
delete_file = os.path.join(os.path.dirname(sys.argv[0]), "delete_ite.txt")


def show_over():
    Tk().withdraw()
    showinfo(title="over", message="all done")


def openfilename():
    Tk().withdraw()
    file_path = askopenfilename()
    while file_path is "":
        file_path = askopenfilename()
    return file_path


def file_encoding(file_path):
    try:
        with open(file_path, "rb")as file:
            content = file.read()
            encoding = chardet.detect(content)["encoding"]
    except Exception as e:
        print(e)
    else:
        return encoding


def lines_dict(file_path):
    encoding = file_encoding(file_path)
    content = {}
    with open(file_path, "r", encoding=encoding)as file:
        for line in file.readlines():
            line = line.strip("\n")
            if line in content:
                value = content[line] + 1
                content.update({line: value})
            else:
                content.update({line: 1})
    return content


def check_md5(file_path):
    content = {}
    delete_list = []
    encoding = file_encoding(file_path)
    with open(file_path, "r", encoding=encoding)as file:
        for line in file.readlines():
            if re.match(re_md5, line) is None:
                delete_list.append(f"{line} is not rule")
            else:
                md5 = line.split(",")[1]
                if md5 in content:
                    delete_list.append(f"{line} is repeat")
                else:
                    content.update({md5: line})
    with open(file_path, "w", encoding="utf-8")as file:
        file.writelines(content.values())
    return delete_list


def check_sign(file_path):
    content = {}
    delete_list = []
    encoding = file_encoding(file_path)
    with open(file_path, "r", encoding=encoding)as file:
        for line in file.readlines():
            if re.match(re_sign, line) is None:
                delete_list.append(f"{line} is not rule")
            else:
                content.update({line: line})

    with open(file_path, "w", encoding="utf-8")as file:
        file.writelines(content.values())
    return delete_list


class Ui:

    def __init__(self):
        self.app = self.app_()
        self.button_md5 = Button(self.app, command=self.func_md5, text="MD5N")
        self.button_sign = Button(self.app, command=self.func_sign, text="SIGN")
        self.button_md5.grid(row=1, column=1)
        self.button_sign.grid(row=2, column=1)
        self.app.mainloop()

    @staticmethod
    def app_():
        _ = Tk()
        _.geometry("400x400+400+400")
        return _

    @staticmethod
    def func_md5():
        file_path = openfilename()
        result = check_md5(file_path)
        os.system(f"echo {result} > \"{delete_file}\"")
        show_over()

    @staticmethod
    def func_sign():
        file_path = openfilename()
        result = check_sign(file_path)
        os.system(f"echo {result} > \"{delete_file}\"")
        show_over()


if __name__ == "__main__":
    Ui()
