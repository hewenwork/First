import json
import os
import re
import datetime
import requests
from bs4 import BeautifulSoup
from subprocess import check_output, SubprocessError


class Base:

    def __init__(self):
        self.base_dir = r"G:\auto_collect"
        self.download_date = self.get_download_date()
        self.download_log = self.get_download_log_path()
        self.download_folder = self.get_download_folder()
        self.download_failed = self.get_download_failed_path()

    @staticmethod
    def get_download_date():
        if os.path.exists("test.txt"):
            with open("test.txt", "r")as file:
                days = int(file.read())
        else:
            days = 1
        today = datetime.datetime.today()
        time_interval = datetime.timedelta(days=days)
        download_day = today - time_interval
        return download_day.strftime("%Y-%m-%d")

    @staticmethod
    def get_session():
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        headers = {"User-Agent": user_agent}
        session = requests.session()
        session.headers.update(headers)
        return session

    @staticmethod
    def write_sample(sample_path, sample_download_url, session):
        if os.path.exists(sample_path):
            return True
        else:
            try:
                response = session.get(url=sample_download_url, timeout=5)
                if response.status_code == 200:
                    with open(sample_path, "wb")as file:
                        file.write(response.content)
                    return True
                else:
                    return False
            except requests.RequestException:
                return False
            except OSError:
                return False

    @staticmethod
    def start_info():
        sample_info = {}
        session = Base.get_session()
        download_date = Base.get_download_date()
        return sample_info, session, download_date

    def get_download_folder(self):
        download_folder = os.path.join(self.base_dir, self.download_date)
        if os.path.exists(download_folder) is False:
            os.makedirs(download_folder)
        return download_folder

    def get_download_failed_path(self):
        download_data = Base.get_download_date()
        failed_dir = os.path.join(self.base_dir, r"MD5&SHA256")
        failed_path = os.path.join(failed_dir, "Failed{}.txt".format(download_data))
        if os.path.exists(failed_dir) is False:
            os.makedirs(failed_dir)
        return failed_path

    def get_download_log_path(self):
        download_data = Base.get_download_date()
        log_dir = os.path.join(self.base_dir, r"Log")
        log_path = os.path.join(log_dir, "{}.log".format(download_data))
        if os.path.exists(log_dir) is False:
            os.makedirs(log_dir)
        return log_path

    def write_sample_md5(self, md5):
        file_path = self.download_failed
        if os.path.exists(file_path):
            if len(md5) == 64:
                with open(file_path, "a+")as file:
                    file.write(md5 + "\n")
            else:
                with open(file_path, "r+")as file:
                    old_data = file.read()
                    file.seek(0, 0)
                    file.write(md5 + "\n" + old_data)
        else:
            with open(file_path, "a+")as file:
                file.write(md5 + "\n")

    def write_download_log(self, result):
        log_path = self.download_log
        if os.path.exists(log_path):
            with open(log_path, "r+")as file:
                old_data = file.read()
                file.seek(0, 0)
                file.write(result + "\n" + old_data)
        else:
            with open(log_path, "a+")as file:
                file.write(result + "\n")

    def start_download(self, sample_info, session, target):
        print("\n", target)
        failed_num = 0
        total_num = len(sample_info)
        if total_num is 0:
            result = "{}--has`t data".format(target)
        else:
            download_num = 0
            for file_name, download_url in sample_info.items():
                file_md5 = os.path.splitext(file_name)[0]
                file_path = os.path.join(self.download_folder, file_name)
                download_result = Base.write_sample(file_path, download_url, session)
                if download_result is False:
                    failed_num += 1
                    Base().write_sample_md5(file_md5)
                download_num += 1
                print("\rdownload", "{} / {}".format(download_num, total_num), end="")
            result = "{0} -- Failed:{1}  Total:{2}".format(target, failed_num, total_num)
        Base().write_download_log(result=result)
        print("\n", result)


class SampleMalc0de:

    def __init__(self):
        url = "http://malc0de.com/database/"
        sample_info, session, download_date = Base.start_info()
        self.switch_vpn("on")
        sample_info = self.get_dict()
        self.switch_vpn("off")
        Base().start_download(sample_info=sample_info, session=session, target=url)

    @staticmethod
    def switch_vpn(turn):
        print("Switch VPN " + turn)
        connect_command = "rasdial  US usa vpn2014"
        disconnect_command = "rasdial US /DISCONNECT"
        command_dict = {
            "on": connect_command,
            "off": disconnect_command
        }
        try:
            check_output(command_dict[turn], shell=True)
            return True
        except SubprocessError as e:
            print(e)

    @staticmethod
    def get_dict():
        url = "http://malc0de.com/database/"
        sample_info, session, download_date = Base.start_info()
        try:
            response = session.get(url, timeout=10)
            suop = BeautifulSoup(response.text, "lxml")
            sample_data_list = suop.select("tr > td:nth-of-type(1)")
            sample_url_list = suop.select("tr > td:nth-of-type(2)")
            sample_md5_list = suop.select("tr > td:nth-of-type(7)")
            for sample_date, sample_url, sample_md5 in zip(sample_data_list, sample_url_list, sample_md5_list):
                add_date = sample_date.getText()
                sample_md5 = sample_md5.getText()
                file_name = sample_md5 + ".vir"
                sample_url = "http://" + sample_url.getText()
                if add_date == download_date:
                    sample_info[file_name] = sample_url
            return sample_info
        except requests.RequestException as e:
            print(e)


class SampleVxvault:

    def __init__(self):
        url = "http://vxvault.net/ViriList.php"
        sample_info, session, download_date = Base.start_info()
        try:
            response = session.get(url=url)
            suop = BeautifulSoup(response.text, "lxml")
            suop_add_date = suop.select("tr > td:nth-of-type(1) > a")
            suop_url = suop.select("tr > td:nth-of-type(2) > a:nth-of-type(2)")
            for add_date, link in zip(suop_add_date, suop_url):
                add_date = add_date.getText()
                link = "http://vxvault.net/" + link.get("href")
                if add_date == download_date[5:]:
                    file_name, download_url = SampleVxvault.get_sample_info(session, link)
                    sample_info[file_name] = download_url
                elif add_date < download_date[5:]:
                    break
            Base().start_download(sample_info=sample_info, session=session, target=url)
        except requests.RequestException:
            Base().write_download_log(result=url + "--" * 4 + "Connect Error")

    @staticmethod
    def get_sample_info(session, link):
        sample_response = session.get(url=link).text
        sample_md5 = re.findall("MD5:</B> (.*?)<BR>", sample_response)[0]
        file_name = sample_md5 + ".vir"
        sample_download_url = re.findall("Link:</B> (.*?)<BR>", sample_response)[0].replace("hxxp:", "http:")
        return file_name, sample_download_url


class SampleHybrid:

    def __init__(self):
        url = "https://www.hybrid-analysis.com"
        self.session = self.get_login_session()
        sample_info, session, download_date = Base.start_info()
        sample_info.update(self.get_last_info())
        sample_info.update(self.get_page_info())
        Base().start_download(sample_info=sample_info, session=self.session, target=url)

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
        except requests.RequestException as e:
            print(e)
        return session

    def get_last_info(self):
        json_dict = {}
        url = "https://www.hybrid-analysis.com/feed?json"
        try:
            base_url = "https://www.hybrid-analysis.com/download-sample/"
            json_content = self.session.get(url).json()
            for data_type in json_content["data"]:
                md5 = data_type["md5"]
                file_name = md5 + ".gz"
                sha256 = data_type["sha256"]
                environmentId = data_type["environmentId"]
                threatlevel = data_type["threatlevel"]
                if threatlevel != 0:
                    download_url = base_url + sha256 + "?environmentId=%s" % environmentId
                    json_dict[file_name] = download_url
        except requests.RequestException as e:
            print(e)
        return json_dict

    def get_page_info(self):
        page_dict = {}
        url = "https://www.hybrid-analysis.com/recent-submissions"
        threat_level = ["malicious", "ambiguous", "suspicious", "-"]
        for page in range(11):
            params = {
                "filter": "file",
                "sort": "^timestamp",
                "page": page
            }
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
            except requests.RequestException as e:
                print(e)
        return page_dict


class SampleVirusBay:

    def __init__(self):
        url = "https://beta.virusbay.io/sample/data"
        sample_info, session, download_date = Base.start_info()
        session = SampleVirusBay.get_login_session()
        if session:
            recent = session.get(url=url).json()["recent"]
            for info in recent:
                add_date = info["publishDate"][:10]
                _id = info["_id"]
                sample_md5 = info["md5"]
                file_name = sample_md5 + ".vir"
                link = "https://beta.virusbay.io/api/sample/%s/download/link" % _id
                sample_download_url = session.get(link).text
                sample_info[file_name] = sample_download_url
                if download_date == add_date:
                    sample_info[file_name] = sample_download_url
                elif download_date > add_date:
                    break
            session = Base().get_session()
            Base().start_download(sample_info=sample_info, session=session, target=url)
        else:
            result = url + "-" * 4 + "Login Error"
            Base().write_download_log(result=result)

    @staticmethod
    def get_login_session():
        url = "https://beta.virusbay.io/login"
        data = {
            "email": "niwangxiu@gmail.com",
            "password": "testvirus0504L"
        }
        session = Base.get_session()
        try:
            response = session.post(url=url, data=data)
            token = response.json()["token"]
            authorization = {"Authorization": "JWT %s" % token}
            session.headers.update(authorization)
            return session
        except requests.RequestException as e:
            print(e)
            return False


class SampleMalwareTrafficAnalysis:

    def __init__(self):
        sample_info, session, download_date = Base.start_info()
        download_date = download_date.replace("-", "/")
        url = "http://www.malware-traffic-analysis.net/%s/index.html" % download_date
        if session.get(url).status_code == 200:
            sample_suop = BeautifulSoup(session.get(url).text, "lxml").select("ul > li > a")
            for download_url in sample_suop:
                if "-malware" in download_url.get("href"):
                    sample_name = download_url.get("href")
                    sample_download_url = url.replace("index.html", sample_name)
                    sample_info[sample_name] = sample_download_url
            Base().start_download(sample_info=sample_info, session=session, target=url)
        else:
            result = url + "--has`t data"
            Base().write_download_log(result=result)


class SampleVirusSign:

    def __init__(self):
        url = "http://virusign.com/get_hashlist.php"
        sample_info, session, download_date = Base.start_info()
        session.auth = ("infected", "infected")
        params = {
            "sha256": "",
            "n": "ANY",
            "start_date": download_date,
            "end_date": download_date
        }
        response = session.get(url, params=params).text
        if response is not "":
            for sha256 in response.split("\n")[:-1]:
                sha256 = sha256.replace("\"", "")
                file_name = sha256 + ".7z"
                sample_download_url = "http://virusign.com/file/%s" % file_name
                sample_info[file_name] = sample_download_url
            Base().start_download(sample_info=sample_info, session=session, target=url)
        else:
            result = url + "--has`t data"
            Base().write_download_log(result=result)


class SampleMalshare:

    def __init__(self):
        url = "https://malshare.com/api.php"
        sample_info, session, download_date = Base.start_info()
        api_key = "1f36742f1f87e778ae1d4c370157581d746a4613fca10690f20949154b86589a"
        params = {
            "api_key": api_key,
            "action": "getlist"
        }
        try:
            response = session.get(url=url, params=params).json()
            for sample in response:
                sample_md5 = sample["md5"]
                file_name = sample_md5 + ".vir"
                download_url = url + "?api_key=%s&action=getfile&hash=%s" % (api_key, sample_md5)
                sample_info[file_name] = download_url
            Base().start_download(sample_info=sample_info, session=session, target=url)
        except requests.RequestException as e:
            result = url + "RequestException Error"
            Base().write_download_log(result=result)
        except json.decoder.JSONDecodeError as j:
            result = url + "decoder.JSONDecodeError Error"
            Base().write_download_log(result=result)


class SampleInfosec:

    def __init__(self):
        url = "https://infosec.cert-pa.it/"
        sample_info, session, download_date = Base.start_info()
        try:
            for page in range(1, 10):
                sample_info.update(SampleInfosec.get_page_info(download_date, session, page))
            Base().start_download(sample_info=sample_info, session=session, target=url)
        except requests.RequestException as e:
            result = url + str(e)
            Base.write_download_log(result=result)

    @staticmethod
    def get_page_info(download_date, session, page):
        page_dict = {}
        base_url = "https://infosec.cert-pa.it/analyze/submission-page-{}.html".format(page)
        try:
            response = session.get(base_url)
            date_list = BeautifulSoup(response.text, "lxml").select("tr > td:nth-of-type(1)")
            md5_list = BeautifulSoup(response.text, "lxml").select("tr > td:nth-of-type(3)")
            for add_date, sample_md5 in zip(date_list, md5_list):
                add_date = add_date.getText()[:10]
                sample_md5 = sample_md5.getText()
                file_name = sample_md5 + ".vir"
                link = "https://infosec.cert-pa.it/analyze/{}.html".format(sample_md5)
                if add_date == download_date:
                    download_url = SampleInfosec.get_download_link(session, link)
                    page_dict[file_name] = download_url
                elif add_date < download_date:
                    break
            return page_dict
        except requests.RequestException:
            return page_dict

    @staticmethod
    def get_download_link(session, link):
        try:
            response = session.get(link).text
            text = re.findall(">hXXp(.*?)<", response)[0]
            download_url = "http{}".format(re.sub("[|]]", "", text))
            return download_url
        except IndexError as e:
            print(e)
            return False
        except requests.RequestException as r:
            print(r)
            return False


def start():
    SampleMalc0de()
    SampleVxvault()
    SampleVirusBay()
    SampleMalwareTrafficAnalysis()
    SampleVirusSign()
    SampleMalshare()
    SampleInfosec()
    SampleHybrid()
    return Base().download_folder


if __name__ == "__main__":
    start()

