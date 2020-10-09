# -*- coding: UTF-8 -*-
"""
@author: Hewen
@file:AbstractMd5.py
@time:2020/08/11
"""
from random import choice
from chardet import detect
from os import path, system
from threading import Thread
from datetime import datetime
from re import findall, match
from requests_html import HTMLSession

from tkinter import Tk
from tkinter.ttk import Button, Label
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilenames


def log(function):
    if callable(function):
        def run(*args, **kwargs):
            function_name = function.__name__
            try:
                result = function(*args, **kwargs)
            except Exception as e:
                result = "function: {}, Exception:{}".format(function_name, e)
            with open("AbstractMd5.log", "a+")as file:
                line = "{}: {}, {}\n".format(datetime.today(), function_name, result)
                file.write(line)
            return result

        return run
    else:
        with open("AbstractMd5.log", "a+")as file:
            line = "{}: {}\n".format(datetime.today(), function)
            file.write(line)


api_key_list = [
    'bf33b55b49c2b8fe06dca09e114e2226cffcac2d214f8c8cd92a976e7f0fe696',
    'fb007f45821a070fe8c60fbab00e38f43e27d218b63b281eceeebfa24b682b40',
    'ebb69c2b5fc6bd3f67ff36f28c66cd489e025a321fb0f4e40c985c34e97c9b09s',
    'e63fff6ec2f1d351b56e263e6903cf7199ecba26bd01046c69f4f92b3d79d09e',
    '6172001af0588434c0ff9d7d78da7b1556939a252709f663987fa3bcbc7009ce',
    'ae52dc0bf7fb17444515f9911e243d03442ac4bf9448aa44dc6f3cf6f88a1fad',
    '6e58eb435d8eb9e137ce7cb9c63ffce33081e9dababd094c2fcdfc4647139086',
    '010696052677d9f1962e8a1de5cb22e1ddeed5ed854ab6eae6836de2d1a6498e',
    'cdd061806b4cc5264b8fde9cb61c9093d3396a6bafb7b77bda27a208d8cc1804',
    '9bfb9694197e0812e6fc735fc90eb21b4e3e6dd1f058ad452b5b48df4ea70dd9',
    '6fcd7437a39b77c405601a83c02a16d882b7c258a82b24499cd1660cc428df3a',
    '92bb1fdbb853890322be3291b2955135d9479e1307f3fe1af8aba403843e8cc8',
    '286087a0e2c1d52e66126467807d9ec33d0a1ba15148e2280252ad060e50f501',
    'b847e5bc4203cdb8245f5d6c8ab5e8606b31a73ef268f3ab474da288a419b8aa',
    '3f8ef86651609fb3fda4134d6433762efa5bbc30ca1cd1b491c584e410a1d384',
    'd8ac8c77f6c3b297750c0ba92484f06a8037075049ff79101b921d6d36104559',
    'a7450f5a40fccd2d761d83593ce8f918960b49de12b6ec172759ab485591fa71',
    '5926cc5a2d8ff785ba7973228aa5053183d61111d02c9a0a6a98ea76c05f8ac7',
    'de25ed07259c081b8bd873a8248022c6c138419f95339cea8eecf02313d7f6e0',
    'ee07787779550e5031d061220fd30eb504ac7bceac820736005c878acba5f15b',
    '2243746e5f13d38e8907355aa543b9eeb53a9a5df02c07f976ee03fc4f086781',
    'a5efd48f0b928a7a77ba0c20e803991d3ebe50add87a97e7a680cd802e64bc88',
    '6c78677baf1f91105bd165578eb4ed36b702ee52b5aba06a9c22d54c52d98d8d',
    'b9b4d1cf70ad6c849df565e9b4fc11dbc508d915332a42a9cbca175c76097b7c',
    '626f13733c1ab37b459fe2b362a9d9c037822be429c3a8b59ec89a6631b2a55b',
    '5dc4d2be4a434cd2b7abc651cb3e9a09ec311770cd8474310ab0d91445d466ec',
    '27ef571e4443ffc42395e69a939106a7f8740951c83aecb14d63959ea779b7ea',
    'd09dca26deddad1aadeb767f2762b80c6e0570596b5671a0e32c70afa4a853c9',
    '809886425d3c5e955849890d3ac2c235f63cebd57aff0454fd5d5fe98160c559',
    '6d3305d504ccd66c95fb23de209aabbef50793746e9bed97cb46a5ad3be3d1a9',
    '392ff7ebbfee647c2141e7b4ac4c9ee3d7242608a4ff8b56ba943daf2b40c4a6',
    '0106dfd35f87f68df9cd3a6fb5decd71de0f6dba6c954fc4d7003ed152b4279d',
    '78c0d9b5d93eec1a6118d0c27c05d2cf43ca1b1d8f85a5b64491134781b8a5c0',
    '33a9068c3937d8e17846767c8c344ff4f932140704362e2546d2c4dc5d85e436',
    'a5424fa7a0b9a81d2b11845dba0a694da2a9763e06fb9392e6d2af59469a1fd8',
    '40dde2e5940bccd39ec8a3af05c2ce46cc4aa7ad4f2599d9eab832b6fbfd5661',
    'd5a63233aa9309c2d53f15bf945e01ffccaea56727f87ed2e2779e686b3aa758',
    'ca8073c043cc387b585657e17f8c8ea9fa3dcec37679403aec98b76a77e439ae',
    '9d75fb43e225104caaf9ff567b13969850ee132dc0842158cec82cd397dca5f5',
    'c6225b29a41a9084271387b16130332efb838003fdcd6b6bb1001c1e07dbc230',
    'c8dfa1603a030e1dfed7c1466f18c93f0ddcdca9d8df6ef323fb1482df496d10'
]
session = HTMLSession()


@log
def report(md5: str):
    api_key = choice(api_key_list)
    url = "https://www.virustotal.com/vtapi/v2/file/report"
    params = {"apikey": api_key, "resource": md5}
    json = session.get(url, params=params)
    if json.status_code == 403:
        return report(md5)
    return json.json().setdefault("positives", "VT无数据")


@log
def abstract_file(file_path: str) -> list:
    with open(file_path, "rb")as file:
        encoding = detect(file.read())["encoding"]
    with open(file_path, "r", encoding=encoding)as file:
        re = r"^[\w\.]*?,\s\w*?,\s.*?,\s\d*?.*?$"
        line_list = [line for line in file.readlines() if match(re, line)]
        return line_list


@log
def parse_line_list(line_list: list) -> dict:
    database_dict = {}
    for line in line_list:
        re_index = r"^[\w\.]*?,\s\w*?,\s.*?,\s(\d{1,8})"
        index = findall(re_index, line)[0]
        if index in database_dict:
            database_dict[index].append(line)
        else:
            database_dict[index] = [line]

    return database_dict


@log
def parse_index(index_dict: dict):
    positives_dict = {}
    file_path = path.join(path.expanduser("~"), r"Desktop\VirusTotal.txt")
    with open(file_path, "w", encoding="utf-8")as file:
        file.write("分析结果如下:\n")
        for index, detail in index_dict.items():
            index_line = "\n---数据库编号:{}\n".format(index)
            file.write(index_line)
            for line in detail:
                md5 = line.split(index)[-1].strip(", ")
                positives = positives_dict.setdefault(md5, report(md5)) if len(md5) == 33 else "没有MD5"
                md5_line = "Positives:{}, 原始数据:{}".format(positives, line)
                file.write(md5_line)


class UI:
    text = r'''
工具流程
1. 点击按钮选择扫描日志文件 (可以一次性选择多个文件)
2. 程序合并所有日志信息, 并以相同编号分类
3. 将所有编号的MD5发送到vt上查询
4. 汇总所有信息在桌面生成文档VirusTotal.txt
分析结果如下:

---数据库编号:12013776
Positives:25, 原始数据:Trojan.Generic, MD5, C:\$Recycle.Bin1\1$1.class, 12013776, 21f2312a9d50f72810e242f72e751243

---数据库编号:14539955
Positives:19, 原始数据:Trojan, MD5, C:\$Recycle.Bin\HD3P.exe, 14539955, 42e661f5b4251eeb00e6c968ef0750ba


---------------------------工具维护人: 贺文---------------------------
使用过程如有任何问题请联系解决
'''

    def __init__(self):
        app = Tk()
        app.title("误报提取工具")
        app.geometry("800x500+100+100")
        self.button = Button(app, text="选择文件开始查询", command=lambda: Thread(target=self.run).start())
        label = Label(app, text=self.text)
        self.button.place(x=200, y=10)
        label.place(x=1, y=40)
        app.mainloop()

    def run(self):
        self.button["state"] = "disable"
        desktop_path = path.join(path.expanduser("~"), "desktop")
        file_path_list = askopenfilenames(initialdir=desktop_path)
        line_list = [line for file_path in file_path_list for line in abstract_file(file_path)]
        index_dict = parse_line_list(line_list)
        print(index_dict)
        parse_index(index_dict)
        showinfo(title="提示", message="操作完成, 结果请查看桌面VirusTotal.txt")
        result_path = path.join(desktop_path, "VirusTotal.txt")
        command = "notepad \"{}\"".format(result_path)
        system(command)
        self.button["state"] = "normal"


def test():
    line_list = abstract_file(r"C:\Users\hewen\Desktop\aa.txt")
    database_dict = parse_line_list(line_list)
    parse_index(database_dict)
    # print(database_dict)


if __name__ == "__main__":
    UI()
    # test()

