# encoding = utf-8
import os
import re
import json
import time
import aiohttp
import asyncio
import datetime
import requests
from faker import Faker
from functools import wraps
from bs4 import BeautifulSoup
from contextlib import closing
from subprocess import check_output, SubprocessError

base_dir = r"G:\auto_collect"
session = requests.session()
UserAgent = Faker().user_agent()
session.headers["User-Agent"] = UserAgent


def log(func):

    @wraps(func)
    def derater(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            with open("Error.log", "a+", encoding="UTF-8")as file:
                file.write(f"{datetime.datetime.now()}:{e}\n")
            return func(*args, **kwargs)

    return derater


class DownUp:
    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": UserAgent
    }

    def __init__(self, download_url, file_path, auth=None):
        print(auth)
        self.file = open(file_path, "wb")
        response = requests.get(download_url, stream=True, headers=self.headers, auth=auth)
        if "Accept-Ranges" in response.headers.keys():
            aiohttp.BasicAuth = auth
            self.task = []
            self.total_size = int(response.headers["Content-Length"])
            self.chunk_size = 1024 * 1024
            self.chunk_num = int(self.total_size / self.chunk_size) + 1
            self.loop = asyncio.get_event_loop()
            self.loop.run_until_complete(self.get_total_size(download_url))
            self.loop.close()
        else:
            self.alone(download_url, auth)
        self.file.close()

    async def get_total_size(self, download_url):
        async with aiohttp.ClientSession() as asysession:
            start_size = 0
            for i in range(self.chunk_num):
                end_size = self.chunk_size + start_size
                if self.chunk_num - i == 1:
                    end_size = self.total_size
                self.task.append(self.loop.create_task(self._star(download_url, start_size, end_size, asysession)))
                start_size = end_size + 1
            await asyncio.wait(self.task)

    async def _star(self, download_url, start_size, end_size, session):
        self.headers["range"] = f"bytes={start_size}-{end_size}"
        async with session.get(download_url, headers=self.headers)as chunk:
            self.continue_download = False
            content = await chunk.read()
            self.file.seek(start_size, 0)
            self.file.write(content)
            self.file.flush()

    def alone(self, download_url, auth):
        try:

            self.file.write(session.get(download_url, auth=auth).content)
        except Exception as e:
            print(e, "aaa")


class Download:

    def __init__(self, auth=None):

        self.sample_dict = {}
        self.download_sample(auth=auth)

    @staticmethod
    def get_download_date():
        data_today = datetime.datetime.today()
        data_interval = datetime.timedelta(days=1)
        download_date = (data_today - data_interval).strftime("%Y-%m-%d")
        return download_date

    def get_sample_dict(self):
        target_url = "http://www.malware-traffic-analysis.net/2019/09/13/index.html"
        with closing(session.get(target_url))as response:
            if response.status_code is 200:
                return self.sample_dict
            else:
                return False

    def download_sample(self, auth=None):
        download_dir = os.path.join(base_dir, self.get_download_date())
        if os.path.exists(download_dir) is False:
            os.makedirs(download_dir)
        download_dict = self.get_sample_dict()
        if download_dict:
            for file_name, download_url in download_dict.items():
                file_path = os.path.join(download_dir, file_name)
                DownUp(download_url, file_path, auth=auth)


class Compression:

    @staticmethod
    def de(file_path):
        dir_path = os.path.dirname(file_path)
        command_dict = {
            "rar": f"rar e -pinfected -y \"{file_path}\" \"{dir_path}\"",
            "zip": f"7z e -tzip -pinfected -y \"{file_path}\" -o\"{dir_path}\"",
            ".gz": f"7z e -tgzip -pinfected -y \"{file_path}\" -o\"{dir_path}\"",
            ".7z": f"7z e -t7z -pinfected -y \"{file_path}\" -o\"{dir_path}\""
        }
        try:
            check_output(command_dict[file_path[-3:]], shell=True)
            return True
        except Exception as e:
            print(e)

    @staticmethod
    def co(file_path):
        result_path = file_path + "[infected].rar"
        command = f"rar a -ep -pinfected -id[c,d,p,q] -y \"{result_path}\" \"{file_path}\""
        try:
            check_output(command, shell=True)
            return result_path
        except SubprocessError as e:
            print(e)
            return False


class SampleMalwareTrafficAnalysis(Download):

    def get_sample_dict(self):
        download_date = self.get_download_date().replace("-", "/")
        target = f"http://www.malware-traffic-analysis.net/{download_date}/index.html"
        if session.get(target).status_code == 200:
            sample_suop = BeautifulSoup(session.get(target).text, "lxml").select("ul > li > a")
            for download_url in sample_suop:
                if "-malware" in download_url.get("href"):
                    sample_name = download_url.get("href")
                    sample_download_url = target.replace("index.html", sample_name)
                    self.sample_dict[sample_name] = sample_download_url
        return self.sample_dict


class VirusSign(Download):

    def __init__(self):
        auth = ("infected", "infected")
        super().__init__(auth=auth)

    def get_sample_dict(self):
        url = "http://virusign.com/get_hashlist.php"
        params = {
            "sha256": "",
            "n": "ANY",
            "start_date": self.get_download_date(),
            "end_date": self.get_download_date()
        }
        with closing(session.get(url, params=params, timeout=30))as response:
            if len(response.text) != 0:
                for sha256 in response.text.split("\n")[:-1]:
                    sha256 = sha256.replace("\"", "")
                    sample_name = sha256 + ".7z"
                    sample_download_url = "http://virusign.com/file/%s" % sample_name
                    self.sample_dict[sample_name] = sample_download_url
        return self.sample_dict



if __name__ == "__main__":
    VirusSign()
