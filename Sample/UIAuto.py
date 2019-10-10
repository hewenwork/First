# encoding = utf-8
# @Author: Hewen
# @Time: 10/8/2019 11:14 AM
# @File: UIAuto.py

import os
import re
import datetime
import asyncio
import aiohttp
import requests
from faker import Faker
from bs4 import BeautifulSoup
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar

session = requests.session()
UserAgent = Faker().user_agent()
session.headers["User-Agent"] = UserAgent
date_today = datetime.datetime.today()
date_interval = datetime.timedelta(days=1)
download_date = (date_today - date_interval).strftime("%Y-%m-%d")
download_dir = os.path.join(r"G:\auto_collect", date_today.strftime("%Y-%m-%d"))
if os.path.exists(download_dir) is False:
    os.makedirs(download_dir)


class DownSpeed:
    headers = session.headers

    def __init__(self, file_name, download_url, auth=None):
        self.file_path = os.path.join(download_dir, file_name)
        self.download_url = download_url
        self.file_md5 = file_name[:-3]
        self.file = open(self.file_path, "wb")
        # response = session.get(download_url, stream=True, auth=auth)
        # if "Accept-Ranges" in response.headers.keys():
        #     self.async_downlaod(response, auth)
        # else:
        #     self.alone(download_url, self.file)
        self.alone(auth)


    def async_downlaod(self, response, auth):
        aiohttp.BasicAuth = auth
        task = []
        total_size = int(response.headers["Content-Length"])
        chunk_size = 1024 * 8
        chunk_num = int(total_size / chunk_size) + 1
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.get_total_size(chunk_num, chunk_size, total_size, task, loop))
        loop.close()

    async def get_total_size(self, chunk_num, chunk_size, total_size, task, loop):
        async with aiohttp.ClientSession() as aiosession:
            start_size = 0
            for i in range(chunk_num):
                end_size = chunk_size + start_size
                if chunk_num - i == 1:
                    end_size = total_size
                task.append(
                    loop.create_task(self._star(self.download_url, self.file, start_size, end_size, aiosession)))
                start_size = end_size + 1
                await asyncio.wait(task)

    async def _star(self, download_url, file, start_size, end_size, aiosession):
        self.headers["range"] = f"bytes={start_size}-{end_size}"
        async with aiosession.get(download_url, headers=self.headers)as chunk:
            self.continue_download = False
            content = await chunk.read()
            file.seek(start_size, 0)
            file.write(content)
            file.flush()

    def alone(self, auth):
        try:
            respone = session.get(self.download_url, auth=auth)
            if respone.status_code == 200:
                self.file.write(respone.content)
            self.file.close()
        except Exception:
            with open(r"G:\auto_collect\MD5&SHA256\%s" % date_today, "a+")as file:
                file.write(f"self.file_md5\n")
            os.remove(self.file_path)


class UICollect(GridLayout):

    def __init__(self):
        super().__init__()
        self.cols = 3
        self.label = Label()
        self.add_widget(self.label)


class UIAuto(GridLayout):

    def __init__(self):
        super().__init__()
        self.cols = 1
        self.add_widget(UICollect())

        # self.label = Label()
        # self.button = Button()
        # self.progressbar = ProgressBar()
        # self.add_widget(self.addlabel())
        # self.add_widget(self.addprogress())
        # self.add_widget(self.addbutton())

    def sample_malware(self):
        sample_dict = {}
        sample_date = download_date.replace("-", "/")
        target = f"http://www.malware-traffic-analysis.net/{sample_date}/index.html"
        if session.get(target).status_code == 200:
            sample_suop = BeautifulSoup(session.get(target).text, "lxml").select("ul > li > a")
            for download_url in sample_suop:
                if "-malware" in download_url.get("href"):
                    sample_name = download_url.get("href")
                    sample_download_url = target.replace("index.html", sample_name)
                    sample_dict[sample_name] = sample_download_url
        if len(sample_dict) != {}:
            for key, value in sample_dict.items():
                DownSpeed(key, value)

    def sample_virussin(self):
        sample_dict = {}
        auth = ("infected", "infected")
        url = "http://virusign.com/get_hashlist.php"
        params = {
            "sha256": "",
            "n": "ANY",
            "start_date": download_date,
            "end_date": download_date
        }
        response = session.get(url, params=params, timeout=30)
        if len(response.text) != 0:
            for sha256 in response.text.split("\n")[:-1]:
                sha256 = sha256.replace("\"", "")
                sample_name = sha256 + ".7z"
                sample_download_url = "http://virusign.com/file/%s" % sample_name
                sample_dict[sample_name] = sample_download_url
        if len(sample_dict) != {}:
            for key, value in sample_dict.items():
                DownSpeed(key, value, auth=auth)

    def sample_malshare(self):
        sample_dict = {}
        target = "https://malshare.com/api.php"
        api_key = "1f36742f1f87e778ae1d4c370157581d746a4613fca10690f20949154b86589a"
        params = {
            "api_key": api_key,
            "action": "getlist"
        }
        response = session.get(target, params=params)
        for sample in response.json():
            sample_md5 = sample["md5"]
            file_name = sample_md5 + ".vir"
            download_url = target + "?api_key=%s&action=getfile&hash=%s" % (api_key, sample_md5)
            sample_dict[file_name] = download_url
        if len(sample_dict) != {}:
            for key, value in sample_dict.items():
                DownSpeed(key, value)

    def sample_infosec(self):
        sample_dict = {}
        page = 1
        while page < 10:
            base_url = f"https://infosec.cert-pa.it/analyze/submission-page-{page}.html"
            page += 1
            response = session.get(base_url)
            date_list = BeautifulSoup(response.text, "lxml").select("tr > td:nth-of-type(1)")
            md5_list = BeautifulSoup(response.text, "lxml").select("tr > td:nth-of-type(3)")
            for add_date, sample_md5 in zip(date_list, md5_list):
                add_date = add_date.getText()[:10]
                sample_md5 = sample_md5.getText()
                file_name = sample_md5 + ".vir"
                link = f"https://infosec.cert-pa.it/analyze/{sample_md5}.html"
                if add_date == download_date:
                    try:
                        response = session.get(link)
                        text = re.findall(">hXXp(.*?)<", response.text)[0]
                        download_url = f"http{text}".replace("[", "").replace("]", "")
                        sample_dict[file_name] = download_url
                    except Exception as e:
                        print(e)
                elif add_date < download_date:
                    page = 100
        if len(sample_dict) != {}:
            for key, value in sample_dict.items():
                DownSpeed(key, value)

    def sample_virusbay(self):
        sample_dict = {}
        url = "https://beta.virusbay.io/login"
        data = {
            "email": "niwangxiu@gmail.com",
            "password": "testvirus0504L"
        }
        try:
            response = session.post(url=url, data=data)
            token = response.json()["token"]
            authorization = {"Authorization": "JWT %s" % token}
            session.headers.update(authorization)
            target = "https://beta.virusbay.io/sample/data"
            recent = session.get(url=target).json()["recent"]
            for info in recent:
                add_date = info["publishDate"][:10]
                _id = info["_id"]
                sample_md5 = info["md5"]
                file_name = sample_md5 + ".vir"
                link = "https://beta.virusbay.io/api/sample/%s/download/link" % _id
                sample_download_url = session.get(link).text
                if download_date == add_date:
                    sample_dict[file_name] = sample_download_url
                elif download_date > add_date:
                    break
        except Exception as e:
            print(e)
        if len(sample_dict) != {}:
            for key, value in sample_dict.items():
                DownSpeed(key, value)

if __name__ == "__main__":
    UIAuto()
