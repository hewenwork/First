# -*- coding: UTF-8 -*-
"""
@author: Hewen
@file:FakeHttp.py
@time:2020/09/08
"""
from enum import Enum
from uvicorn import run
# from aiofiles import open
from os import path, makedirs
from contextlib import closing
from fastapi import FastAPI, Response
from requests_html import HTMLSession
from configparser import RawConfigParser
from pydantic import BaseModel
from typing import Dict, List, Optional

parser = RawConfigParser()
config_path = r"C:\Users\hewen\Desktop\ac.ini"
parser.read(config_path)
config_dict = {section: {option: value for option, value in parser.items(section)} for section in parser.sections()}

app = FastAPI()
scheme_netloc_list = ["http://update.iobit.com", "http://download.iobit.com", "http://clouddownload.iobit.com"]


def get_source(file_path, url):
    if path.exists(file_path):
        return get_content(file_path)
    else:
        with closing(HTMLSession().get(url)) as response, open(file_path, "wb")as file:
            file.write(response.content)
        return get_source(file_path, url)


def get_true_url(file_path):
    for scheme_netloc in scheme_netloc_list:
        url = f"{scheme_netloc}/{file_path}".replace("\\", "/")
        with closing(HTMLSession().head(url)) as response:
            if response.status_code == 200:
                return url
    return False


def get_content(file_path):
    with open(file_path, "rb")as file:
        return file.read()


@app.get("/ac/geturl.php")
async def get_id(getid: str):
    return config_dict.setdefault(getid, config_dict["null"])


@app.get("/{dir_1}/{file_name}")
async def get_file(dir_1: str, file_name: str):
    file_dir = dir_1
    makedirs(file_dir) if path.exists(file_dir) is False else None
    file_path = path.join(file_dir, file_name)
    url = get_true_url(file_path)
    content = get_source(file_path, url)
    return Response(content=content)


@app.get("/{dir_1}/{dir_2}/{file_name}")
async def get_file(dir_1: str, dir_2: str, file_name: str):
    file_dir = path.join(dir_1, dir_2)
    file_path = path.join(file_dir, file_name)
    makedirs(file_dir) if path.exists(file_dir) is False else None
    url = get_true_url(file_path)
    content = get_source(file_path, url)
    return Response(content=content)


@app.get("/{dir_1}/{dir_2}/{dir_3}/{file_name}")
async def get_file(dir_1: str, dir_2: str, dir_3: str, file_name: str):
    file_dir = path.join(dir_1, dir_2, dir_3)
    file_path = path.join(file_dir, file_name)
    makedirs(file_dir) if path.exists(file_dir) is False else None
    url = get_true_url(file_path)
    content = get_source(file_path, url)
    return Response(content=content)


@app.get("/{dir_1}/{dir_2}/{dir_3}/{dir_4}/{file_name}")
async def get_file(dir_1: str, dir_2: str, dir_3: str, dir_4: str, file_name: str):
    file_dir = path.join(dir_1, dir_2, dir_3, dir_4)
    file_path = path.join(file_dir, file_name)
    makedirs(file_dir) if path.exists(file_dir) is False else None
    url = get_true_url(file_path)
    content = get_source(file_path, url)
    return Response(content=content)


if __name__ == "__main__":
    run(app, host="192.168.1.20", port=80)
