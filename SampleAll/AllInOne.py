import os
import re
import sys
import chardet
from bs4 import BeautifulSoup
from subprocess import check_output
from urllib3 import disable_warnings
from requests import RequestException
from requests_html import HTMLSession
from datetime import datetime, timedelta

disable_warnings()


class Base:
    def __init__(self):
        self.session = HTMLSession()
        # self.run(download_date)

    def run(self, download_date):
        print(download_date)


class SampleVxvault(Base):

    def run(self, download_date):
        sample_dir = os.path.join(r"G:\AutoCollect", download_date.strftime("%Y-%m-%d"))  # 存放Sample
        url = "http://vxvault.net/ViriList.php/"
        sample_date = download_date.strftime("%m-%d")
        sample_list = []
        try:
            soup = self.session.get(url).html.find("tr > td:nth-of-type(1) > a")
            for add_date_element in soup:
                add_date = add_date_element.text
                if add_date < sample_date:
                    break
                if add_date == sample_date:
                    page_link = "http://vxvault.net/" + add_date_element.attrs["href"]
                    result = self.get_sample_detail(page_link)
                    if isinstance(result, tuple):
                        sample_md5, sample_url = result
                        sample_name = f"{sample_md5}.vir"
                        sample_path = os.path.join(sample_dir, sample_name)
                        sample_info = {
                            "sample_url": sample_url,
                            "sample_path": sample_path
                        }
                        sample_list.append(sample_info)
            if len(sample_list) == 0:
                return False, f"website: : {url},  has`t data."
            else:
                return True, sample_list
        except Exception as e:
            return False, f"Get Failed, url: {url}, error: {e}."

    def get_sample_detail(self, page_link):
        try:
            result = self.session.get(page_link)
            sample_md5 = re.findall(r"<B>MD5:</B> (.*?)<BR>", result.text)[0]
            sample_url = f"http://" + re.findall(r"<B>Link:</B> hxxp://(.*?)<BR>", result.text)[0]
            return sample_md5, sample_url
        except Exception as e:
            return f"Get Failed, url: {page_link}, error: {e}."


class SampleVirusign(Base):

    def run(self, download_date):
        sample_dir = os.path.join(r"G:\AutoCollect", download_date.strftime("%Y-%m-%d"))  # 存放Sample
        sample_date = download_date.strftime("%Y-%m-%d")
        url = f"http://www.virusign.com/get_hashlist.php"
        params = {
            "md5": "",
            "sha256": "",
            "start_date": sample_date,
            "end_date": sample_date
        }
        auth = ("infected", "infected")
        try:
            sample_list = []
            response = self.session.get(url, params=params, timeout=40).text
            for sample_sha256 in re.findall(r"\"(\w{64})\"", response):
                sample_name = f"{sample_sha256}.7z"
                sample_path = os.path.join(sample_dir, sample_name)
                sample_url = f"http://virusign.com/file/{sample_sha256}.7z"
                sample_info = {
                    "sample_md5": sample_sha256,
                    "sample_url": sample_url,
                    "sample_path": sample_path,
                    "auth": auth,
                    "is_archive": True
                }
                sample_list.append(sample_info)
            if len(sample_list) == 0:
                information = f"website today num is 0."
                return False, information
            else:
                return True, sample_list
        except Exception as e:
            information = f"parse website error: {e}."
            return False, information


class SampleAbuse(Base):

    def run(self, download_date):
        # api = "768fca1913d08f2e7479da1865f1b11a"
        sample_dir = r"G:\Abuse"
        if download_date.date() == datetime.today().date():
            return False, "Can`t Download today data"
        sample_date = download_date.strftime("%Y-%m-%d")
        sample_name = f"[infected]_mb-api_{sample_date}.zip"
        sample_url = f"https://mb-api.abuse.ch/downloads/{sample_date}.zip"
        sample_dict = {
            "sample_name": sample_name,
            "sample_path": os.path.join(sample_dir, sample_name),
            "sample_url": sample_url
        }
        sample_list = [sample_dict]
        return True, sample_list


class SampleHybrid(Base):

    def run(self, download_date):
        if isinstance(download_date, datetime) is False:
            return False, f"{download_date} is not isinstance datetime."
        sample_date = datetime.today() - timedelta(days=1)
        if download_date.date() != sample_date.date():
            return False, "website not support history data download."
        sample_dir = r"G:\AutoCollect"
        sample_dir = os.path.join(sample_dir, sample_date.strftime("%Y-%m-%d"))  # 存放Sample
        sample_list = []
        login_result, login_detail = self.hybird_login_session()
        for sha256 in set.union(self.get_latest(), self.get_feed()):
            if login_result:
                url_base = "https://www.hybrid-analysis.com/download-sample/"
                sample_name = f"{sha256}.bin.gz"
                sample_path = os.path.join(sample_dir, sample_name)
                sample_url = f"{url_base}{sha256}"
                sample_detail = {
                    "sample_md5": sha256,
                    "sample_name": sample_name,
                    "sample_path": sample_path,
                    "sample_url": sample_url,
                    "session": login_detail,
                    "is_archive": True
                }
                sample_list.append(sample_detail)
            else:
                sample_detail = {"sample_md5": sha256}
                sample_list.append(sample_detail)
        return True, sample_list

    def get_feed(self):
        # get download dict
        url_feed = "https://www.hybrid-analysis.com/feed"
        try:
            result = self.session.get(url_feed, params={"json": ""}).json()
        except Exception as e:
            information = f"Failed in Get Feed {url_feed}: {e}."
            return {information}
        else:
            sha256_set = set(detail["sha256"] for detail in result["data"])
            return sha256_set

    def get_latest(self):
        sample_set = set()
        url = "https://www.hybrid-analysis.com/submissions/sandbox/files"
        params = {
            "sort": "timestamp",
            "sort_order": "desc",
            "page": 1
        }
        selector = "a.analysis-overview-link.convert-link"
        for page in range(1, 11):
            params.update({"page": page})
            try:
                response = self.session.get(url, params=params).text
                soup = BeautifulSoup(response, "lxml").select(selector)
                for detail in soup:
                    sha256 = detail.get("href").split("/")[-1]
                    sample_set.add(sha256)
            except Exception as e:
                information = f"get {url} in page{page} error:{e}."
                sample_set.add(information)
                continue
        return sample_set

    def hybird_login_session(self):
        url_login = "https://www.hybrid-analysis.com/login"
        user_data = {
            "login[email]": "cicely@iobit.com",
            "login[password]": "IObit>20191213"
        }
        try:
            response = self.session.get(url_login)
            soup = BeautifulSoup(response.text, "lxml")
            token = soup.select("input#login__token")[0].get("value")
            user_data.setdefault("login[_token]", token)
            result = self.session.post(url_login, data=user_data)
            if "I forgot my password" in result.text:
                return False, "login failed."
            else:
                return True, self.session
        except Exception as e:
            return False, f"login Exception :{e}."


class SampleInfosec(Base):

    def sample_infosec(self, download_date):
        if isinstance(download_date, datetime) is False:
            return False, f"{download_date} is not isinstance datetime"
        sample_date = download_date.strftime("%Y-%m-%d")
        sample_dir = os.path.join(r"G:\AutoCollect", sample_date)  # 存放Sample
        if os.path.exists(sample_dir) is False:
            try:
                os.makedirs(sample_dir)
            except Exception as e:
                return False, f"Make dir {sample_dir} Exception: {e}."
        url = "https://infosec.cert-pa.it/analyze/"
        sample_list = []
        try:
            response = self.session.get(url + "submission.html").text
            md5_list = re.findall(f"<td>{sample_date} .*</td>\n.*\n.*<td><a href=\"/analyze/(.*).html\">", response)
            if len(md5_list) == 0:
                return False, "has`t data"
            for sample_md5 in md5_list:
                sample_name = f"{sample_md5}.vir"
                sample_path = os.path.join(sample_dir, sample_name)
                sample_response = self.session.get(url + sample_md5 + ".html").text
                link = re.findall(r"rel=\"nofollow\">.*?\.(.*?)</span><span class", sample_response)[0]
                sample_url = "http://" + link.strip("[").strip("]")
                sample_info = {
                    "sample_md5": sample_md5,
                    "sample_url": sample_url,
                    "sample_path": sample_path,
                    "is_archive": False
                }
                sample_list.append(sample_info)
            return True, sample_list
        except Exception as e:
            return False, f"Exception: {e}."


class SampleLimitedFree(Base):

    def run(self, download_date):
        sample_dir = r"G:\LimitedFree"
        sample_date = download_date.strftime("%Y%m%d")
        sample_name = f"virussign.com_{sample_date}_LimitedFree.zip"
        sample_url = f"http://samples.virussign.com/samples/{sample_name}"
        sample_info = {
            "sample_path": os.path.join(sample_dir, sample_name),
            "sample_name": sample_name,
            "sample_url": sample_url,
            "auth": ("f_yunwing1", "9kkSkk3dSd"),
            "stream": True,
            "is_archive": True
        }
        return True, [sample_info]


class SampleMalshare(Base):

    def run(self, download_date):
        sample_dir = os.path.join(r"G:\AutoCollect", download_date.strftime("%Y-%m-%d"))  # 存放Sample
        sample_date = download_date.strftime("%Y-%m-%d")
        md5_url = f"https://malshare.com/daily/{sample_date}/malshare_fileList.{sample_date}.sha1.txt"
        if download_date == datetime.today() - timedelta(days=1):
            md5_url = "https://malshare.com/daily/malshare.current.sha1.txt"
        try:
            response = self.session.get(md5_url)
            if response.status_code != 200:
                return False, f"{sample_date} has`t data"
            sample_list = []
            for line in response.text.split("\n")[:-1]:
                sample_md5 = line
                sample_name = sample_md5 + ".vir"
                sample_path = os.path.join(sample_dir, sample_name)
                action = "getfile"
                api_key = "2befc1c0b4d476b8527887f3f415648050638eff8dd400071f694e7356d5e49a"
                sample_url = f"https://malshare.com/api.php?api_key={api_key}&action={action}&hash={sample_md5}"
                sample_info = {
                    "sample_md5": sample_md5,
                    "sample_url": sample_url,
                    "sample_path": sample_path,
                }
                sample_list.append(sample_info)
            return True, sample_list
        except Exception as e:
            return False, f"link: {md5_url}, Exception: {e}."


class SampleSnapshot(Base):

    def __init__(self):
        super(SampleSnapshot).__init__()
        self.sample_dir = r"G:\snapshot"
        user = "iobit"
        pwd = "iobit#@6sample"
        self.auth = (user, pwd)
        self.option = {
            "auth": self.auth,
            "stream": True,
            "verify": False
        }

    def run(self, download_date):
        sample_date = download_date.strftime("%Y%m%d")
        sample_list = []
        sample_all_dict = self.parse_all(sample_date)
        sample_critical_dict = self.parse_critical(sample_date)
        sample_list.append(sample_all_dict) if isinstance(sample_all_dict, dict) else None
        sample_list.append(sample_critical_dict) if isinstance(sample_critical_dict, dict) else None
        if len(sample_list) > 0:
            return True, sample_list
        else:
            return False, f"has`t data {sample_date}."

    def parse_all(self, sample_date):
        sample_url = f"https://www.snapshot.clamav.net/daily/snapshot-all-{sample_date}.zip.001"
        sample_name = f"[infected]_snapshot_all_{sample_date}.zip"
        sample_path = os.path.join(self.sample_dir, sample_name)
        try:
            length_all = self.session.get(sample_url, **self.option).headers["content-length"]
            if int(length_all) > 1024:
                sample_all_dict = {
                    "sample_url": sample_url,
                    "sample_path": sample_path,
                    "auth": self.auth,
                    "stream": True,
                    "verify": False
                }
                return sample_all_dict
            else:
                return False
        except Exception as e:
            return e

    def parse_critical(self, sample_date):
        sample_url = f"https://www.snapshot.clamav.net/daily/snapshot-critical-{sample_date}.zip.001"
        sample_name = f"[infected]_snapshot_critical_{sample_date}.zip"
        sample_path = os.path.join(self.sample_dir, sample_name)
        try:
            length_critical = self.session.get(sample_url, **self.option).headers["content-length"]
            if int(length_critical) > 1024:
                sample_critical_dict = {
                    "sample_url": sample_url,
                    "sample_path": sample_path,
                    "auth": self.auth,
                    "stream": True,
                    "verify": False
                }
                return sample_critical_dict
            else:
                return False
        except Exception as e:
            return e


class SampleTraffic(Base):

    def run(self, download_date):
        sample_dir = r"G:\malware_traffic_analysis"
        sample_list = []
        sample_date = download_date.strftime("%Y/%m/%d")
        url = f"http://www.malware-traffic-analysis.net/{sample_date}/"
        try:
            result = self.session.get(url + "index.html")
            soup = result.html.find("ul > li > a") if result.status_code == 200 else None
            if soup is None:
                return False, "has`t data"
            for line in soup:
                sample_name = line.attrs["href"]
                sample_url = f"{url}{sample_name}"
                sample_path = os.path.join(sample_dir, sample_name)
                if "-malware" in sample_name:
                    sample_info = {
                        "sample_path": sample_path,
                        "sample_url": sample_url,
                        "is_archive": True
                    }
                    sample_list.append(sample_info)
            if len(sample_list) == 0:
                return False, f"has`t data {sample_date}"
            return True, sample_list
        except Exception as e:
            return False, e


class SampleUrlhaus(Base):

    def run(self, download_date):
        sample_dir = r"G:\Urlhaus"
        sample_date = download_date.strftime("%Y-%m-%d")
        sample_name = f"[infected]_UrlHash_{sample_date}.zip"
        download_url = f"https://urlhaus-api.abuse.ch/downloads/{sample_date}.zip"
        sample_info = {
            "sample_path": os.path.join(sample_dir, sample_name),
            "sample_url": download_url,
            "stream": True,
            "is_archive": True
        }
        return True, [sample_info]


class SampleVirusbay(Base):

    def login(self):
        data = {
            "email": "niwangxiu@gmail.com",
            "password": "testvirus0504L"
        }
        login_url = "https://beta.virusbay.io/login"
        try:
            response = self.session.post(url=login_url, data=data)
            token = response.json()["token"]
            authorization = {"Authorization": "JWT %s" % token}
            self.session.headers.update(authorization)
            return self.session
        except Exception as e:
            return f"login failed, Exception: {e}."

    def run(self, download_date):
        sample_dir = os.path.join(r"G:\AutoCollect", download_date.strftime("%Y-%m-%d"))  # 存放Sample
        sample_date = download_date.strftime("%Y-%m-%d")
        session = self.login()
        if isinstance(session, HTMLSession) is False:
            return False, session
        data_url = "https://beta.virusbay.io/sample/data"
        recent = session.get(url=data_url).json()["recent"]
        sample_list = []
        for sample in recent:
            add_date = sample["publishDate"][:10]
            sample_md5 = sample["md5"]
            sample_name = sample_md5 + ".vir"
            sample_path = os.path.join(sample_dir, sample_name)
            sample_link = "https://beta.virusbay.io/api/sample/%s/download/link" % sample["_id"]
            if add_date == sample_date:
                try:
                    sample_url = session.get(sample_link).text
                except Exception as e:
                    sample_url = f"Exception parse: {e}"
                sample_info = {
                    "sample_md5": sample_md5,
                    "sample_url": sample_url,
                    "sample_path": sample_path,
                }
                sample_list.append(sample_info)
        return True, sample_list


class Run:

    def __init__(self):
        self.download_date = datetime.today()  # 程序开始时间

        self.log_log_dir = r"G:\SampleLog\DownloadLog"  # 存放下载日志位置
        self.log_path = os.path.join(self.log_log_dir, "%s.log" % self.download_date.strftime("%Y%m%d"))  # 存放下载日志位置

        self.log_md5_dir = r"G:\SampleLog\MD5"  # 存放下载的MD5位置
        self.md5_path = os.path.join(self.log_md5_dir, "%s.txt" % self.download_date.strftime("%Y%m%d"))  # 存放下载的MD5位置

        self.smart_file_dir = r"G:\Auto"  # 转移到smartccl位置
        self.smart_md5_dir = r"\\192.168.1.39\e\VTSpider\MD5SHA256"  # 转移MD5到39位置
        try:
            if os.path.exists(self.log_log_dir) is False:
                os.makedirs(self.log_log_dir)
            if os.path.exists(self.log_md5_dir) is False:
                os.makedirs(self.log_md5_dir)
            open(self.md5_path, "w").close()
        except Exception as e:
            exit(e)
        if len(sys.argv) > 1:
            input_date = sys.argv[-1]
            if re.match(r"%Y%m%d", input_date) is not None:
                self.sample_date = datetime.strptime(sys.argv[-1], "%Y%m%d")
            else:
                self.sample_date = None
                exit("data error, ex:20200301")
        else:
            self.sample_date = datetime.today() - timedelta(days=1)
        self.start()

    def write_log(self, info):
        with open(self.log_path, "a+", encoding="utf-8") as file:
            line = f"{datetime.today()}: {info}\n"
            file.write(line)
            print(line)

    def write_hash(self, sample_hash):
        if sample_hash is None:
            return
        try:
            if re.match(r"^[a-zA-Z0-9]{32}$|^[a-zA-Z0-9]{64}$", sample_hash):
                with open(self.md5_path, "r+", encoding="utf-8") as file:
                    if len(sample_hash) == 32:
                        data = f"{sample_hash}\n" + file.read()
                        file.seek(0)
                    else:
                        data = f"{sample_hash}\n"
                        file.seek(0, 2)
                    file.write(data)
        except Exception as er:
            self.write_log(f"write has Exception:{er}.")

    @staticmethod
    def trans(file_path, dist):
        if os.path.exists(file_path) is False:
            return f"target file: {file_path} not exists."
        if os.path.exists(dist) is False:
            return f"dist dir: {dist} not exists."
        try:
            os.system(f"copy \"{file_path}\" \"{dist}\"")
            return f"copy {file_path} to {dist} Successful."
        except Exception as e:
            return f"copy {file_path} to {dist} Exception: {e}."

    @staticmethod
    def encoding(string):
        if type(string) is bytes:
            return chardet.detect(string)["encoding"]
        if type(string) is str and os.path.exists(string):
            try:
                with open(string, "rb")as file:
                    return chardet.detect(file.read())["encoding"]
            except Exception as e:
                return e

    def extract(self, file_path, pwd="infected"):
        # Determine if the file exists
        if os.path.exists(file_path) is False:
            return f"File isn`t exists: {file_path}."
        # Determine if the file is a compressed file supported by 7z
        try:
            command = f"7z t \"{file_path}\" -p{pwd}"
            result = check_output(command, shell=True)
            result_string = result.decode(self.encoding(result))
            if "Everything is Ok" in result_string:
                dist_dir = os.path.dirname(file_path)
                extract_command = f"7z e -y -aot -p{pwd} \"{file_path}\" -o\"{dist_dir}\""
                check_output(extract_command, shell=True)
                return f"{file_path} has extract over."
            else:
                return "File error"
        except Exception as e:
            return f"Command error: {e}."

    @staticmethod
    def archive(file_path, dist_path, pwd="infected"):
        if os.path.exists(file_path) is False:
            return False, "file don`t exists"
        try:
            command = f"rar a -ep -p{pwd} -id[c,d,p,q] -y \"{dist_path}\" \"{file_path}\""
            check_output(command, shell=True)
            return True, "compression successful"
        except Exception as e:
            return False, f"compression error: {e}"

    def download(self, file_path, url, **kwargs):
        if file_path is None:
            return False, "No path to save."
        file_dir = os.path.dirname(file_path)
        if os.path.exists(file_dir) is False:
            try:
                os.makedirs(file_dir)
            except Exception as e:
                return False, f"Make dir {file_dir} Exception: {e}."
        if url is None:
            return False, f"No url to Requests."
        session = kwargs.setdefault("session", HTMLSession())
        method = kwargs.setdefault("method", "get")
        verify = kwargs.setdefault("verify", True)
        option = {
            "auth": kwargs.setdefault("auth"),
            "params": kwargs.setdefault("params"),
            "stream": kwargs.setdefault("stream", True),
            "timeout": (30, 20),
            "verify": verify
        }
        if os.path.exists(file_path):
            with open(file_path, "rb")as file:
                file_size = len(file.read())
        else:
            file_size = 0
        session.headers.update({"Range": f"bytes={file_size}-"})
        response = session.request(method=method, url=url, **option)
        status_code = response.status_code
        if status_code == 416:
            return False, f"Request: {url}, status_code: {status_code}.Range overflow."
        if status_code == 404:
            return False, f"Request: {url}, status_code: {status_code}.data not found."
        if status_code == 403:
            return False, f"Request: {url}, status_code: {status_code}.Access Denied."
        if status_code == 429:
            return False, f"Request: {url}, status_code: {status_code}.Too Many Requests."
        response_size = response.headers.setdefault("content-length")
        total_size = int(response_size) + file_size
        if total_size == file_size:
            return True, f"File has download. file_size: {file_size}."
        if status_code == 206:
            try:
                with open(file_path, "ab+")as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)
                        file.flush()
                        file_size += len(chunk)
                        percent = "{:.2%}".format(file_size / total_size)
                        print(f"\r{datetime.today()}: {file_size}/{total_size}-- percent:{percent}", end="")
                    print()
                    return True, "Download Ok"
            except RequestException:
                print("\ndownload again.")
                return self.download(file_path, url, **kwargs)

    def start(self):
        sample_list = [
            {"website": "http://vxvault.net/ViriList.php/ViriFiche.php", "function": SampleVxvault, "is_trans": False},
            {"website": "http://www.virusign.com/get_hashlist.php", "function": SampleVirusign, "is_trans": False},
            {"website": "https://beta.virusbay.io/sample/data", "function": SampleVirusbay, "is_trans": False},
            {"website": "https://infosec.cert-pa.it/analyze/", "function": SampleInfosec, "is_trans": False},
            {"website": "https://www.hybrid-analysis.com", "function": SampleHybrid, "is_trans": False},
            {"website": "https://malshare.com/api.php", "function": SampleMalshare, "is_trans": False},
            {"website": "http://samples.virussign.com/samples", "function": SampleLimitedFree, "is_trans": True},
            {"website": "http://www.malware-traffic-analysis.net", "function": SampleTraffic, "is_trans": True},
            {"website": "https://www.snapshot.clamav.net/daily", "function": SampleSnapshot, "is_trans": True},
            {"website": "https://bazaar.abuse.ch/browse/", "function": SampleAbuse, "is_trans": True},
            {"website": "https://urlhaus-api.abuse.ch", "function": SampleUrlhaus, "is_trans": True}
        ]
        for value in sample_list:
            website = value["website"]
            function = value["function"]
            is_trans = value["is_trans"]
            self.write_log(f"------START WEBSITE: {website}")
            result, detail = function(self.sample_date).run(self.sample_date)
            download_num = 0
            if result:
                total_num = len(detail)
                for sample_dict in detail:
                    sample_md5 = sample_dict.setdefault("sample_md5")
                    sample_url = sample_dict.setdefault("sample_url")
                    sample_path = sample_dict.setdefault("sample_path")
                    is_archive = sample_dict.setdefault("is_archive", False)
                    self.write_hash(sample_md5) if sample_md5 is not None else None
                    self.write_log(f"URL: {sample_url}")
                    self.write_log(f"PATH: {sample_path}")
                    download_result, download_information = self.download(sample_path, sample_url, **sample_dict)
                    self.write_log(download_information)
                    download_num += 1 if download_result else 0
                    if is_trans and download_result:
                        trans_detail = self.trans(sample_path, self.smart_file_dir)
                        self.write_log(trans_detail)
                    if is_archive and download_result and is_trans is False:
                        extract_detail = self.extract(sample_path)
                        self.write_log(extract_detail)
                        try:
                            os.remove(sample_path)
                            self.write_log(f"delete archive file {sample_path}: ok.")
                        except Exception as delete_error:
                            self.write_log(f"delete failed, Exception: {delete_error}.")
            else:
                total_num = 0
                self.write_log(detail)
            self.write_log(f"total_num: {total_num}, download_num: {download_num}.")
            self.write_log(f"------END WEBSITE: {website}\n")


if __name__ == "__main__":
    Run()
