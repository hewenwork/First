# encoding = utf-8
# @Author: Hewen
# @Time:  4:32 PM
import os
import datetime
import requests
from faker import Faker
from functools import wraps
from bs4 import BeautifulSoup


class AutoDownload:

    def __new__(cls, *args, **kwargs):
        base_dir = r"G:\auto_collect"
        cls.download_date = cls.get_downlaod_date()
        cls.download_dir = os.path.join(base_dir, cls.download_date)
        if os.path.exists(cls.download_dir) is False:
            os.makedirs(cls.download_dir)
        cls.session = requests.session()
        cls.session.headers["User-Agent"] = Faker().user_agent()
        return object.__new__(cls)

    @staticmethod
    def download_failed(func):
        @wraps(func)
        def derater(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                with open("Error.log", "a+", encoding="UTF-8")as file:
                    file.write(f"{datetime.datetime.now()}:{e}\n")
                return func(*args, **kwargs)

        return derater

    @classmethod
    def get_downlaod_date(cls):
        data_today = datetime.datetime.today()
        data_interval = datetime.timedelta(days=1)
        download_date = (data_today - data_interval).strftime("%Y-%m-%d")
        return download_date

    @download_failed
    def downlaod(self, file_path, download_url, auth=None):
        content = self.session.get(download_url, auth=auth, timeout=20).content
        with open(file_path, "wb")as file:
            file.write(content)

    def __init__(self):
        self.sample_virusbay()
        self.sample_virussign()
        self.sample_malshare()
        self.sample_malware_traffic_analysis()

    def sample_virussign(self):
        sample_info = {}
        url = "http://virusign.com/get_hashlist.php"
        auth = ("infected", "infected")
        params = {
            "sha256": "",
            "n": "ANY",
            "start_date": self.download_date,
            "end_date": self.download_date
        }
        response = self.session.get(url, params=params, timeout=20)
        if len(response.text) != 0:
            for sha256 in response.text.split("\n")[:-1]:
                sha256 = sha256.replace("\"", "")
                sample_name = sha256 + ".7z"
                sample_download_url = "http://virusign.com/file/%s" % sample_name
                sample_info[sample_download_url] = sample_download_url
        print(len(sample_info))

    def sample_malware_traffic_analysis(self):
        sample_info = {}
        target = f"http://www.malware-traffic-analysis.net/{self.download_date}/index.html"
        if self.session.get(target).status_code == 200:
            sample_suop = BeautifulSoup(self.session.get(target).text, "lxml").select("ul > li > a")
            for download_url in sample_suop:
                if "-malware" in download_url.get("href"):
                    sample_name = download_url.get("href")
                    sample_download_url = target.replace("index.html", sample_name)
                    sample_info[sample_name] = sample_download_url
        print(len(sample_info))

    def sample_virusbay(self):
        sample_info = {}
        session = self.session
        url = "https://beta.virusbay.io/login"
        data = {
            "email": "niwangxiu@gmail.com",
            "password": "testvirus0504L"
        }
        response = session.post(url=url, data=data)
        token = response.json()["token"]
        authorization = {"Authorization": "JWT %s" % token}
        session.headers.update(authorization)
        url = "https://beta.virusbay.io/sample/data"
        recent = session.get(url).json()["recent"]
        for info in recent:
            add_date = info["publishDate"][:10]
            _id = info["_id"]
            sample_md5 = info["md5"]
            file_name = sample_md5 + ".vir"
            link = "https://beta.virusbay.io/api/sample/%s/download/link" % _id
            sample_download_url = self.session.get(link).text
            if self.download_date == add_date:
                sample_info[file_name] = sample_download_url
            elif self.download_date > add_date:
                break
        print(len(sample_info))

    def sample_malshare(self):
        sample_info = {}
        url = "https://malshare.com/api.php"
        api_key = "1f36742f1f87e778ae1d4c370157581d746a4613fca10690f20949154b86589a"
        params = {
            "api_key": api_key,
            "action": "getlist"
        }
        response = self.session.get(url, params=params)
        for sample in response.json():
            sample_md5 = sample["md5"]
            file_name = sample_md5 + ".vir"
            download_url = url + "?api_key=%s&action=getfile&hash=%s" % (api_key, sample_md5)
            sample_info[file_name] = download_url
        print(len(sample_info))

    def sample_urlhas(self):
        sample_info = {}
        download_dir = r""
        file_path = os.path.join(download_dir, f"urlhaus[infected]{self.download_date}.zip")
        download_url = f"https://urlhaus-api.abuse.ch/downloads/{self.download_date}.zip"
        sample_info[file_path] = download_url
        print(len(sample_info))


class AutoUpload:
    pass


class MakeSample:
    pass


class AutoGui:
    pass


if __name__ == "__main__":
    AutoDownload()
