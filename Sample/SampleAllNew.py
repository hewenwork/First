import os
import re
import requests_html
from subprocess import check_output
from datetime import datetime, timedelta

download_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")  # 样本下载日期

Init_dir = r"G:\AutoCollect"
sample_dir = os.path.join(Init_dir, download_date)  # 存放Sample

log_dir = os.path.join(Init_dir, "log")  # 存放MD5和SSD
log_path = os.path.join(log_dir, f"{download_date}.log")  # 存放下载日志

smart_file_dir = r"G:\Auto"  # 转移到smartccl位置
smart_log_dir = r"\\192.168.1.39\e\VTSpider\MD5SHA256"  # 转移到39位置

if os.path.exists(sample_dir) is False:
    os.makedirs(sample_dir)

if os.path.exists(log_dir) is False:
    os.makedirs(log_dir)

session = requests_html.HTMLSession()


def write_log(info):
    with open(log_path, "a+", encoding="utf-8")as file:
        file.write(f"{datetime.today()}:  {info}\n")


def compression(file_path, dist_path, pwd="infected"):
    if os.path.exists(file_path) is False:
        return False, "file don`t exists"
    try:
        command = f"rar a -ep -p{pwd} -id[c,d,p,q] -y \"{dist_path}\" \"{file_path}\""
        check_output(command, shell=True)
        return True, "compression successful"
    except Exception as e:
        return False, f"compression error: {e}"


def decompression(file_path, pwd="infected"):
    if os.path.exists(file_path) is False:
        return False, "File don`t exists"
    file_type = file_path[-3:]
    dist_path = file_path.split(".")[0] + ".vir"
    type_command = {
        "rar": f"rar e -p{pwd} -y \"{file_path}\" \"{dist_path}\"",
        "7z": f"7z e -p{pwd} -y \"{file_path}\" -so > \"{dist_path}\"",
        "zip": f"7z e -p{pwd} -y \"{file_path}\" -so > \"{dist_path}\"",
        ".gz": f"7z e -p{pwd} -y \"{file_path}\" -so > \"{dist_path}\"",
    }
    if file_type in type_command is False:
        return False, "File isn`t compression"
    try:
        command = type_command[file_type]
        check_output(command, shell=True)
        os.remove(file_path)
        return True, "Decompression successful"
    except Exception as e:
        return False, f"Decompression Error: {e}"


def download(file_path, link, auth=None, params=None):
    if os.path.exists(file_path):
        return False, "file exists"
    try:
        content = session.get(link, auth=auth, params=params)
        if content.status_code == 200:
            content = content.content
            with open(file_path, "wb")as file:
                file.write(content)
            return True, file_path
        else:
            return False, "file download failed"
    except Exception as e:
        return False, f"error: {e}"


class Sample:

    def __init__(self):
        self.sample_dict = {
            "http://vxvault.net/ViriList.php/ViriFiche.php": self.sample_vxvault(),
            "https://www.hybrid-analysis.com": self.sample_hy(),
            "https://beta.virusbay.io/sample/data": self.sample_virusbay(),
            "https://malshare.com/api.php": self.sample_malshare(),
            # "http://www.virusign.com/get_hashlist.php": self.sample_virusign(),
            "http://www.malware-traffic-analysis.net": self.sample_traffic(),
            "https://infosec.cert-pa.it/analyze/": self.sample_infosec()
        }

    @staticmethod
    def sample_vxvault():
        url = "http://vxvault.net/ViriList.php/"
        try:
            soup = session.get(url)
            sample_dict = {}
            for i in soup.html.find("tr > td:nth-of-type(1) > a"):
                sample_link = "http://vxvault.net/" + i.attrs["href"]
                result = session.get(sample_link)
                sample_date = re.findall(r"<B>Added:</B> (.*?)<BR>", result.text)[0]
                if sample_date == download_date:
                    sample_md5 = re.findall(r"<B>MD5:</B> (.*?)<BR>", result.text)[0]
                    sample_url = f"http://" + re.findall(r"<B>Link:</B> hxxp://(.*?)<BR>", result.text)[0]
                    sample_info = {
                        "sample_path": os.path.join(sample_dir, sample_md5 + ".vir"),
                        "sample_url": sample_url
                    }
                    sample_dict.update({sample_md5: sample_info})
                elif sample_date < download_date:
                    break
            return sample_dict
        except Exception as e:
            return f"error: {e}"

    @staticmethod
    def sample_hy():
        # update login session
        url_login = "https://www.hybrid-analysis.com/login"
        try:
            token = session.get(url_login).html.find("input#login__token")[0].attrs["value"]
            user_data = {
                "login[email]": "cicely@iobit.com",
                "login[password]": "IObit>20191213",
                "login[_token]": token
            }
            session.post(url_login, data=user_data)
        except Exception as e:
            return e

        sample_dict = {}
        # get download dict
        url_feed = "https://www.hybrid-analysis.com/feed"
        try:
            result = session.get(url_feed, params={"json": ""})
            data = result.json()["data"]
            url_base = "https://www.hybrid-analysis.com/download-sample/"
            for detail in data:
                sample_md5 = detail["md5"]
                file_name = sample_md5 + ".bin.gz"
                file_path = os.path.join(sample_dir, file_name)
                download_url = url_base + detail["sha256"]
                sample_info = {
                    "sample_path": file_path,
                    "sample_url": download_url,
                    # "session": session
                }
                sample_dict.update({sample_md5: sample_info})
            return sample_dict
        except Exception as e:
            return e

    @staticmethod
    def sample_virusbay():
        login_url = "https://beta.virusbay.io/login"
        data = {
            "email": "niwangxiu@gmail.com",
            "password": "testvirus0504L"
        }
        sample_dict = {}
        try:
            response = session.post(url=login_url, data=data)
            token = response.json()["token"]
            authorization = {"Authorization": "JWT %s" % token}
            session.headers.update(authorization)
            data_url = "https://beta.virusbay.io/sample/data"
            recent = session.get(url=data_url).json()["recent"]
            for sample in recent:
                sample_date = sample["publishDate"][:10]
                if download_date == sample_date:
                    sample_md5 = sample["md5"]
                    sample_name = sample_md5 + ".vir"
                    sample_link = "https://beta.virusbay.io/api/sample/%s/download/link" % sample["_id"]
                    sample_url = session.get(sample_link).text
                    sample_info = {
                        "sample_path": os.path.join(sample_dir, sample_name),
                        "sample_url": sample_url
                    }
                    sample_dict.update({sample_md5: sample_info})
            return sample_dict
        except Exception as e:
            return e

    @staticmethod
    def sample_malshare():
        url = f"https://malshare.com/api.php"
        params = {
            "api_key": "1f36742f1f87e778ae1d4c370157581d746a4613fca10690f20949154b86589a",
            "action": "getlist"
        }
        auth = ("infected", "infected")
        try:
            sample_dict = {}
            response = session.get(url, params=params).json()
            params.update({"action": "getfile"})
            for sample in response:
                sample_md5 = sample["md5"]
                sample_name = sample_md5 + ".vir"
                sample_url = "https://malshare.com/api.php"
                params.update({"hash": sample_md5})
                sample_info = {
                    "sample_path": os.path.join(sample_dir, sample_name),
                    "sample_url": sample_url,
                    "auth": auth,
                    "params": params
                }
                sample_dict.update({sample_md5: sample_info})
            return sample_dict
        except Exception as e:
            return e

    @staticmethod
    def sample_virusign():
        url = f"http://www.virusign.com/get_hashlist.php"
        params = {
            "md5": "",
            "sha256": "",
            "start_date": download_date,
            "end_date": download_date
        }
        auth = ("infected", "infected")
        try:
            sample_dict = {}
            response = session.get(url, params=params, timeout=40).text
            sha256_list = re.findall(r"\"(\w{64})\"", response)
            md5_list = re.findall(r"\"\w{64}\",\"(\w{32})\"", response)
            for sample_md5, sample_sah256 in zip(md5_list, sha256_list):
                sample_info = {
                    "sample_path": os.path.join(sample_dir, sample_md5 + ".7z"),
                    "sample_url": f"http://virusign.com/file/{sample_sah256}.7z",
                    "auth": auth
                }
                sample_dict.update({sample_md5: sample_info})
            return sample_dict
        except Exception as e:
            return e

    @staticmethod
    def sample_traffic():
        sample_dict = {}
        sample_date = download_date.replace("-", "/")
        url = f"http://www.malware-traffic-analysis.net/{sample_date}/"
        try:
            result = session.get(url + "index.html")
            soup = result.html.find("ul > li > a") if result.status_code == 200 else None
            if soup is None:
                return "has`t data"
            for line in soup:
                sample_name = line.attrs["href"]
                if "-malware" in sample_name:
                    sample_url = url + sample_name
                    sample_info = {
                        "sample_path": os.path.join(sample_dir, sample_name),
                        "sample_url": sample_url
                    }
                    sample_dict.update({sample_name: sample_info})
            return sample_dict
        except Exception as e:
            return e

    @staticmethod
    def sample_infosec():
        url = "https://infosec.cert-pa.it/analyze/"
        try:
            sample_dict = {}
            response = session.get(url + "submission.html").text
            md5_list = re.findall(f"<td>{download_date} .*</td>\n.*\n.*<td><a href=\"/analyze/(.*).html\">", response)
            if len(md5_list) == 0:
                return "has`t data"
            for sample_md5 in md5_list:
                sample_response = session.get(url + sample_md5 + ".html").text
                link = re.findall(r"rel=\"nofollow\">.*?\.(.*?)</span><span class", sample_response)[0]
                sample_url = "http://" + link.strip("[").strip("]")
                sample_info = {
                    "sample_path": os.path.join(sample_dir, sample_md5 + ".vir"),
                    "sample_url": sample_url
                }
                sample_dict.update({sample_md5: sample_info})
            return sample_dict
        except Exception as e:
            return e
