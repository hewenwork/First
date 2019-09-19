import os
import re
import json
import asyncio
import aiohttp
import datetime
import requests
from faker import Faker
from bs4 import BeautifulSoup
from contextlib import closing
from subprocess import check_output, SubprocessError


class DownSpeed:

    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": Faker().user_agent()
    }

    def __init__(self, file_path, download_url, auth=None):
        file = open(file_path, "wb")
        response = requests.get(download_url, stream=True, headers=self.headers, auth=auth)
        if "Accept-Ranges" in response.headers.keys():
            self.async_downlaod(response, auth)
        else:
            self.alone(download_url, file)
        file.close()

    def async_downlaod(self, response, auth):
        aiohttp.BasicAuth = auth
        task = []
        total_size = int(response.headers["Content-Length"])
        chunk_size = 1024 * 1024
        chunk_num = int(total_size / chunk_size) + 1
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.get_total_size(chunk_num, chunk_size, total_size, task, loop))
        loop.close()

    async def get_total_size(self, chunk_num, chunk_size, total_size, task, loop):
        async with aiohttp.ClientSession() as session:
            start_size = 0
            for i in range(chunk_num):
                end_size = chunk_size + start_size
                if chunk_num - i == 1:
                    end_size = total_size
                task.append(loop.create_task(self._star(self.download_url, self.file, start_size, end_size, session)))
                start_size = end_size + 1
            await asyncio.wait(task)

    async def _star(self, download_url, file, start_size, end_size, session):
        self.headers["range"] = f"bytes={start_size}-{end_size}"
        async with session.get(download_url, headers=self.headers)as chunk:
            self.continue_download = False
            content = await chunk.read()
            file.seek(start_size, 0)
            file.write(content)
            file.flush()

    @staticmethod
    def alone(download_url, file):
        try:
            with requests.get(download_url).content as content:
                file.write(content)
        except Exception as e:
            print(e)


class Base:

    def __new__(cls, *args, **kwargs):
        cls.sample_dict = {}
        cls.config_file = "Auto.ini"
        if os.path.exists(cls.config_file):
            return object.__new__(cls)
        else:
            return

    def __init__(self, section):
        self.target = self.get_config(section, "url")
        if self.get_config(section, "download") == "yes":
            self.download_date = self.get_download_date()
            self.base_dir = self.get_base_dir()
            self.download_log = self.get_download_log_path()
            self.download_folder = self.get_download_folder()
            self.download_failed = self.get_download_failed_path()
            self.session = self.get_session()
            self.get_sample_dict()
            self.start_download()
        else:
            self.write_download_log(f"{self.target}:  设置不下载")
            return

    @staticmethod
    def write_error(func):
        def execute(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except requests.exceptions as e:
                with open("Error.log", "a+", encoding="UTF-8")as file:
                    file.write(f"{datetime.datetime.now()}:{e}")
            return func
        return execute()

    def write_log(self, result):
        error_data = f"{datetime.datetime.now()}: {self.target} {result}\n"
        with open("Error.log", "a+", encoding="UTF-8")as file:
            file.write(error_data)

    def switch_vpn(self, turn):
        print(f"Switch VPN {turn}")
        vpn_name = self.get_config("VPN", "name")
        vpn_user = self.get_config("VPN", "user")
        vpn_password = self.get_config("VPN", "password")
        command_dict = {
            "on": f"rasdial {vpn_name} {vpn_user} {vpn_password}",
            "off": f"rasdial {vpn_name} /DISCONNECT"
        }
        try:
            check_output(command_dict[turn], shell=True)
            return True
        except SubprocessError as e:
            self.write_log(e)

    def get_config(self, section, option):
        con = configparser.ConfigParser()
        try:
            con.read(self.config_file)
            result = con.get(section, option)
            return result
        except configparser.NoSectionError as e:
            self.write_log(e)
        except configparser.NoOptionError as e:
            self.write_log(e)

    def get_base_dir(self):
        base_dir = self.get_config("main", "dir")
        if os.path.exists(base_dir) is False:
            os.makedirs(base_dir)
        return base_dir

    def get_download_date(self):
        days = int(self.get_config("main", "days"))
        today = datetime.datetime.today()
        try:
            time_interval = datetime.timedelta(days=days)
            download_day = today - time_interval
            return download_day.strftime("%Y-%m-%d")
        except TypeError as e:
            self.write_log(e)

    def get_download_folder(self):
        download_folder = os.path.join(self.base_dir, self.download_date)
        if os.path.exists(download_folder) is False:
            os.makedirs(download_folder)
        return download_folder

    def get_download_failed_path(self):
        failed_dir = os.path.join(self.base_dir, r"MD5&SHA256")
        if os.path.exists(failed_dir) is False:
            os.makedirs(failed_dir)
        failed_path = os.path.join(failed_dir, f"Failed{self.download_date}.txt")
        return failed_path

    def get_download_log_path(self):
        log_dir = os.path.join(self.base_dir, r"Log")
        if os.path.exists(log_dir) is False:
            os.makedirs(log_dir)
        log_path = os.path.join(log_dir, f"{self.download_date}.log")
        return log_path

    def write_sample_md5(self, md5):
        if os.path.exists(self.download_failed):
            if len(md5) == 64:
                with open(self.download_failed, "a+")as file:
                    file.write(md5 + "\n")
            else:
                with open(self.download_failed, "r+")as file:
                    old_data = file.read()
                    file.seek(0, 0)
                    file.write(md5 + "\n" + old_data)
        else:
            with open(self.download_failed, "a+")as file:
                file.write(md5 + "\n")

    def write_download_log(self, result):
        with open(self.download_log, "a+")as file:
            file.write(f"{datetime.datetime.now()}: {result}\n")

    def get_session(self):
        headers = {"User-Agent": self.get_config("session", "useragent")}
        session = requests.session()
        session.headers.update(headers)
        return session

    def get_sample_dict(self):
        return

    def write_sample(self, sample_path, sample_download_url):
        if os.path.exists(sample_path) is False:
            try:
                with closing(self.session.get(url=sample_download_url, timeout=10))as response, \
                        open(sample_path, "wb")as file:
                    if response.status_code == 200:
                        file.write(response.content)
                        return True
                    else:
                        os.remove(sample_path)
                        self.write_log("No data")
                        return False
            except requests.RequestException as e:
                self.write_log(e)
                return False
            except OSError as e:
                self.write_log(e)
                return False
        else:
            return True

    async def start_download(self):
        failed_num = 0
        download_num = 0
        total_num = len(self.sample_dict)
        if total_num is 0:
            result = f"{self.target}--has`t data this time"
            self.write_download_log(result=result)
            return
        else:
            for file_name, download_url in self.sample_dict.items():
                file_md5 = os.path.splitext(file_name)[0]
                file_path = os.path.join(self.download_folder, file_name)
                download_result = self.write_sample(file_path, download_url)
                if download_result is False:
                    failed_num += 1
                    self.write_sample_md5(file_md5)
                download_num += 1
                print(f"\rDownload: {download_num} / {total_num}", end="")
            result = f"{self.target} -- Failed:{failed_num}  Total:{total_num}"
            self.write_download_log(result=result)


class SampleVxvault(Base):

    def __init__(self):
        super().__init__("target1")

    def get_sample_dict(self):
        target = "http://vxvault.net/ViriList.php"
        try:
            response = self.session.get(url=target)
            suop = BeautifulSoup(response.text, "lxml")
            suop_add_date = suop.select("tr > td:nth-of-type(1) > a")
            suop_url = suop.select("tr > td:nth-of-type(2) > a:nth-of-type(2)")
            for add_date, link in zip(suop_add_date, suop_url):
                add_date = add_date.getText()
                link = "http://vxvault.net/" + link.get("href")
                if add_date == self.download_date[-5:]:
                    file_name, download_url = self.get_sample_info(link)
                    self.sample_dict[file_name] = download_url
                elif add_date < self.download_date[-5:]:
                    break
        except requests.RequestException:
            self.write_download_log(result=target + "--" * 4 + "Connect Error")

    def get_sample_info(self, link):
        try:
            with closing(self.session.get(url=link))as response:
                sample_md5 = re.findall("MD5:</B> (.*?)<BR>", response.text)[0]
                file_name = sample_md5 + ".vir"
                sample_download_url = re.findall("Link:</B> (.*?)<BR>", response.text)[0].replace("hxxp:", "http:")
        except requests.RequestException as e:
            self.write_log(e)
            file_name, sample_download_url = None, None
        return file_name, sample_download_url


class SampleMalc0de(Base):

    def __init__(self):
        super().__init__("target2")

    def get_sample_dict(self):
        target = "http://malc0de.com/database/"
        self.switch_vpn("on")
        try:
            with closing(self.session.get(target, timeout=10))as response:
                suop = BeautifulSoup(response.text, "lxml")
                sample_data_list = suop.select("tr > td:nth-of-type(1)")
                sample_url_list = suop.select("tr > td:nth-of-type(2)")
                sample_md5_list = suop.select("tr > td:nth-of-type(7)")
                for sample_date, sample_url, sample_md5 in zip(sample_data_list, sample_url_list, sample_md5_list):
                    add_date = sample_date.getText()
                    sample_md5 = sample_md5.getText()
                    file_name = sample_md5 + ".vir"
                    sample_url = "http://" + sample_url.getText()
                    if add_date == self.download_date:
                        self.sample_dict[file_name] = sample_url
        except requests.RequestException as e:
            self.write_log(e)
        self.switch_vpn("off")


class SampleMalwareTrafficAnalysis(Base):

    def __init__(self):
        super().__init__("target3")

    def get_sample_dict(self):
        download_date = self.download_date.replace("-", "/")
        target = f"http://www.malware-traffic-analysis.net/{download_date}/index.html"
        if self.session.get(target).status_code == 200:
            sample_suop = BeautifulSoup(self.session.get(target).text, "lxml").select("ul > li > a")
            for download_url in sample_suop:
                if "-malware" in download_url.get("href"):
                    sample_name = download_url.get("href")
                    sample_download_url = target.replace("index.html", sample_name)
                    self.sample_dict[sample_name] = sample_download_url


class SampleVirusBay(Base):

    def __init__(self):
        super().__init__("target4")

    def get_sample_dict(self):
        target = "https://beta.virusbay.io/sample/data"
        old_session = self.session
        self.session = self.get_login_session()
        recent = self.session.get(url=target).json()["recent"]
        for info in recent:
            add_date = info["publishDate"][:10]
            _id = info["_id"]
            sample_md5 = info["md5"]
            file_name = sample_md5 + ".vir"
            link = "https://beta.virusbay.io/api/sample/%s/download/link" % _id
            sample_download_url = self.session.get(link).text
            if self.download_date == add_date:
                self.sample_dict[file_name] = sample_download_url
            elif self.download_date > add_date:
                break
        self.session = old_session

    def get_login_session(self):
        url = "https://beta.virusbay.io/login"
        data = {
            "email": self.get_config("target4", "user"),
            "password": self.get_config("target4", "password")
        }
        try:
            response = self.session.post(url=url, data=data)
            token = response.json()["token"]
            authorization = {"Authorization": "JWT %s" % token}
            self.session.headers.update(authorization)
            return self.session
        except requests.RequestException as e:
            self.write_log(e)


class SampleHybrid(Base):

    def __init__(self):
        super().__init__("target5")
        self.session = self.get_login_session()
        self.threat_level = ["malicious", "ambiguous", "suspicious", "-"]

    def get_sample_dict(self):
        # self.get_last_info()
        self.get_page_info()

    def get_login_session(self):
        self.session.headers["User-Agent"] = "Falcon Sandbox"
        url = "https://www.hybrid-analysis.com/login"
        try:
            response = self.session.get(url)
            token = re.findall("name=\"token\" value=\"(.*?)\">", response.text)[0]
            data = {
                "email": self.get_config("target5", "user"),
                "password": self.get_config("target5", "password"),
                "token": token
            }
            if self.session.post(url, data=data).status_code == 200:
                return self.session
            else:
                self.write_log("Login Failed")
        except requests.RequestException as e:
            self.write_log(e)
            return

    def get_last_info(self):
        url = "https://www.hybrid-analysis.com/feed?json"
        try:
            base_url = "https://www.hybrid-analysis.com/download-sample/"
            json_content = self.session.get(url).json()
            for data_type in json_content["data"]:
                file_name = data_type["md5"] + ".gz"
                sha256 = data_type["sha256"]
                environmentId = data_type["environmentId"]
                threatlevel = data_type["threatlevel"]
                if threatlevel != 0:
                    download_url = f"{base_url}{sha256}?environmentId={environmentId}"
                    self.sample_dict[file_name] = download_url
        except requests.RequestException as e:
            self.write_log(e)
        except KeyError as e:
            self.write_log(e)

    def get_page_info(self):
        for page in range(11):
            self.get_page(page)

    def get_page(self, page):
        url = "https://www.hybrid-analysis.com/recent-submissions"
        params = {
            "filter": "file",
            "sort": "^timestamp",
            "page": page
        }
        try:
            with closing(self.session.get(url, params=params))as response:
                suop = BeautifulSoup(response.text, "lxml")
                sample_list = suop.select("div.submissions-table-container > table > tbody > tr")
                for sample_tr in sample_list:
                    sample_threat_level = sample_tr.select("td.hidden-xl.wraparound > dl > dd:nth-child(6)")[
                        0].getText().strip()
                    sample_download_url_list = sample_tr.select("td.hidden-xl.wraparound > dl > dd:nth-child(4) > a")
                    sample_md5 = sample_tr.select(
                        "td.hidden-xl.wraparound > dl > dd:nth-child(4) > span[class=\"lowprio compact\"]")[
                        0].getText().strip()
                    if len(sample_download_url_list) != 0 and sample_threat_level in self.threat_level:
                        sample_download_url = sample_download_url_list[0].get("href").strip()
                        file_name = f"{sample_md5}.gz"
                        self.sample_dict[file_name] = sample_download_url
        except requests.RequestException as e:
            self.write_log(e)


class SampleVirusSign(Base):

    def __init__(self):
        super().__init__("target6")

    def get_sample_dict(self):
        target = "http://virusign.com/get_hashlist.php"
        self.session.auth = ("infected", "infected")
        params = {
            "sha256": "",
            "n": "ANY",
            "start_date": self.download_date,
            "end_date": self.download_date
        }
        response = self.session.get(target, params=params).text
        if response is not "":
            for sha256 in response.split("\n")[:-1]:
                sha256 = sha256.replace("\"", "")
                file_name = sha256 + ".7z"
                sample_download_url = "http://virusign.com/file/%s" % file_name
                self.sample_dict[file_name] = sample_download_url


class SampleMalshare(Base):

    def __init__(self):
        super().__init__("target7")

    def get_sample_dict(self):
        target = "https://malshare.com/api.php"
        api_key = "1f36742f1f87e778ae1d4c370157581d746a4613fca10690f20949154b86589a"
        params = {
            "api_key": api_key,
            "action": "getlist"
        }
        try:
            with closing(self.session.get(url=target, params=params))as response:
                for sample in response.json():
                    sample_md5 = sample["md5"]
                    file_name = sample_md5 + ".vir"
                    download_url = target + "?api_key=%s&action=getfile&hash=%s" % (api_key, sample_md5)
                    self.sample_dict[file_name] = download_url
        except requests.RequestException as e:
            self.write_log(e)
        except json.decoder.JSONDecodeError as e:
            self.write_log(e)


class SampleInfosec(Base):

    def __init__(self):
        super().__init__("target8")

    def get_sample_dict(self, _page=1):
        while _page > 0 or _page < 10:
            base_url = f"https://infosec.cert-pa.it/analyze/submission-page-{_page}.html"
            _page += 1
            try:
                with closing(self.session.get(base_url))as response:
                    date_list = BeautifulSoup(response.text, "lxml").select("tr > td:nth-of-type(1)")
                    md5_list = BeautifulSoup(response.text, "lxml").select("tr > td:nth-of-type(3)")
                    for add_date, sample_md5 in zip(date_list, md5_list):
                        add_date = add_date.getText()[:10]
                        sample_md5 = sample_md5.getText()
                        file_name = sample_md5 + ".vir"
                        link = f"https://infosec.cert-pa.it/analyze/{sample_md5}.html"
                        if add_date == self.download_date:
                            download_url = self.get_download_link(link)
                            self.sample_dict[file_name] = download_url
                        elif add_date < self.download_date:
                            _page = 0
            except requests.RequestException as e:
                self.write_log(e)

    def get_download_link(self, link):
        try:
            with closing(self.session.get(link))as response:
                text = re.findall(">hXXp(.*?)<", response.text)[0]
                download_url = f"http{text}".replace("[", "").replace("]", "")
            return download_url
        except IndexError as e:
            self.write_log(e)
            return
        except requests.RequestException as e:
            self.write_log(e)
            return


class Compression(Base):

    def __init__(self):
        super().__init__(self)
        self.path_7z = self.get_config("7-zip", "path")
        self.path_rar = self.get_config("winrar", "path")
        self.password = self.get_config("main", "password")
        self.failed_folder = self.get_failed_folder()

    def get_failed_folder(self):
        failed_folder = os.path.join(self.base_dir, "Failed")
        if os.path.exists(failed_folder) is False:
            os.makedirs(failed_folder)
        return failed_folder

    def de(self, file_path):
        dir_path = os.path.dirname(file_path)
        command_dict = {
            "rar": {
                "path": self.path_rar,
                "command": f"rar e -p{self.password} \"{file_path}\" \"{dir_path}\" -y"},
            "zip": {
                "path": self.path_7z,
                "command": f"7z e -tzip -p{self.password} \"{file_path}\" -o\"{dir_path}\" -y"},
            ".gz": {
                "path": self.path_7z,
                "command": f"7z e -tgzip -p{self.password} \"{file_path}\" -o\"{dir_path}\" -y"},
            ".7z": {
                "path": self.path_7z,
                "command": f"7z e -t7z -p{self.password} \"{file_path}\" -o\"{dir_path}\" -y"}
        }
        try:
            os.chdir(command_dict[file_path[-3:]]["path"])
            check_output(command_dict[file_path[-3:]]["command"], shell=True)
            os.remove(file_path)
            return True
        except SubprocessError as e:
            print(e)
        except KeyError:
            pass

    def co(self, file_path, password="infected"):
        os.chdir(self.path_rar)
        result_path = file_path + "[infected].rar"
        command = f"rar a -ep -p{password} \"{result_path}\" \"{file_path}\""
        try:
            check_output(command, shell=True)
            return result_path
        except SubprocessError as e:
            print(e)
            return False

    def auto(self, folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            self.de(file_path)


if __name__ == "__main__":
    pass
    # with closing(asyncio.get_event_loop())as loop:
    #     tasks = [SampleInfosec().start_download(), SampleHybrid.start_download()]
    #     loop.run_until_complete(asyncio.wait(tasks))
