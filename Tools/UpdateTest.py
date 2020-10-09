import aiofiles
from sys import argv
from uvicorn import run
from os import path, makedirs
from fastapi import FastAPI, Response
from requests_html import HTMLSession
from socket import gethostbyname_ex, gethostname
from tkinter import Tk, Text
from tkinter.ttk import *

app = FastAPI()
global host
global website
session = HTMLSession()
base_dir = path.dirname(argv[0])  # r"C:\Users\hewen\Desktop\Tools\Update"   #
hosts_content = """# Copyright (c) 1993-2009 Microsoft Corp.
#
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
#
# This file contains the mappings of IP addresses to host names. Each
# entry should be kept on an individual line. The IP address should
# be placed in the first column followed by the corresponding host name.
# The IP address and the host name should be separated by at least one
# space.
#
# Additionally, comments (such as these) may be inserted on individual
# lines or following the machine name denoted by a '#' symbol.
#
# For example:
#
#      102.54.94.97     rhino.acme.com          # source server
#       38.25.63.10     x.acme.com              # x client host

# localhost name resolution is handled within DNS itself.
#	127.0.0.1       localhost
#	::1             localhost
"""

show_info = """
模拟后台的方法, 修改hosts文件使访问指向自己的服务器
适用范围: 一切需要向后台请求文件的测试如: 新闻, version-check.ini, update.ini, 文件更新等
工具使用方法:
1. 真机运行EXE
2. 确认本机IP, 如果不对手动修改
3. 确认要测试的链接地址, 如果不在请手动添加要修改的跳转地址
注: 只添加域名就行
如测试http://download.iobit.com/news/version-check.ini只添加download.iobit.com
4. 点击开始, 弹窗提示OK, 关闭弹窗后, 手动将文件夹下的hosts文件替换虚拟机的hosts文件
5. 手动修改并保存本机目录下的文件, 虚拟机刷新请求就会请求本机的文件"""


def write_hosts_file():
    hosts_file = path.join(base_dir, "hosts")
    with open(hosts_file, "w")as file:
        file.write(hosts_content)
        for line in website.split("\n"):
            new_line = "{}    {}\n".format(host, line)
            file.write(new_line) if len(line) > 4 else None


def get_link_host(file_path):
    for i in website.split("\n"):
        try:
            url = "http://{}/{}".format(i, file_path)
            if session.head(url).status_code == 200:
                print(url)
                return url
        except Exception as e:
            print("出错了: {}".format(e))


def make_new_file(pc_path, web_path):
    url = get_link_host(web_path)
    with open(pc_path, "w", encoding="utf-8")as file:
        file.write(session.get(url).text)


def check_file(pc_path, web_path):
    file_dir = path.dirname(pc_path)
    makedirs(file_dir) if path.exists(file_dir) is False else None
    make_new_file(pc_path, web_path)


@app.get("/{model1}/{model2}/{file_path}")
async def root(file_path: str, model1: str, model2: str):
    web_path = r"{}/{}/{}".format(model1, model2, file_path)
    pc_path = r"{}\{}".format(base_dir, web_path.replace("/", "\\"))
    check_file(pc_path, web_path) if path.exists(pc_path) is False else None
    async with aiofiles.open(pc_path, "rb")as file:
        content = await file.read()
    return Response(content=content, status_code=200)


@app.get("/{model}/{file_path}")
async def root(model: str, file_path: str):
    web_path = r"{}/{}".format(model, file_path)
    pc_path = r"{}\{}".format(base_dir, web_path.replace("/", "\\"))
    check_file(pc_path, web_path)
    async with aiofiles.open(pc_path, "rb")as file:
        content = await file.read()
    return Response(content=content, status_code=200)


class UI:
    def __init__(self):
        self.app = self.get_app()
        self.label_host = self.label(text="请确认本机IP:")
        self.label_website = self.label(text="输入站点默认:\n回车分隔")
        self.entry_host = self.entry()
        self.text_website = self.text_entry()
        self.button_start = self.button(text="start", command=self.get_host)
        self.label_show = self.label(text=show_info)
        self.app_place()
        self.app.mainloop()

    def app_place(self):
        self.label_website.place(x=1, y=1, width=80, height=40)
        self.text_website.place(x=100, y=1, width=280, height=80)
        self.label_host.place(x=1, y=120, width=80, height=40)
        self.entry_host.place(x=100, y=130)
        self.button_start.place(x=100, y=200)
        self.label_show.place(x=160, y=250)

    def button(self, **kwargs):
        button_ = Button(self.app, **kwargs)
        return button_

    @staticmethod
    def get_app() -> Tk:
        app = Tk()
        app.geometry("800x600+10+100")
        app.title("Test")
        app.wm_attributes("-topmost", 0)  # 置顶, -1强制, 0运行时
        return app

    def label(self, **kwargs):
        label_ = Label(self.app, **kwargs)
        return label_

    def entry(self):
        entry = Entry(self.app)
        host = gethostbyname_ex(gethostname())[-1][0]
        entry.insert("end", host)
        return entry

    def text_entry(self):
        text_ = Text(self.app)
        global website
        website = ["download.iobit.com", "update.iobit.com"]
        [text_.insert("insert", i + "\n") for i in website]
        return text_

    def get_host(self):
        self.entry_host["state"] = "disable"
        global host
        host = self.entry_host.get()
        global website
        website = self.text_website.get("0.0", "end")
        self.button_start["state"] = "disable"
        write_hosts_file()
        self.app.destroy()


if __name__ == "__main__":
    UI()
    run(app,
        port=80,
        host=host,
        ssl_keyfile=r"C:\Users\hewen\AppData\Local\mkcert\rootCA-key.pem",
        ssl_certfile=r"C:\Users\hewen\AppData\Local\mkcert\rootCA.pem"
        )
