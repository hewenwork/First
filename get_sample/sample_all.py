import datetime
import os
import re
from contextlib import *

import Django as Django
import requests
from bs4 import BeautifulSoup


class get_all_sample():

    def __init__(self):
        today = datetime.datetime.today()
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        self.yestoday_string = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        self.download_folder = r"C:\Users\hewen\Desktop\%s" % self.yestoday_string
        if os.path.exists(self.download_folder)==False:
            os.makedirs(self.download_folder)
        self.session = requests.session()
        self.session.headers.update(headers)

    def write_sample(self, sample_name, sample_download_url, auth=None):
        file_download_path = os.path.join(self.download_folder, sample_name)
        if os.path.exists(file_download_path)==False:
            try:
                # respone = self.session.get(sample_download_url, stream=True)
                # with open(file_download_path, "wb")as file:
                #     file.write(respone.content)
                with closing(self.session.get(sample_download_url, stream=True, auth=auth)) as response:
                    chunk_size = 1024  # 单次请求最大值
                    content_size = int(response.headers['content-length'])  # 内容体总大小
                    data_count = 0
                    with open(file_download_path, "wb") as file:
                        for data in response.iter_content(chunk_size=chunk_size):
                            file.write(data)
                            data_count = data_count + len(data)
                            now_jd = (data_count / content_size) * 100
                            print("\r 文件下载进度：%d%%(%d/%d) - %s" % (now_jd, data_count, content_size, file_download_path), end="")


            except:
                print("error")

    def get_sample_from_vxvault(self):
        star_url = "http://vxvault.net/ViriList.php"
        suop = BeautifulSoup(self.session.get(star_url).text, "lxml").select("tr > td:nth-of-type(2) > a:nth-of-type(2)")
        for sample_info in suop:
            sample_info = "http://vxvault.net/%s" % sample_info.get("href")
            respone = self.session.get(sample_info).text
            sample_name = re.findall("MD5:<\/B> (.*?)<BR>", respone)[0]
            sample_add_date = re.findall("Added:<\/B> (.*?)<BR>", respone)[0]
            sample_download_url = re.findall("Link:<\/B> (.*?)<BR>", respone)[0].replace("hxxp:", "http:")
            if sample_add_date == self.yestoday_string:
                # print(sample_add_date, sample_name, sample_download_url)
                self.write_sample(sample_name,sample_download_url)
            elif sample_add_date < self.yestoday_string:
                break

    def get_sample_from_malware_traffic_analysis(self):
        url = "http://www.malware-traffic-analysis.net/%s/index.html" % self.yestoday_string.replace("-", "/")
        sample_info = self.session.get(url)
        if sample_info.status_code == 200:
            sample_suop = BeautifulSoup(self.session.get(url).text, "lxml").select("ul > li > a")
            for download_url in sample_suop:
                if "-malware" in download_url.get("href"):
                    final_download_url = url.replace("index.html", download_url.get("href"))
                    self.write_sample(download_url.get("href"), final_download_url)

    def get_sample_from_malc0de(self):
        url = "http://malc0de.com/database/"
        respone = self.session.get(url)
        suop = BeautifulSoup(respone.text, "lxml")
        sample_data_list = suop.select("tr > td:nth-of-type(1)")
        sample_url_list = suop.select("tr > td:nth-of-type(2)")
        sample_md5_list = suop.select("tr > td:nth-of-type(7)")
        for sample_data, sample_url, sample_md5 in zip(sample_data_list, sample_url_list, sample_md5_list):
            sample_data = sample_data.getText()
            sample_url = "http://" + sample_url.getText()
            sample_name = sample_md5.getText().upper()
            if sample_data == self.yestoday_string:
                print(sample_name, sample_url)
                self.write_sample(sample_name, sample_url)

    def get_sample_from_virusbay(self):
        # session = requests.session()
        # session.headers.update(
        #     {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        # )
        # url = "https://beta.virusbay.io/login"
        # data = {
        #     "email": "niwangxiu@gmail.com",
        #     "password": "testvirus0504L"
        # }
        # respone = session.post(url, data=data)
        # token = respone.json()["token"]
        # session.headers.update({"Authorization": "JWT %s" % token})
        session = self.get_login_seesion(target="virusbay")
        url = "https://beta.virusbay.io/sample/data"
        respone = session.get(url).json()
        recent = respone["recent"]
        for info in recent:
            publishDate = info["publishDate"][:10]
            _id = info["_id"]
            sample_name = info["md5"].upper()
            url = "https://beta.virusbay.io/api/sample/%s/download/link" % _id
            sample_download_url = session.get(url).text
            if publishDate == self.yestoday_string:
                self.write_sample(sample_name,sample_download_url)
            elif publishDate < self.yestoday_string:
                break

    def get_sample_from_hybird(self):
        # url = "https://www.hybrid-analysis.com/login"
        # session = requests.session()
        # headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        # }
        # session.headers.update(headers)
        # respone = session.get(url)
        # token = re.findall("name=\"token\" value=\"(.*?)\">", respone.text)[0]
        # data = {
        #     "email": "cicely@iobit.com",
        #     "password": "IObit2018",
        #     "token": token
        # }
        # session.post(url, data=data)
        session = self.get_login_seesion(target="hybrid")
        for num in range(1, 11):
            url = "https://www.hybrid-analysis.com/recent-submissions?filter=file&sort=^timestamp&page=%.f" % num
            respone = session.get(url)
            suop = BeautifulSoup(respone.text, "lxml")
            sample_data_list = suop.select("td.submission-timestamp.hidden-xs")
            sample_download_list = suop.select("a.btn.btn-default.btn-xs.pull-right.sampledl.download-url")
            is_virus_list = suop.select("dd:nth-of-type(3)")
            for sample_data, sample_download_url, is_virus in zip(sample_data_list, sample_download_list, is_virus_list):
                sample_data = sample_data.getText().strip().split(",")[0]
                sample_data = str(datetime.datetime.strptime(sample_data, "%B %d %Y").date())
                sample_download_url = "https://www.hybrid-analysis.com%s" % sample_download_url.get("href")
                is_virus = is_virus.getText().strip()
                file_name = sample_download_url[48:112] + ".vir.gz"
                print(file_name)

    def get_login_seesion(self, target):
        session = requests.session()
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        session.headers.update(headers)
        if target == "virusbay":
            url = "https://beta.virusbay.io/login"
            data = {
                "email": "niwangxiu@gmail.com",
                "password": "testvirus0504L"
            }
            respone = session.post(url, data=data)
            token = respone.json()["token"]
            session.headers.update({"Authorization": "JWT %s" % token})
            return session
        elif target == "hybrid":
            url = "https://www.hybrid-analysis.com/login"
            respone = session.get(url)
            token = re.findall("name=\"token\" value=\"(.*?)\">", respone.text)[0]
            data = {
                "email": "cicely@iobit.com",
                "password": "IObit2018",
                "token": token
            }
            session.post(url, data=data)
            return session

    def get_samole_form_virusign(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Authorization": "Basic aW5mZWN0ZWQ6aW5mZWN0ZWQ="
        }
        for d in range(5):
            p = 1
            while p != -1:
                url = "http://virusign.com/home.php?d=%d&r=100&c=hashes&o=date&s=DESC&n=EXACT&p=%s" % (d, p)
                p += 1
                respone = requests.get(url=url, headers=headers)
                suop = BeautifulSoup(respone.text, "lxml")
                date_list = suop.select("tr > td:nth-of-type(2)")
                sha256_list = suop.select("tr > td:nth-of-type(4)")
                for date, sha256 in zip(date_list, sha256_list):
                    date = date.getText()
                    sha256 = sha256.getText().split(" ")[-1]
                    download_url = "http://virusign.com/file/%s.7z" % sha256
                    if date == self.yestoday_string:
                        print(date, sha256)

                    elif date < self.yestoday_string:
                        p = -1
# get_all_sample().get_sample_from_malware_traffic_analysis()
# get_all_sample().get_sample_from_vxvault()
# get_all_sample().get_sample_from_malc0de()
# get_all_sample().get_sample_from_virusbay()
# get_all_sample().get_sample_from_hybird()
get_all_sample().get_samole_form_virusign()

Django