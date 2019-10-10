# encoding = utf-8
# @Author: Hewen
# @Time: 10/8/2019 2:36 PM
# @File: Final.py
import re
import os
import hashlib
import datetime
import requests
from faker import Faker
from functools import wraps
from bs4 import BeautifulSoup
from subprocess import check_output, SubprocessError


def log(func):
    @wraps(func)
    def derecoter(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            with open("Error.log", "a")as file:
                file.write(f"{datetime.datetime.now()}: {func.__name__}-->{e}\n")
        return func

    return derecoter


class Final:

    def __init__(self):
        self.switchVpn(switch="on")
        self.download_dir = r"G:\AutoCollect"
        self.date_today = datetime.datetime.now()
        self.download_date = (self.date_today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        self.date_dir = os.path.join(self.download_dir, self.download_date)
        if os.path.exists(self.date_dir) is False:
            os.makedirs(self.date_dir)
        self.md5_dir = os.path.join(self.download_dir, "MD5&SHA256")
        if os.path.exists(self.md5_dir) is False:
            os.makedirs(self.md5_dir)
        self.md5_path = os.path.join(self.md5_dir, f"{self.download_date}.log")
        self.session = requests.session()
        self.session.headers["User-Agent"] = Faker().user_agent()
        self.start_download()
        self.auto_deal()
        self.switchVpn(switch="off")

    def start_download(self):
        self.sample_vxvault()
        self.sample_malware()
        self.sample_virussin()
        self.sample_malshare()
        self.sample_infosec()
        self.sample_virusbay()

    def auto_deal(self):
        for file_name in os.listdir(self.date_dir):
            file_path = os.path.join(self.date_dir, file_name)
            if file_path[-3:] in ["rar", ".7z", "zip", ".gz"]:
                try:
                    self.de(file_path)
                except Exception as e:
                    with open("Error.log", "a")as file:
                        file.write(f"{datetime.datetime.now()}: {self.__name__}--> {e}\n")
                else:
                    os.remove(file_path)
        self.rename_file(self.date_dir)
        self.co(self.date_dir)
        result_path = f"{self.date_dir}[infected].rar"
        dist = r"\\192.168.1.39\f\Auto"
        os.system(f"copy {result_path} {dist}")

    def downlaod(self, session, sample_dict, auth=None):
        if sample_dict != {}:
            for file_name, download_url in sample_dict.items():
                file_path = os.path.join(self.date_dir, file_name)
                md5 = os.path.basename(file_path).split(".")[0]
                try:
                    sample_content = session.get(download_url, auth=auth).content
                except requests.exceptions:
                    os.remove(file_path)
                    with open(self.md5_path, "a+")as file:
                        file.write(f"{md5}\n")
                else:
                    with open(file_path, "wb")as file:
                        file.write(sample_content)

    @staticmethod
    def switchVpn(switch):
        if switch == "on":
            command = "rasdial US usa vpn2014"
        else:
            command = "rasdial US /DISCONNECT"
        try:
            check_output(command, shell=True)
        except SubprocessError:
            return

    @log
    def sample_vxvault(self):
        sample_dict = {}
        url = "http://vxvault.net/ViriList.php"
        suop = BeautifulSoup(self.session.get(url, timeout=8).text, "lxml")
        for link in suop.select("tr > td:nth-of-type(2) > a:nth-of-type(2)"):
            link = "http://vxvault.net/" + link.get("href")
            try:
                response = self.session.get(link)
            except requests.exceptions as e:
                with open("Error.log", "a")as file:
                    file.write(f"{datetime.datetime.now()}: {e}\n")
            else:
                download_url = re.findall("Link:</B> (.*?)<BR>", response.text)[0].replace("hxxp://", "http://")
                add_date = re.findall("Added:</B> (.*?)<BR>", response.text)[0]
                file_md5 = re.findall("MD5:</B> (.*?)<BR>", response.text)[0]
                file_name = file_md5 + ".vir"
                if self.download_date == add_date:
                    sample_dict[file_name] = download_url
                elif self.download_date > add_date:
                    break
        self.downlaod(self.session, sample_dict)

    @log
    def sample_malware(self):
        sample_dict = {}
        sample_date = self.download_date.replace("-", "/")
        target = f"http://www.malware-traffic-analysis.net/{sample_date}/index.html"
        if self.session.get(target).status_code == 200:
            sample_suop = BeautifulSoup(self.session.get(target).text, "lxml").select("ul > li > a")
            for download_url in sample_suop:
                if "-malware" in download_url.get("href"):
                    sample_name = download_url.get("href")
                    sample_download_url = target.replace("index.html", sample_name)
                    sample_dict[sample_name] = sample_download_url
        self.downlaod(self.session, sample_dict)

    @log
    def sample_virussin(self):
        sample_dict = {}
        auth = ("infected", "infected")
        url = "http://virusign.com/get_hashlist.php"
        params = {
            "sha256": "",
            "n": "ANY",
            "start_date": self.download_date,
            "end_date": self.download_date
        }
        response = self.session.get(url, params=params, timeout=30)
        if len(response.text) != 0:
            for sha256 in response.text.split("\n")[:-1]:
                sha256 = sha256.replace("\"", "")
                sample_name = sha256 + ".7z"
                sample_download_url = "http://virusign.com/file/%s" % sample_name
                sample_dict[sample_name] = sample_download_url
        self.downlaod(self.session, sample_dict, auth=auth)

    @log
    def sample_malshare(self):
        sample_dict = {}
        target = "https://malshare.com/api.php"
        # api_key = "1f36742f1f87e778ae1d4c370157581d746a4613fca10690f20949154b86589a"
        api_key = "2befc1c0b4d476b8527887f3f415648050638eff8dd400071f694e7356d5e49a"
        params = {
            "api_key": api_key,
            "action": "getlist"
        }
        response = self.session.get(target, params=params)
        for sample in response.json():
            sample_md5 = sample["md5"]
            file_name = sample_md5 + ".vir"
            download_url = target + "?api_key=%s&action=getfile&hash=%s" % (api_key, sample_md5)
            sample_dict[file_name] = download_url
        self.downlaod(self.session, sample_dict)

    @log
    def sample_infosec(self):
        sample_dict = {}
        shutdown = False
        for page in range(1, 10):
            base_url = f"https://infosec.cert-pa.it/analyze/submission-page-{page}.html"
            response = self.session.get(base_url)
            date_list = BeautifulSoup(response.text, "lxml").select("tr > td:nth-of-type(1)")
            md5_list = BeautifulSoup(response.text, "lxml").select("tr > td:nth-of-type(3)")
            for add_date, sample_md5 in zip(date_list, md5_list):
                add_date = add_date.getText()[:10]
                sample_md5 = sample_md5.getText()
                file_name = sample_md5 + ".vir"
                link = f"https://infosec.cert-pa.it/analyze/{sample_md5}.html"
                if add_date == self.download_date:
                    try:
                        response = self.session.get(link)
                        text = re.findall(">hXXp(.*?)<", response.text)[0]
                        download_url = f"http{text}".replace("[", "").replace("]", "")
                    except IndexError:
                        with open(self.md5_path, "a+")as file:
                            file.write(f"{sample_md5}\n")
                    else:
                        sample_dict[file_name] = download_url
                elif add_date < self.download_date:
                    shutdown = True
                    break
            if shutdown:
                break
        self.downlaod(self.session, sample_dict)

    @log
    def sample_virusbay(self):
        sample_dict = {}
        url = "https://beta.virusbay.io/login"
        data = {
            "email": "niwangxiu@gmail.com",
            "password": "testvirus0504L"
        }
        response = self.session.post(url=url, data=data)
        token = response.json()["token"]
        authorization = {"Authorization": "JWT %s" % token}
        self.session.headers.update(authorization)
        target = "https://beta.virusbay.io/sample/data"
        recent = self.session.get(url=target).json()["recent"]
        for info in recent:
            add_date = info["publishDate"][:10]
            _id = info["_id"]
            sample_md5 = info["md5"]
            file_name = sample_md5 + ".vir"
            link = f"https://beta.virusbay.io/api/sample/{_id}/download/link"
            sample_download_url = self.session.get(link).text
            if self.download_date == add_date:
                sample_dict[file_name] = sample_download_url
            elif self.download_date > add_date:
                break
        self.downlaod(requests.session(), sample_dict)

    @staticmethod
    @log
    def de(file_path):
        dir_path = os.path.dirname(file_path)
        command_dict = {
            "rar": f"rar e -pinfected -y \"{file_path}\" \"{dir_path}\"",
            "zip": f"7z e -tzip -pinfected -y \"{file_path}\" -o\"{dir_path}\"",
            ".gz": f"7z e -tgzip -pinfected -y \"{file_path}\" -o\"{dir_path}\"",
            ".7z": f"7z e -t7z -pinfected -y \"{file_path}\" -o\"{dir_path}\""
        }
        check_output(command_dict[file_path[-3:]], shell=True)

    @staticmethod
    @log
    def co(file_path):
        result_path = file_path + "[infected].rar"
        command = f"rar a -ep -pinfected -id[c,d,p,q] -y \"{result_path}\" \"{file_path}\""
        check_output(command, shell=True)

    @staticmethod
    @log
    def rename_file(folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, "rb")as file:
                    md5 = hashlib.md5(file.read()).hexdigest()
                file_path_new = os.path.join(folder_path, f"{md5}.vir")
                os.rename(file_path, file_path_new)
            except Exception as e:
                with open("Error.log", "a")as file:
                    file.write(f"{datetime.datetime.now()}: rename_file--> {e}\n")
                command = f"rar a -ep1 -df test.rar {file_path}"
                check_output(command, shell=True)
                os.remove("test.rar")


if __name__ == "__main__":
    Final()
