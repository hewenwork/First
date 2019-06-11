import json
import os
import re
import datetime
import requests
from bs4 import BeautifulSoup
from subprocess import check_output, SubprocessError


class Base:

    def __init__(self):
        self.download_date = self.get_download_date()
        self.base_dir = r"C:\Users\hewen\Desktop\Download"
        self.download_folder = os.path.join(self.base_dir, self.download_date)
        self.download_log = os.path.join(self.base_dir, r"Log\{}.log".format(self.download_date))
        self.failed_log = os.path.join(self.base_dir, r"SHA256\{}.db".format(self.download_date))

    @staticmethod
    def get_download_date():
        today = datetime.datetime.today()
        time_interval = datetime.timedelta(days=1)
        download_day = today - time_interval
        return download_day.strftime("%Y-%m-%d")

    @staticmethod
    def write_sample(sample_path, sample_download_url, session):
        init_size = 0
        if os.path.exists(sample_path):
            print("\r{} download over".format(sample_download_url), end="")
            return True
        else:
            try:
                response = session.get(url=sample_download_url, stream=True)
                total_size = int(response.headers("content-length"))
                with open(sample_path, "wb")as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)
                        init_size += 1024
                        download_process = int(init_size/total_size*10)
                        print("\r{}".format(sample_download_url), "#"*download_process + "", end="")
                return True
            except requests.RequestException:
                return False

    def write_failed_sha256(self, md5):
        file_path = self.failed_log
        if os.path.exists(file_path):
            with open(file_path, "a+")as file:
                file.write(md5 + "\n")
        else:
            with open(file_path, "a+")as file:
                file.seek(0, 0)
                file.write(md5 + "\n")

    @staticmethod
    def write_download_log(log_path, result):
        if os.path.exists(log_path):
            with open(log_path, "r+")as file:
                old_data = file.read()
                file.seek(0, 0)
                file.write(result + "\n" + old_data)
        else:
            with open(log_path, "a+")as file:
                file.write(result + "\n")

    @staticmethod
    def start_info():
        sample_info = {}
        session = Base.get_session()
        download_folder = Base.get_download_folder()
        failed_path = Base.get_download_failed_path()
        log_path = Base.get_download_log_path()
        return sample_info, session, download_folder, failed_path, log_path

    @staticmethod
    def start_download(sample_info, session, target, download_folder, failed_path, log_path):
        failed_num = 0
        total_num = len(sample_info)
        if total_num is 0:
            result = "{}--has`t data".format(target)
        else:
            for file_name, download_url in sample_info.items():
                sample_md5 = file_name.split(".")[0]
                file_path = os.path.join(download_folder, file_name)
                download_result = Base.write_sample(file_path, download_url, session=session)
                if download_result is False:
                    failed_num += 1
                    Base.write_failed_sha256(file_path=failed_path, md5=sample_md5)
            result = "{0} -- Failed:{1}  Total:{2}".format(target, failed_num, total_num)
        Base.write_download_log(log_path, result)


class SampleHybrid:

    def __init__(self):
        self.session = self.get_login_session()
        sample_info = {}
        download_folder = Base().download_folder

    @staticmethod
    def get_login_session():
        headers = {"User-Agent":  "Falcon Sandbox"}
        session = requests.session()
        session.headers.update(headers)
        url = "https://www.hybrid-analysis.com/login"
        try:
            response = session.get(url)
            token = re.findall("name=\"token\" value=\"(.*?)\">", response.text)[0]
            data = {
                "email": "cicely@iobit.com",
                "password": "IObit2018",
                "token": token
            }
            session.post(url, data=data)
            return session
        except requests.RequestException:
            exit("Login Failed")

    def get_page_info(self, page):
        url = "https://www.hybrid-analysis.com/recent-submissions"
        params = {
            "filter": "file",
            "sort": "^timestamp",
            "page": page
        }
        page_dict = {}
        threat_level = ["malicious", "ambiguous", "suspicious", "-"]
        try:
            response = self.session.get(url, params=params)
            suop = BeautifulSoup(response.text, "lxml")
            sample_download_list = suop.select("a.btn.btn-default.btn-xs.pull-right.sampledl.download-url")
            is_virus_list = suop.select("dd:nth-of-type(3)")
            for sample_download_url, is_virus in zip(sample_download_list, is_virus_list):
                sample_sha256 = sample_download_url.get("href").split("?")[0][17:]
                file_name = sample_sha256 + ".gz"
                sample_download_url = "https://www.hybrid-analysis.com{}".format(sample_download_url.get("href"))
                is_virus = is_virus.getText().strip()
                if is_virus in threat_level:
                    page_dict[file_name] = sample_download_url
            return page_dict
        except requests.RequestException:
            return page_dict


# SampleHybrid()

# url = "https://www.hybrid-analysis.com/feed?json"
# headers = {"User-Agent": "Falcon Sandbox"}
# #
# a = requests.get(url, headers=headers).content
with open(r"C:\Users\hewen\Desktop\aa.txt", "r")as file:
    # file.write(a)
    text = file.read()
    # print(text)
aa = json.loads(text)
for i in aa["data"]:
    for j in i:
        print(j)
    break

# # print(a)
# apikey = "0ccgsgk0w00w4ogwcgk4o4s0ggw8gg4og04wsko8kw4s8wgocks400cgsg88400g"
# pwd = "606bb32347177d5fa05dec56f2e97329ce4f24fc535c4c77"