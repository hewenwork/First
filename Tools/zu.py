# encoding = utf-8
# @Author: Hewen
# @Time: 12/3/2019 1:13 PM
# @File: Dupl.py
import os
import re
import sys
import chardet
from tkinter import Tk, Button
from datetime import datetime
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename

re_md5 = r"^[a-zA-Z.]*?,[a-z0-9]*?,\d*?\n$"
re_sign = r"^[a-zA-Z.]*?,[0-9]*?,[a-zA-Z0-9]*?,[0-9]*?,[a-zA-Z0-9]*$"
delete_file = os.path.join(os.path.dirname(sys.argv[0]), "delete_ite.txt")


#
# def encoding(file_path):
#     try:
#         with open(file_path, "rb")as file:
#             result = chardet.detect(file.read())["encoding"]
#         return True, result
#     except Exception as e:
#         return False, f"Exception: {e}"

#
# def lines_dict(file_path):
#     result, detail = encoding(file_path)
#     if result is False:
#         return False, detail
#     with open(file_path, "r", encoding=detail)as file:
#         content = {line for line in file.readlines()}
#     return True, content
#
#
# def check_md5(file_path):
#     result, detail = encoding(file_path)
#     if result is False:
#         return False, detail
#     lines_dict(file_path)
#     for line in
#         content = {}
#     delete_list = []
#     with open(file_path, "r", encoding=detail)as file:
#         for line in file.readlines():
#             if re.match(re_md5, line) is None:
#                 delete_list.append(f"{line} is not rule")
#             else:
#                 md5 = line.split(",")[1]
#                 if md5 in content:
#                     delete_list.append(f"{line} is repeat")
#                 else:
#                     content.update({md5: line})
#     with open(file_path, "w", encoding="utf-8")as file:
#         file.writelines(content.values())
#     return delete_list
#
#
# def check_sign(file_path):
#     content = {}
#     delete_list = []
#     encoding = encoding(file_path)
#     with open(file_path, "r", encoding=encoding)as file:
#         for line in file.readlines():
#             if re.match(re_sign, line) is None:
#                 delete_list.append(f"{line} is not rule")
#             else:
#                 content.update({line: line})
#
#     with open(file_path, "w", encoding="utf-8")as file:
#         file.writelines(content.values())
#     return delete_list


class Ui:

    def __init__(self):
        self.app = Tk()
        self.app.geometry("400x400+400+400")
        self.button_md5 = Button(self.app, command=self.func_md5, text="MD5N")
        self.button_sign = Button(self.app, command=self.func_sign, text="SIGN")
        self.button_md5.grid(row=1, column=1)
        self.button_sign.grid(row=2, column=1)
        self.app.mainloop()

    @staticmethod
    def get_path():
        file_path = askopenfilename()
        if os.path.exists(file_path) is False:
            showinfo(message="No select any file !")
            return False
        return file_path

    @staticmethod
    def get_encoding(file_path):
        try:
            with open(file_path, "rb")as file:
                encoding = chardet.detect(file.read())["encoding"]
            return encoding
        except Exception as e:
            message = f"Select path: {file_path}.Encoding {e} !"
            showinfo(message=message)
            return False

    @staticmethod
    def write_log(line):
        with open(delete_file, "a+", encoding="utf-8") as file:
            line = f"{datetime.today()}: {line}" if "\n" in line is False else f"{datetime.today()}: {line}\n"
            file.write(line)

    def base_func(self, rule=None):
        file_path = self.get_path()
        if file_path is False:
            return
        encoding = self.get_encoding(file_path)
        if encoding is False:
            return
        # with open(file_path, "r", encoding=encoding)as file:
        #     content = {line for line in file.readlines()}
        line_dict = {}
        with open(file_path, "r", encoding=encoding)as file:
            # line_set = {line for line in file.readlines()}
            for line in file.readlines():
                # if line in line_set:
                #     self.write_log(line)
                if re.match(re_md5, line) is None:
                    self.write_log(line)
                    continue

                if line_dict.setdefault(line, line) is None:
                    self.write_log(line)

        file_dir = os.path.dirname(file_path)
        file_name = rule + ".deal.txt"
        new_path = os.path.join(file_dir, file_name)
        md5_dict = {line.split(",")[1]: line for line in content if re.match(re_md5, line) is not None}
        with open(new_path, "w", encoding="utf-8")as file:
            for line in md5_dict.values():
                file.write(line)

    def func_md5(self):
        result, detail = self.get_path_encoding()
        if result is False:
            showinfo(message=detail)
            return
        file_path = result
        encoding = detail
        with open(file_path, "r", encoding=encoding)as file:
            content = {line for line in file.readlines()}
        new_path = file_path + ".deal.txt"
        md5_dict = {line.split(",")[1]: line for line in content if re.match(re_md5, line) is not None}
        with open(new_path, "w", encoding="utf-8")as file:
            for line in md5_dict.values():
                file.write(line)
        showinfo(message="ALL DONE !")

    def func_sign(self):
        result, detail = self.get_path_encoding()
        if result is False:
            showinfo(detail)
        else:
            file_path = result
            encoding = detail
            with open(file_path, "r", encoding=encoding)as file:
                content = {line for line in file.readlines()}
            new_path = file_path + ".deal.txt"
            md5_dict = {line.split(",")[1]: line for line in content if re.match(re_md5, line) is not None}
            with open(new_path, "w", encoding="utf-8")as file:
                for line in md5_dict.values():
                    file.write(line)


if __name__ == "__main__":
    Ui()
