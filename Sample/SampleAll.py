# encoding = utf-8
# @Author: Hewen
# @Time: 1/20/2020 11:13 AM
# @File: SampleAll.py
import os
import re
import hashlib
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from subprocess import check_output, CalledProcessError

download_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
smart_dir = r"G:\Auto"  # 转移到smartccl位置
log_dir = os.path.join(r"G:\AutoCollect", "log")  # 存放MD5和SSD
sample_dir = os.path.join(r"G:\AutoCollect", download_date)  # 存放Sample
smart_log = r"\\192.168.1.39\e\VTSpider\MD5SHA256"  # 转移到39位置
log_path = os.path.join(log_dir, "download_log")  # 存放下载日志

if os.path.exists(sample_dir) is False:
    os.makedirs(sample_dir)

if os.path.exists(log_dir) is False:
    os.makedirs(log_dir)

if os.path.exists(log_path) is False:
    os.makedirs(log_path)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/78.0.3904.108 Safari/537.36",
}
session = requests.session()
session.headers.update(headers)


def log_messeage():
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        **{
            "level": logging.INFO,
            "format": "%(asctime)s - %(lineno)s - %(message)s",
            "filename": f"{log_path}\\log{datetime.now().date()}.txt"
        })
    logger.addHandler(logging.StreamHandler())
    return logger


log = log_messeage()


def download(file_name, download_url, sessions=None, auth=None, params=None):
    if sessions is None:
        sessions = session
    file_path = os.path.join(sample_dir, file_name)
    if os.path.exists(file_path):
        return True
    try:
        content = sessions.get(download_url, auth=auth, params=params)
        if content.status_code == 200:
            content = content.content
            with open(file_path, "wb")as file:
                file.write(content)
            print(download_url, "Successful")
            return True
        else:
            return False
    except Exception as e:
        log.info(e)
        return False


def log_md5_ssd(*args):
    file_ssdeep_path = os.path.join(log_dir, f"0SsDeep{download_date}.log")
    file_md5_path = os.path.join(log_dir, f"md5{download_date}.log")
    if len(args) == 0:
        return file_ssdeep_path, file_md5_path
    else:
        md5 = args[0]
        ssd = args[-1]
        if len(args) == 1:
            with open(file_md5_path, "a+")as file:
                file.write(f"{args[0]}\n")
        else:
            line = f"{md5},{ssd}\n"
            with open(file_ssdeep_path, "a+")as file:
                file.write(line)
            with open(file_md5_path, "a+")as file:
                file.write(f"{md5}\n")


def tran_39():
    ssd_path, md5_path = log_md5_ssd()
    try:
        command_ssd = f"copy \"{ssd_path}\" \"{smart_log}\""
        command_md5 = f"copy \"{md5_path}\" \"{smart_log}\""
        os.system(command_md5)
        os.system(command_ssd)
        log.info("md5&ssd has copied")
    except Exception as e:
        log.info(e)


class SampleHy:

    def __init__(self):
        self.session = session
        base_url = "https://www.hybrid-analysis.com/download-sample/"
        data = self.login()
        if data is False:
            info = f"{base_url} download Failed"
            log.info(info)
            return
        try:
            download_num = 0
            for detail in data:
                md5 = detail["md5"]
                ssdeep = detail["ssdeep"]
                if ssdeep is not None:
                    log_md5_ssd(md5, ssdeep)
                file_name = md5 + ".bin.gz"
                download_url = base_url + detail["sha256"]
                if download(file_name, download_url, sessions=self.session):
                    download_num += 1
        except Exception as e:
            log.info(e)
        else:
            info = f"{base_url} download success, total {download_num}"
            log.info(info)

    def login(self):
        url_login = "https://www.hybrid-analysis.com/login"
        try:
            suop = BeautifulSoup(self.session.get(url_login).text, "lxml")
            token = suop.select("div [type=\"hidden\"]")[0].get("value")
            user_data = {
                "login[email]": "cicely@iobit.com",
                "login[password]": "IObit>20191213",
                "login[_token]": token
            }
            login_result = self.session.post(url_login, data=user_data)
            if login_result.status_code == 200:
                log.info(f"{url_login} login success")
            else:
                return False
            url_data_today = "https://www.hybrid-analysis.com/feed"
            result = self.session.get(url_data_today, params={"json": ""})
            if result.status_code == 200:
                return result.json()["data"]
            else:
                log.info(f"{url_data_today} get failed")
                return False
        except Exception as e:
            log.info(e)
            return False


class SampleVxvault:
    def __init__(self):
        url = "http://vxvault.net/ViriList.php"
        try:
            result = session.get(url).content.decode()
            suop = BeautifulSoup(result, "lxml")
            suop_add_date = suop.select("tr > td:nth-of-type(1) > a")
            suop_sample_md5 = suop.select("tr > td:nth-of-type(3) > a")
            download_num = 0
            for add_date, sample_md5 in zip(suop_add_date, suop_sample_md5):
                sample_link = "http://vxvault.net/%s" % add_date.get("href")
                add_date = add_date.getText()
                if add_date == download_date[-5:]:
                    sample_md5 = sample_md5.getText()
                    download_link = self.getlink(sample_link)
                    log_md5_ssd(sample_md5)
                    file_name = sample_md5 + ".vir"
                    if download(file_name, download_link):
                        download_num += 1
                elif add_date < download_date[-5:]:
                    break
        except Exception as e:
            log.info(e)
        else:
            info = f"{url} download success, total {download_num}"
            log.info(info)

    @staticmethod
    def getlink(sample_link):
        try:
            content = session.get(sample_link).content.decode()
            suop_link = re.findall(r"<B>Link:</B> hxxp://(.*?)<BR>", content)
            download_link = f"http://{suop_link[0]}"
            return download_link
        except Exception as e:
            log.info(e)
            return False


class SampleMalware:
    def __init__(self):
        sample_date = download_date.replace("-", "/")
        url = f"http://www.malware-traffic-analysis.net/{sample_date}/index.html"
        try:
            result = session.get(url)
            if result.status_code != 200:
                info = f"{url} download success, total 0"
                log.info(info)
                return
            download_num = 0
            suop = BeautifulSoup(result.text, "lxml").select("ul > li > a")
            for download_url in suop:
                if "-malware" in download_url.get("href"):
                    file_name = download_url.get("href")
                    download_url = url.replace("index.html", download_url.get("href"))
                    download_num += 1 if download(file_name, download_url) else 0
            info = f"{url} download success, total {download_num}"
            log.info(info)
        except Exception as e:
            log.info(e)


class SampleVirusign:
    def __init__(self):
        url = f"http://www.virusign.com/get_hashlist.php"
        params = {
            "ssdeep": "",
            "md5": "",
            "sha256": "",
            "start_date": download_date,
            "end_date": download_date
        }
        auth = ("infected", "infected")
        download_num = 0
        try:
            response = session.get(url, params=params, timeout=40)
            for sample_detail in response.text.split("\n")[:-1]:
                sample_detail = sample_detail.replace("\"", "").split(",")
                ssd = sample_detail[0]
                md5 = sample_detail[-1]
                sha256 = sample_detail[1]
                log_md5_ssd(md5, ssd)
                file_name = sha256 + ".7z"
                download_url = f"http://virusign.com/file/{sha256}.7z"
                if download(file_name, download_url, auth=auth):
                    download_num += 1
        except Exception as e:
            log.info(e)
        else:
            info = f"{url} download success, toatl {download_num}"
            log.info(info)


class SampleMalshare:

    def __init__(self):
        url_malshare = f"https://malshare.com/api.php"
        params = {
            "api_key": "1f36742f1f87e778ae1d4c370157581d746a4613fca10690f20949154b86589a",
            "action": "getlist"
        }
        try:
            response = session.get(url_malshare, params=params).json()
            params.update({"action": "getfile"})
            download_num = 0
            for sample in response:
                sample_md5 = sample["md5"]
                file_name = sample_md5 + ".vir"
                download_url = "https://malshare.com/api.php"
                params.update({"hash": sample_md5})
                auth = ("infected", "infected")
                log_md5_ssd(sample_md5)
                if download(file_name, download_url, sessions=session, auth=auth, params=params):
                    download_num += 1
        except Exception as e:
            log.info(e)
        else:
            info = f"{url_malshare} downlaod success, total {download_num}"
            log.info(info)


class SampleVirusbay:

    def __init__(self):
        self.session = session
        recent = self.login()
        sample_detail = [
            {info["md5"]: self.session.get("https://beta.virusbay.io/api/sample/%s/download/link" % info["_id"]).text
             for info in recent if download_date == info["publishDate"][:10]}
        ]
        self.session.headers.pop("Authorization")
        download_num = 0
        for detail in sample_detail:
            for md5, download_url in detail.items():
                log_md5_ssd(md5)
                file_name = f"{md5}.vir"
                if download(file_name, download_url, sessions=self.session):
                    download_num += 1
        info = f"https://beta.virusbay.io/login download success, total {download_num}"
        log.info(info)

    def login(self):
        url = "https://beta.virusbay.io/login"
        try:
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
        except Exception as e:
            log.info(e)
        else:
            return recent


class MakeRar:

    def __init__(self):
        self.de_all()
        self.de_all()
        # for file_name in os.listdir(sample_dir):
        #     file_path = os.path.join(sample_dir, file_name)
        #     self.rename(file_path)
        dist_path = self.co(sample_dir)
        if dist_path:
            command = f"copy \"{dist_path}\" \"{smart_dir}\""
            try:
                os.system(command)
                log.info(f"{dist_path} Ok")
            except Exception as e:
                info = f"{dist_path}, {e}"
                log.info(info)

    def de_all(self):
        for file_name in os.listdir(sample_dir):
            file_path = os.path.join(sample_dir, file_name)
            if file_path[-3:] in [".gz", "zip", "rar", ".7z"]:
                self.de(file_path)
                try:
                    os.remove(file_path)
                    info = f"{file_path} has delete by decompress"
                    log.info(info)
                except Exception as e:
                    log.info(e)

    @staticmethod
    def de(file_path, password="infected", dist_path=None):
        if os.path.exists(file_path) is False:
            return False
        if dist_path is None:
            dist_path = os.path.dirname(file_path)
        if os.path.exists(dist_path) is False:
            try:
                os.makedirs(dist_path)
            except OSError as e:
                log.info(e)
                return False
        file_type = file_path[-3:]
        command_dict = {
            "rar": f"rar e -p{password} -y \"{file_path}\" \"{dist_path}\"",
            "zip": f"7z e -p{password} -y \"{file_path}\" -o\"{dist_path}\"",
            ".gz": f"7z e -p{password} -y \"{file_path}\" -o\"{dist_path}\"",
            ".7z": f"7z e -p{password} -y \"{file_path}\" -o\"{dist_path}\""
        }
        try:
            check_output(command_dict[file_type], shell=True)
        except CalledProcessError as e:
            log.info(e)
            return False
        else:
            return True

    @staticmethod
    def co(file_path, dist_path=None):
        if os.path.exists(file_path) is False:
            return False
        if dist_path is None:
            dist_path = file_path + "[infected].rar"
        command = f"rar a -ep -pinfected -id[c,d,p,q] -y \"{dist_path}\" \"{file_path}\""
        try:
            check_output(command, shell=True)
        except CalledProcessError as e:
            log.info(e)
            return False
        else:
            return dist_path

    @staticmethod
    def rename(file_path):
        if os.path.exists(file_path):
            file_dir = os.path.dirname(file_path)
        else:
            return
        try:
            with open(file_path, "rb")as file:
                new_name = hashlib.md5(file.read()).hexdigest()
                new_path = os.path.join(file_dir, f"{new_name}.vir")
            if os.path.exists(new_path) is False:
                os.rename(file_path, new_path)
            else:
                os.remove(file_path)
                log.info(f"{file_path}, has delete by rename")
                return
        except Exception as e:
            log.info(f"{file_path}, {e}")


class SampleAll:

    def __init__(self):
        SampleHy()
        SampleVxvault()
        SampleMalware()
        SampleVirusign()
        SampleMalshare()
        SampleVirusbay()
        MakeRar()
        tran_39()


if __name__ == "__main__":
    SampleAll()
