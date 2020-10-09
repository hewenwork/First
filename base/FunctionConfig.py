# -*- coding: UTF-8 -*-
"""
@author: Hewen
@file:FunctionConfig.py
@time:2020/07/24
"""
from re import findall
from chardet import detect
from datetime import datetime
from configparser import RawConfigParser


def log(function):
    def run(*args, **kwargs):
        function_name = function.__name__
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            result = "function: {}, Exception:{}".format(function_name, e)
        print(result) if result is str else None
        return result

    return run


class Main:

    def __init__(self, *args, **kwargs):
        file_path_en = r"C:\Users\hewen\Desktop\English.lng"
        # file_path1 = r"C:\Program Files (x86)\IObit\IObit Uninstaller\Language\Vietnamese.lng"
        dict_en = self.read_config(file_path_en)
        # dict_ot = self.read_config(file_path1)
        # self.compare_dict(dict_en, dict_ot)
        import os
        for file_name in os.listdir(r"C:\Program Files (x86)\IObit\IObit Uninstaller\Language"):
            file_path = os.path.join(r"C:\Program Files (x86)\IObit\IObit Uninstaller\Language", file_name)
            if os.path.isdir(file_path):
                continue
            file_dict = self.read_config(file_path)
            self.compare_dict(dict_en, file_dict)
        # self.compare_dict(dict_en, dict_ot)

    @log
    def read_config(self, file_path) -> dict:
        """
        :param file_path: 配置文件路径
        :return: 配置文件读取后字典返回, {section:{节点: 值}}
        """
        # 使用Raw避免%转义报错问题
        parser = RawConfigParser()
        # 大小写问题
        parser.optionxform = str
        # 获取文件编码格式
        with open(file_path, "rb")as file:
            encoding = detect(file.read())["encoding"]
        parser.read(file_path, encoding=encoding)
        config_dict = {section: {key: value for key, value in parser.items(section)} for section in parser.sections()}
        return config_dict

    def compare_dict(self, dict1: dict, dict2: dict):
        dict1_name = dict1["Main"]["DisplayName"]
        dict2_name = dict2["Main"]["DisplayName"]
        for section in dict1:
            # print(
            # "{}文件存在section:{}, 多语言{}不存在".format(dict1_name, section, dict2_name)) if section not in dict2 else None
            for key, value in dict1[section].items():
                print(dict2_name, section, key) if key not in dict2[section] else None
                if "%d" in value:
                    print(dict2_name, key) if "%d" not in dict2[section][key] else None
                if "%s" in value:
                    print(dict2_name, key) if "%s" not in dict2[section][key] else None
                if "<br>" in value:
                    br_num1 = findall(r"<br>", value)
                    br_num2 = findall(r"<br>", dict2[section][key])

                    print(dict2_name, key, len(br_num1), len(br_num2)) if len(br_num1) != len(br_num2) else None
                #     if "<a>" not in dict2[section][key]:
                #         print(dict2_name, key) if "</a>" not in value else None

    @staticmethod
    def line_check(line: str):
        if "<a>" in line:
            if "<\a>" not in line:
                print(line)


if __name__ == "__main__":
    Main()
