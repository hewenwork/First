# -*- coding: UTF-8 -*-
"""
@author: Hewen
@file:LanguageCheck.py
@time:2020/08/07
"""

from chardet import detect
from os import listdir, path
from datetime import datetime
from configparser import RawConfigParser


def log(function):
    def run(*args, **kwargs):
        function_name = function.__name__
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            result = "function: {}, Exception:{}".format(function_name, e)
        with open("LanguageCheck.log", "a+", encoding="utf-8")as file:
            line = "{}: {}\n".format(datetime.today(), result)
            file.write(line)
        return result

    return run


con = RawConfigParser()
con.optionxform = str  # 大小写问题


class Main:

    def __init__(self):
        file_dir = r"C:\Users\hewen\Desktop\Language"
        for file_name in listdir(file_dir):
            file_path = path.join(file_dir, file_name)
            aa = self.get_dict_from_config(file_path)
            print(file_path)
            check_list = [("Main", "lbl_DownloadFinished.Caption"), ("Main", "Lan_FinsishDec_M")]
            self.check_same_string(aa, ("Main", "Lan_Finish_M"), check_list)

    @staticmethod
    @log
    def get_dict_from_config(config_path: str) -> dict:
        with open(config_path, "rb")as file:
            content = file.read()
            encoding = detect(content)["encoding"]
        con.read(config_path, encoding=encoding)
        con_dict = {section: {key: value for key, value in con.items(section)} for section in con.sections()}
        return con_dict

    @staticmethod
    @log
    def check_same_string(con_dict: dict, main_string: (), check_string: [()]):
        main_section, main_key = main_string
        main_value = con_dict[main_section][main_key]
        for check in check_string:
            section, key = check
            value = con_dict[section][key]
            if main_value in value:
                print()
            else:
                print("key: {}\nmain: {}\ncheck: {}".format(key, main_value, value))


if __name__ == "__main__":
    Main()


