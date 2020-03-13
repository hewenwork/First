# encoding = utf-8
# @Author: Hewen
# @Time: 10/23/2019 10:46 AM
# @File: DealDatabase.py
import os
import tkinter
import tkinter.filedialog

import chardet

tkinter.Tk().withdraw()

rule = ""
for i in range(32, 127):
    rule += chr(i)

path_list = []


def file_list(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isdir(file_path):
            file_list(file_path)
        else:
            path_list.append(file_path)
    return path_list


class DealDatabase:

    def __init__(self):
        folder = tkinter.filedialog.askdirectory()
        print(len(file_list(folder)))
        for file_path in file_list(folder):
            if os.path.getsize(file_path) >= 4:
                with open(file_path, "r", encoding=self.file_enconding(file_path))as file:
                    content = file.readlines()
                    for line in content:
                        result = self.jundge_char(line)
                        print(result)

    @staticmethod
    def file_enconding(file_path):
        try:
            with open(file_path, "rb")as file:
                return chardet.detect(file.read())["encoding"]
        except Exception as e:
            print(e)
            return

    @staticmethod
    def jundge_char(line):
        for word in line:
            if word in rule is False:
                return line


if __name__ == "__main__":
    DealDatabase()
