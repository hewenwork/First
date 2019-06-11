import os
import re
import shutil
import hashlib
import datetime
import requests
from bs4 import BeautifulSoup
from contextlib import closing
from subprocess import check_output, SubprocessError


class Base:

    @staticmethod
    def get_date(days):
        today = datetime.datetime.today()
        time_interval = datetime.timedelta(days=days)
        download_day = today - time_interval
        return download_day

    @staticmethod
    def get_path_folder(folder_path):
        if os.path.exists(folder_path) is False:
            os.makedirs(folder_path)
        return folder_path

    @staticmethod
    def get_path_file(file_path):
        if os.path.exists(file_path):
            return file_path
        else:
            dir_path = os.path.dirname(file_path)
            if os.path.exists(dir_path):
                os.makedirs(dir_path)
            with open(file_path, "a+", encoding="utf-8")as file:
                file.write()
            return file_path

    @staticmethod
    def get_session():
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        headers = {"User-Agent": user_agent}
        session = requests.session()
        session.headers.update(headers)
        return session

    @staticmethod
    def write_sample(sample_path, sample_download_url, session):
        if os.path.exists(sample_path)is False:
            try:
                with closing(session.get(url=sample_download_url, stream=True))as response, \
                        open(sample_path, "wb")as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)
                return True
            except requests.RequestException:
                return False
            except OSError:
                return False
        else:
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
                file.write(md5 + "\n")

    @staticmethod
    def write_download_log(file_path, log):
        if os.path.exists(file_path):
            with open(file_path, "r+")as file:
                old_data = file.read()
                file.seek(0, 0)
                file.write(log + "\n" + old_data)
        else:
            with open(file_path, "a+")as file:
                file.write(log + "\n")

    @staticmethod
    def start_download(sample_info, session, url, download_folder, failed_path, log_path):
        failed_num = 0
        total_num = len(sample_info)
        if total_num is 0:
            result = "{}--has`t data".format(url)
        else:
            for file_name, download_url in sample_info.items():
                sample_md5 = file_name.split(".")[0]
                file_path = os.path.join(download_folder, file_name)
                download_result = Base.write_sample(file_path, download_url, session)
                if download_result is False:
                    failed_num += 1
                    Base.write_sample_md5(file_path=failed_path, md5=sample_md5)
                print("\r{}".format(url), end="")
            result = "{0} -- Failed:{1}  Total:{2}".format(url, failed_num, total_num)
        Base.write_download_log(log_path, result)

    @staticmethod
    def get_list(folder_path):
        file_list = []
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            file_list.append(file_path)
        return file_list

    @staticmethod
    def get_file_md5(file_path):
        try:
            with open(file_path, "rb")as file:
                md5_con = hashlib.md5()
                md5_con.update(file.read())
                md5_result = str(md5_con.hexdigest())
                return md5_result
        except OSError:
            return False

    @staticmethod
    def rename_file(file_path):
        file_md5 = Base.get_file_md5(file_path)
        file_dir = os.path.dirname(file_path)
        new_file_name = file_md5 + ".vir"
        new_file_path = os.path.join(file_dir, new_file_name)
        try:
            shutil.move(file_path, new_file_path)
        except PermissionError:
            os.remove(file_path)


class Init:

    def __init__(self):
        self.start_info()

    @staticmethod
    def start_info():
        sample_info = {}
        base_dir = os.getcwd()
        session = Base.get_session()
        download_date = Base.get_date().strftime("%Y-%m-%d")
        path_folder_download = os.path.join(base_dir, download_date)
        path_file_log = os.path.join(base_dir, r"Log\{}.log".format(download_date))
        Base.get_file_path(path_file_log)
        path_file_sign = os.path.join(base_dir, r"MD5&SHA256\Failed{}.txt".format(download_date))
        Base.get_file_path(path_file_sign)
        return sample_info, session, download_date, path_folder_download, path_file_sign, path_file_log


class SampleMalc0de:

    def __init__(self):
        self.switch_vpn("on")
        url = "http://malc0de.com/database/"
        sample_info, session, download_date, path_folder_download, path_file_sign, path_file_log = Init()
        try:
            response = session.get(url)
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
            Base.start_download(sample_info, session, url, download_folder, download_failed_path, download_log_path)
        except requests.RequestException:
            Base.write_download_log(download_log_path, "VPN Error")
        self.switch_vpn("off")

    @staticmethod
    def switch_vpn(turn):
        connect_command = "rasdial  US usa vpn2014"
        disconnect_command = "rasdial US /DISCONNECT"
        command_dict = {
            "on": connect_command,
            "off": disconnect_command
        }
        try:
            check_output(command_dict[turn], shell=True)
            return True
        except SubprocessError:
            return False


class SampleVxvault:

    def __init__(self):
        url = "http://vxvault.net/ViriList.php"
        download_date, sample_info, session, download_folder, download_failed_path, download_log_path = Base.start_info()
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
            Base.start_download(sample_info, session, url, download_folder, download_failed_path, download_log_path)
        except requests.RequestException:
            Base.write_download_log(download_log_path, url + "Connect Error")

    @staticmethod
    def get_sample_info(session, link):
        sample_response = session.get(url=link).text
        sample_md5 = re.findall("MD5:</B> (.*?)<BR>", sample_response)[0]
        file_name = sample_md5 + ".vir"
        sample_download_url = re.findall("Link:</B> (.*?)<BR>", sample_response)[0].replace("hxxp:", "http:")
        return file_name, sample_download_url


class SampleHybrid:

    def __init__(self):
        url = "https://www.hybrid-analysis.com/recent-submissions"
        download_date, sample_info, session, download_folder, download_failed_path, download_log_path = Base.start_info()
        session = SampleHybrid.get_login_session()
        if session:
            for page in range(1, 11):
                sample_info.update(SampleHybrid.get_page_info(session, url, page))
            Base.start_download(sample_info, session, url, download_folder, download_failed_path, download_log_path)
        else:
            Base.write_download_log(download_log_path, url + "login Error")

    @staticmethod
    def get_login_session():
        session = requests.session()
        session.headers["User-Agent"] = "Falcon Sandbox"
        url = "https://www.hybrid-analysis.com/login"
        try:
            response = session.get(url).text
            token = re.findall("name=\"token\" value=\"(.*?)\">", response)[0]
            data = {
                "email": "cicely@iobit.com",
                "password": "IObit2018",
                "token": token
            }
            session.post(url, data=data)
            return session

        except requests.RequestException:
            return False

    @staticmethod
    def get_page_info(session, url, page):
        page_dict = {}
        threat_level = ["malicious", "ambiguous", "suspicious", "-"]
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
        for sample_date, sample_download_url, is_virus in zip(sample_date_list, sample_download_list,
                                                              is_virus_list):
            sample_sha256 = sample_download_url.get("href").split("?")[0][17:]
            file_name = sample_sha256 + ".gz"
            sample_download_url = "https://www.hybrid-analysis.com%s" % sample_download_url.get("href")
            is_virus = is_virus.getText().strip()
            if is_virus in threat_level:
                page_dict[file_name] = sample_download_url
        return page_dict


class SampleVirusBay:

    def __init__(self):
        url = "https://beta.virusbay.io/sample/data"
        download_date, sample_info, session, download_folder, download_failed_path, download_log_path = Base.start_info()
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
                if download_date == add_date:
                    sample_info[file_name] = sample_download_url
            session = Base.get_session()
            Base.start_download(sample_info, session, url, download_folder, download_failed_path, download_log_path)
        else:
            Base.write_download_log(download_log_path, url + "Login Error")

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
        except requests.RequestException:
            return False


class SampleMalwareTrafficAnalysis:

    def __init__(self):
        download_date, sample_info, session, download_folder, download_failed_path, download_log_path = Base.start_info()
        download_date = download_date.replace("-", "/")
        url = "http://www.malware-traffic-analysis.net/%s/index.html" % download_date
        if session.get(url).status_code == 200:
            sample_suop = BeautifulSoup(session.get(url).text, "lxml").select("ul > li > a")
            for download_url in sample_suop:
                if "-malware" in download_url.get("href"):
                    sample_name = download_url.get("href")
                    sample_download_url = url.replace("index.html", sample_name)
                    sample_info[sample_name] = sample_download_url
            Base.start_download(sample_info, session, url, download_folder, download_failed_path, download_log_path)
        else:
            Base.write_download_log(download_log_path, url + "--has`t data")


class SampleVirusSign:

    def __init__(self):
        url = "http://virusign.com/get_hashlist.php"
        download_date, sample_info, session, download_folder, download_failed_path, download_log_path = Base.start_info()
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
            Base.start_download(sample_info, session, url, download_folder, download_failed_path, download_log_path)
        else:
            Base.write_download_log(download_log_path, url + "--has`t data")


class SampleMalshare:

    def __init__(self):
        url = "https://malshare.com/api.php"
        download_date, sample_info, session, download_folder, download_failed_path, download_log_path = Base.start_info()
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
            Base.start_download(sample_info, session, url, download_folder, download_failed_path, download_log_path)
        except requests.RequestException:
            Base.write_download_log(download_log_path, url + "Error")


class SampleInfosec:

    def __init__(self):
        url = "https://infosec.cert-pa.it/"
        download_date, sample_info, session, download_folder, download_failed_path, download_log_path = Base.start_info()
        try:
            for page in range(1, 10):
                sample_info.update(SampleInfosec.get_page_info(download_date, session, page))
            Base.start_download(sample_info, session, url, download_folder, download_failed_path, download_log_path)
        except requests.RequestException:
            Base.write_download_log(download_log_path, url + "Error")

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
        response = session.get(link).text
        text = re.findall(">hXXp(.*?)<", response)[0]
        download_url = "http{}".format(re.sub("[|]]", "", text))
        return download_url


class DownloadSample:

    @staticmethod
    def init():
        SampleMalc0de()
        SampleVxvault()
        SampleHybrid()
        SampleVirusBay()
        SampleMalwareTrafficAnalysis()
        SampleVirusSign()
        SampleMalshare()
        SampleInfosec()
        return Base.get_download_folder()


class Compression:

    def __init__(self):
        self.path_rar = r"C:\Program Files\WinRAR"
        self.path_7z = r"C:\Program Files\7-Zip"

    @staticmethod
    def de_7z(file_path, password="infected"):
        os.chdir(Compression().path_7z)
        dir_path = os.path.dirname(file_path)
        command_dict = {
            ".gz": "7z e -tgzip -p%s -y \"%s\" -o\"%s\"" % (password, file_path, dir_path),
            "zip": "7z e -tzip -p%s -y \"%s\" -o\"%s\"" % (password, file_path, dir_path),
            ".7z": "7z e -t7z -p%s -y \"%s\" -o\"%s\"" % (password, file_path, dir_path),
        }
        file_type = file_path[-3:]
        command = command_dict[file_type]
        try:
            check_output(command, shell=True)
            return True
        except SubprocessError:
            return False

    @staticmethod
    def de_rar(file_path, password="infected"):
        os.chdir(Compression().path_rar)
        dir_path = os.path.dirname(file_path)
        command = "rar e -p%s -y \"%s\" \"%s\"" % (password, file_path, dir_path)
        try:
            check_output(command)
            return True
        except SubprocessError:
            return False

    @staticmethod
    def co_rar(file_path, password="infected"):
        os.chdir(Compression().path_rar)
        result_path = file_path + "[infected].rar"
        command = "rar a -ep -p%s \"%s\" \"%s\"" % (password, result_path, file_path)
        try:
            check_output(command, shell=True)
            return result_path
        except SubprocessError:
            return False

    @staticmethod
    def auto_de(file_path):
        file_dir = os.path.dirname(file_path)
        dist_dir = os.path.join(os.path.dirname(file_dir), r"处理失败")
        if os.path.exists(dist_dir)is False:
            os.makedirs(dist_dir)
        if file_path[-3:] in [".gz", ".7z", "zip"]:
            if Compression.de_7z(file_path):
                os.remove(file_path)
            else:
                try:
                    shutil.move(file_path, dist_dir)
                except PermissionError:
                    os.remove(file_path)
        elif file_path[-3:] == "rar":
            if Compression.de_rar(file_path):
                os.remove(file_path)
            else:
                try:
                    shutil.move(file_path, dist_dir)
                except PermissionError:
                    os.remove(file_path)
        else:
            return True


class Auto:

    def __init__(self):
        dist_dir = r"\\192.168.1.39\f\Auto"
        # folder_path = DownloadSample.init()
        folder_path = input(u"fk")
        list(map(Compression.auto_de, Base.get_list(folder_path)))
        list(map(Base.rename_file, Base.get_list(folder_path)))
        result_path = Compression.co_rar(folder_path)
        try:
            command = "copy \"{}\" \"{}\"".format(result_path, dist_dir)
            check_output(command, shell=True)
        except SubprocessError:
            Base.write_download_log(os.path.join(base_dir, "Copy_log.log"), "Copy_Failed")


if __name__ == "__main__":
    Auto()
    # start_date = input(u"Set the start time like 080000\n")
    # while True:
    #     now_date = datetime.datetime.now().strftime("%H%M%S")
    #     if now_date == start_date:
    #         print("start download")
    #         Auto()
    #         today_date = datetime.datetime.today().date()
    #         print("\r{}\ndownload over, wait for next time".format(today_date), end="")
