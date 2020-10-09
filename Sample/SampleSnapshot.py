#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: Hewen
"""
from urllib import parse
from os import path, makedirs, popen, remove
from urllib3 import disable_warnings
from requests_html import HTMLSession
from datetime import datetime, timedelta

date_today = datetime.today()
date_download = date_today - timedelta(days=2)
log_dir = path.join(path.dirname(__file__), "Log")
makedirs(log_dir) if path.exists(log_dir) is False else None
log_path = path.join(log_dir, date_today.strftime("%Y-%m-%d.log"))
sm_dir = r"G:\Auto"
file_dir = r"G:\AutoSample\Snapshot"
makedirs(file_dir) if path.exists(file_dir) is False else None
disable_warnings()


def log(function):
    def write_log(*args, **kwargs):
        function_name = function.__name__
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            result = "Exception:{}".format(e)
        with open(log_path, "a+", encoding="utf-8")as file:
            attr = datetime.today(), function_name, result
            line = "{}: function: {}, result:{}\n".format(*attr)
            file.write(line)
        return result

    return write_log


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
            file_name = datetime.today().strftime("%Y%m%d%H%M%S.7z")
        else:
            file_name = parse.unquote(content_disposition.split("filename=")[-1].strip("\""))
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


@log
def cmd_copy(file_path, dist_path):
    makedirs(dist_path) if path.exists(dist_path) is False else None
    command = "copy \"{}\" \"{}\"".format(file_path, dist_path)
    output = popen(command)
    out = output.read()
    return True if "copied" in out else out


class Run:

    def __init__(self):
        self.parse_critical()
        self.parse_all()

    @log
    def parse_all(self):
        auth = "iobit", "iobit#@6sample"
        date = date_download.strftime("%Y%m%d")
        file_name = "[infected]{}Snapshot-all.zip".format(date)
        file_path = r"G:\AutoSample\Snapshot\{}".format(file_name)
        url = "https://www.snapshot.clamav.net/daily/snapshot-all-{}.zip.001".format(date)
        download(auth=auth, url=url, file_path=file_path, verify=False)
        file_size = path.getsize(file_path) if path.exists(file_path) else 0
        cmd_copy(file_path, sm_dir) if file_size != 0 else remove(file_path)

    @log
    def parse_critical(self):
        auth = "iobit", "iobit#@6sample"
        date = date_download.strftime("%Y%m%d")
        file_name = "[infected]{}Snapshot-critical.zip".format(date)
        file_path = r"G:\AutoSample\Snapshot\{}".format(file_name)
        url = "https://www.snapshot.clamav.net/daily/snapshot-critical-{}.zip.001".format(date)
        download(auth=auth, url=url, file_path=file_path, verify=False)
        file_size = path.getsize(file_path) if path.exists(file_path) else 0
        cmd_copy(file_path, sm_dir) if file_size != 0 else remove(file_path)


if __name__ == "__main__":
    Run()
