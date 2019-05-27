import os
import re
import datetime
import requests
from bs4 import BeautifulSoup
from subprocess import check_output
# base_dir = os.getcwd()
base_dir = r"C:\Users\hewen\Desktop\MyTest"


class Base:

    @staticmethod
    def get_date(days=1):
        today = datetime.datetime.today()
        time_interval = datetime.timedelta(days=days)
        download_day = today - time_interval
        return download_day.strftime("%Y-%m-%d")

    @staticmethod
    def get_download_folder():
        download_data = Base.get_date()
        download_folder = os.path.join(base_dir, download_data)
        if os.path.exists(download_folder) is False:
            os.makedirs(download_folder)
        return download_folder

    @staticmethod
    def get_download_failed_path():
        download_data = Base.get_date()
        failed_dir = os.path.join(base_dir, r"MD5&SHA256")
        failed_path = os.path.join(failed_dir, "Failed{}.txt".format(download_data))
        if os.path.exists(failed_dir) is False:
            os.makedirs(failed_dir)
        return failed_path

    @staticmethod
    def get_download_log_path():
        download_data = Base.get_date()
        log_dir = os.path.join(base_dir, r"Log")
        log_path = os.path.join(log_dir, "Download{}.log".format(download_data))
        if os.path.exists(log_dir) is False:
            os.makedirs(log_dir)
        return log_path

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
                response = session.get(url=sample_download_url, stream=True)
            except requests.RequestException:
                return False
            with open(sample_path, "wb")as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            return True

    @staticmethod
    def write_sample_md5(file_path, md5):
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
                    Base.write_sample_md5(file_path=failed_path, md5=sample_md5)
            result = "{0} -- Failed:{1}  Total:{2}".format(target, failed_num, total_num)
        Base.write_download_log(log_path, result)


class SampleMalc0de:

    def __init__(self):
        download_date = Base.get_date()
        sample_info, session, download_folder, failed_path, log_path = Base.start_info()
        url = "http://malc0de.com/database/"
        if self.switch_vpn("on"):
            response = session.get(url)
            if response.status_code == 200:
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
            self.switch_vpn("off")
        Base.start_download(sample_info, session, url, download_folder, failed_path, log_path)

    @staticmethod
    def switch_vpn(turn):
        # connect_status = "netstat -an"
        connect_command = "rasdial  US usa vpn2014"
        disconnect_command = "rasdial US /DISCONNECT"
        command_dict = {
            "on": connect_command,
            "off": disconnect_command
        }
        try:
            check_output("chcp 437", shell=True)
            check_output(command_dict[turn], shell=True)
            return True
        except:
            return False


class SampleVxvault:

    @staticmethod
    def get_sample_info(session, link):
        sample_response = session.get(url=link).text
        sample_md5 = re.findall("MD5:</B> (.*?)<BR>", sample_response)[0]
        file_name = sample_md5 + ".vir"
        sample_download_url = re.findall("Link:</B> (.*?)<BR>", sample_response)[0].replace("hxxp:", "http:")
        return file_name, sample_download_url

    def __init__(self):
        download_date = Base.get_date()
        sample_info, session, download_folder, failed_path, log_path = Base.start_info()
        url = "http://vxvault.net/ViriList.php"
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
        Base.start_download(sample_info, session, url, download_folder, failed_path, log_path)


class SampleHybrid:

    @staticmethod
    def get_login_session():
        headers = {"User-Agent":  "Falcon Sandbox"}
        session = requests.session()
        session.headers.update(headers)
        url = "https://www.hybrid-analysis.com/login"
        response = session.get(url)
        if response.status_code == 200:
            token = re.findall("name=\"token\" value=\"(.*?)\">", response.text)[0]
            data = {
                "email": "cicely@iobit.com",
                "password": "IObit2018",
                "token": token
            }
            session.post(url, data=data)
            return session
        else:
            return False

    def __init__(self):
        sample_info, session, download_folder, failed_path, log_path = Base.start_info()
        session = SampleHybrid.get_login_session()
        threat_level = ["malicious", "ambiguous", "suspicious", "-"]
        url = "https://www.hybrid-analysis.com/recent-submissions"
        for page in range(1, 11):
            params = {
                "filter": "file",
                "sort": "^timestamp",
                "page": page
            }
            response = session.get(url, params=params)
            suop = BeautifulSoup(response.text, "lxml")
            sample_date_list = suop.select("td.submission-timestamp.hidden-xs")
            sample_download_list = suop.select("a.btn.btn-default.btn-xs.pull-right.sampledl.download-url")
            is_virus_list = suop.select("dd:nth-of-type(3)")
            for sample_date, sample_download_url, is_virus in zip(sample_date_list, sample_download_list, is_virus_list):
                # sample_date = sample_date.getText().strip().split(",")[0]
                sample_sha256 = sample_download_url.get("href").split("?")[0][17:]
                file_name = sample_sha256 + ".gz"
                sample_download_url = "https://www.hybrid-analysis.com%s" % sample_download_url.get("href")
                is_virus = is_virus.getText().strip()
                if is_virus in threat_level:
                    sample_info[file_name] = sample_download_url
        Base.start_download(sample_info, session, url, download_folder, failed_path, log_path)


class SampleVirusBay:

    # 取登陆信息
    @staticmethod
    def get_login():
        url = "https://beta.virusbay.io/login"
        data = {"email": "niwangxiu@gmail.com",
                "password": "testvirus0504L"}
        session = Base.get_session()
        response = session.post(url=url, data=data)
        token = response.json()["token"]
        authorization = {"Authorization": "JWT %s" % token}
        session.headers.update(authorization)
        return session

    # 取下载MD5和下载链接字典
    def __init__(self):
        url = "https://beta.virusbay.io/sample/data"
        download_date = Base.get_date()
        sample_info, session, download_folder, failed_path, log_path = Base.start_info()
        session = SampleVirusBay.get_login()
        recent = session.get(url=url).json()["recent"]
        for info in recent:
            add_date = info["publishDate"][:10]
            _id = info["_id"]
            sample_md5 = info["md5"]
            file_name = sample_md5 + ".vir"
            link = "https://beta.virusbay.io/api/sample/%s/download/link" % _id
            sample_download_url = session.get(link).text
            if download_date == add_date:
                sample_info[file_name] = sample_download_url
        Base.start_download(sample_info, session, url, download_folder, failed_path, log_path)


class SampleMalwareTrafficAnalysis:

    def __init__(self):
        download_date = Base.get_date()
        sample_info, session, download_folder, failed_path, log_path = Base.start_info()
        download_date = download_date.replace("-", "/")
        url = "http://www.malware-traffic-analysis.net/%s/index.html" % download_date
        if session.get(url).status_code == 200:
            sample_suop = BeautifulSoup(session.get(url).text, "lxml").select("ul > li > a")
            for download_url in sample_suop:
                if "-malware" in download_url.get("href"):
                    sample_name = download_url.get("href")
                    sample_download_url = url.replace("index.html", sample_name)
                    sample_info[sample_name] = sample_download_url
        Base.start_download(sample_info, session, url, download_folder, failed_path, log_path)


class SampleVirusSign:

    def __init__(self):
        download_date = Base.get_date()
        sample_info, session, download_folder, failed_path, log_path = Base.start_info()
        session.auth = ("infected", "infected")
        url = "http://virusign.com/get_hashlist.php"
        params = {
            "sha256": "",
            "n": "ANY",
            "start_date": download_date,
            "end_date": download_date
        }
        response = session.get(url, params=params).text
        for sha256 in response.split("\n"):
            sha256 = sha256.replace("\"", "")
            file_name = sha256 + ".7z"
            sample_download_url = "http://virusign.com/file/%s" % file_name
            sample_info[file_name] = sample_download_url
        Base.start_download(sample_info, session, url, download_folder, failed_path, log_path)


class SampleMalshare:

    def __init__(self):
        sample_info, session, download_folder, failed_path, log_path = Base.start_info()
        api_key = "1f36742f1f87e778ae1d4c370157581d746a4613fca10690f20949154b86589a"
        url = "https://malshare.com/api.php"
        params = {
            "api_key": api_key,
            "action": "getlist"
        }
        response = session.get(url=url, params=params).json()
        for sample in response:
            sample_md5 = sample["md5"]
            file_name = sample_md5 + ".vir"
            download_url = url + "?api_key=%s&action=getfile&hash=%s" % (api_key, sample_md5)
            sample_info[file_name] = download_url
        Base.start_download(sample_info, session, url, download_folder, failed_path, log_path)


class SampleInfosec:

    @staticmethod
    def get_download_link(session, link):
        file_response = session.get(link).text
        sample_download_url = "http{}".format(re.findall(">hXXp(.*?)<", file_response)[0]).replace("]", "").replace("[", "")
        return sample_download_url

    def __init__(self):
        url = "https://infosec.cert-pa.it/"
        download_date = Base.get_date()
        sample_info, session, download_folder, failed_path, log_path = Base.start_info()
        for page in range(1, 10):
            base_url = "https://infosec.cert-pa.it/analyze/submission-page-%s.html" % page
            response = session.get(base_url)
            date_list = BeautifulSoup(response.text, "lxml").select("tr > td:nth-of-type(1)")
            md5_list = BeautifulSoup(response.text, "lxml").select("tr > td:nth-of-type(3)")
            for add_date, sample_md5 in zip(date_list, md5_list):
                add_date = add_date.getText()[:10]
                sample_md5 = sample_md5.getText()
                file_name = sample_md5 + ".vir"
                md5_url = "https://infosec.cert-pa.it/analyze/%s.html" % sample_md5
                if add_date == download_date:
                    download_url = SampleInfosec.get_download_link(session, md5_url)
                    sample_info[file_name] = download_url
                elif add_date < download_date:
                    break
        else:
            pass
        Base.start_download(sample_info, session, url, download_folder, failed_path, log_path)


if __name__ == "__main__":
    # SampleMalc0de()
    # SampleVxvault()
    # SampleHybrid()
    # SampleVirusBay()
    # SampleMalwareTrafficAnalysis()
    # SampleVirusSign()
    # SampleMalshare()
    SampleInfosec()

