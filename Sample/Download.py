# -*- coding: UTF-8 -*-
"""
@author: Hewen
@file:Download.py
@time:2020/08/04
"""
from os import makedirs, path
from datetime import datetime
from urllib.parse import unquote
from urllib3 import disable_warnings
from requests_html import HTMLSession


def log(function):
    def run(*args, **kwargs):
        function_name = function.__name__
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            result = "function: {}, Exception:{}".format(function_name, e)
        with open("Download.log", "a+")as file:
            line = "{}: {}\n".format(datetime.today(), result)
            file.write(line)
        return result

    return run


@log
def download(**kwargs):
    url = kwargs.setdefault("url")
    session = kwargs.setdefault("session", HTMLSession())
    option = kwargs.setdefault("option")
    if option is None:
        params = ['headers', 'cookies', 'auth', 'proxies', 'hooks', 'params', 'verify',
                  'cert', 'prefetch', 'adapters', 'stream', 'trust_env', 'max_redirects']
        option = {key: value for key, value in kwargs.items() if key in params}
        disable_warnings() if "verify" in option else None
        option.setdefault("stream", True)
    response = session.head(url, **option)
    status_code = response.status_code
    headers = response.headers
    if status_code in [301, 302]:
        url = headers["location"]
        return download(url=url, session=session, option=option)
    if status_code != 200:
        return "获取错误, URL:{} status_code{}".format(url, status_code)
    file_dir = kwargs.setdefault("file_dir", path.dirname(__file__))
    makedirs(file_dir) if path.exists(file_dir) is False else None
    file_name = kwargs.setdefault("file_name")
    if file_name is None:
        disposition = headers.setdefault("Content-Disposition")
        file_name = unquote(disposition.split("=")[-1].strip("\"") if disposition else path.basename(url).split("?")[0])
    file_path = kwargs.setdefault("file_path", path.join(file_dir, file_name))
    file_size = path.getsize(file_path) if path.exists(file_path) else 0
    total_size = int(headers.setdefault("content-length", "0"))
    file_mode = "wb" if file_size == 0 else "ab"
    # option["Range"] = "bytes={}-{}".format(file_size, total_size) if total_size != 0 else "bytes={}-".format(file_size)
    chunk_size = 1024 * 1024
    if total_size == file_size:
        return True
    with open(file_path, file_mode) as file:
        for chunk in session.get(url, **option).iter_content(chunk_size=chunk_size):
            file.write(chunk)
    return True


if __name__ == '__main__':
    a = "http://download.iobit.com/toolbox/iobitapps/imf-setup.exe"
    download(url=a)
