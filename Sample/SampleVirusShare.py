# -*- coding: UTF-8 -*-
"""
@author: Hewen
@file:SampleVirusShare.py
@time:2020/08/10
"""
from re import findall
from urllib3 import disable_warnings
from urllib.parse import unquote
from datetime import datetime
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from os import path, makedirs

disable_warnings()


def log(function):
    def run(*args, **kwargs):
        function_name = function.__name__
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            result = "function: {}, Exception:{}".format(function_name, e)
        with open("SampleVirusShare.log", "a+")as file:
            line = "{}: {}\n".format(datetime.today(), result)
            file.write(line)
        return result

    return run


@log
def download(**kwargs) -> bool or str:
    url = kwargs.setdefault("url")
    session = kwargs.setdefault("session", HTMLSession())
    requests_params = ['headers', 'cookies', 'auth', 'proxies', 'hooks', 'params', 'verify',
                       'cert', 'prefetch', 'adapters', 'stream', 'trust_env',
                       'max_redirects']
    option = {key: value for key, value in kwargs.items() if key in requests_params}
    option.setdefault("stream", True)
    while True:
        response = session.head(url, **option)
        status_code = response.status_code
        headers = response.headers
        if status_code == 301 or status_code == 302:
            url = headers["location"]
        elif status_code == 200:
            break
        else:
            return "获取错误, URL:{} status_code{}".format(url, status_code)
    file_dir = kwargs.setdefault("file_dir", path.dirname(__file__))
    makedirs(file_dir) if path.exists(file_dir) is False else None
    file_name = kwargs.setdefault("file_name")
    if file_name is None:
        content_disposition = headers.setdefault("Content-Disposition")
        if content_disposition is None:
            file_name = path.basename(url).split("?")[0]
        else:
            file_name = unquote(content_disposition.split("filename=")[-1].strip("\""))
    file_path = kwargs.setdefault("file_path", path.join(file_dir, file_name))
    if path.exists(file_path):
        file_dir = path.dirname(file_path)
        file_name = "new_{}".format(path.basename(file_path))
        file_path = path.join(file_dir, file_name)
    with open(file_path, "wb") as file:
        chunk_size = 1024 * 1024
        for chunk in session.get(url, **option).iter_content(chunk_size=chunk_size):
            file.write(chunk)
    return True


class Run:

    def __init__(self):
        session = self.login()
        for link in self.main_parser(session):
            print(link)
            download(url=link, file_dir=r"C:\Users\hewen\Desktop\New folder", verify=False)

    @staticmethod
    @log
    def login():
        session = HTMLSession()
        url = "https://virusshare.com/processlogin.4n6"
        data = {"username": "ashy", "password": "testvirus0504L"}
        response = session.post(url, data=data)
        return session if "Logout" in response.text else "Login Failed"

    @staticmethod
    @log
    def main_parser(session):
        url = "https://virusshare.com/torrents.4n6"
        response = session.get(url)
        re = r"href=\"(https://tracker.virusshare.com:7000/torrents/VirusShare_00\d{3}.zip.torrent\?\w*?)\">VirusShare"
        link_list = findall(re, response.content.decode())
        return link_list


# if __name__ == "__main__":
    # Run()

import chardet
file = open(r"C:\Users\hewen\Desktop\a.txt", "rb")
content = file.read()
print(content)
file.close()

file = open(r"C:\Users\hewen\Desktop\a.txt", "r", encoding="utf-8")
content = file.read()
print(content)
file.close()