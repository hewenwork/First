import os
import re
import shutil
import chardet
import hashlib
import datetime
import requests
from bs4 import BeautifulSoup
from subprocess import call, check_output
base_dir = os.getcwd()
Auto_dir = r"\\192.168.1.39\f\Auto"


class Base:

    @staticmethod
    def get_list(folder_path):
        file_list = []
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            file_list.append(file_path)
        return file_list

    @staticmethod
    def get_file_md5(file_path):
        with open(file_path, "rb")as md5_file:
            md5_con = hashlib.md5()
            md5_con.update(md5_file.read())
            md5_result = str(md5_con.hexdigest())
            return md5_result

    @staticmethod
    def rename_file(file_path):
        file_md5 = Base.get_file_md5(file_path)
        file_dir = os.path.dirname(file_path)
        new_file_name = file_md5 + ".vir"
        new_file_path = os.path.join(file_dir, new_file_name)
        if new_file_path.upper() != file_path.upper():
            os.remove(file_path)
            return True
        else:
            os.rename(file_path, new_file_path)
            return True

    @staticmethod
    def move_file(resource_file, dist_dir):
        file_name = resource_file.split("/")[-1]
        new_file_path = os.path.join(dist_dir, file_name)
        if os.path.exists(new_file_path):
            return False
        else:
            shutil.move(resource_file, dist_dir)
            return True

    @staticmethod
    def get_encoding(input_str):
        try:
            encoding_result = chardet.detect(input_str)["encoding"]
        except:
            encoding_result = "utf-8"
        return encoding_result

    @staticmethod
    def switch_vpn(turn):
        check_output("chcp 437", shell=True)
        connect_status = "netstat -an"
        connect_command = "rasdial  US usa vpn2014"
        disconnect_command = "rasdial US /DISCONNECT"
        result = check_output(connect_status)
        status = bytes.decode(result)
        if turn == "on" and "1723" not in status:
            check_output(connect_command)
        elif turn == "off" and "1723" in status:
            check_output(disconnect_command)

    @staticmethod
    def get_download_folder():
        download_data = Base.get_date()
        download_folder = os.path.join(base_dir, download_data)
        if os.path.exists(download_folder) is False:
            os.makedirs(download_folder)
        return download_folder

    @staticmethod
    def get_session():
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        headers = {"User-Agent": user_agent}
        session = requests.session()
        session.headers.update(headers)
        return session

    @staticmethod
    def get_date(days=1):
        today = datetime.datetime.today()
        time_interval = datetime.timedelta(days=days)
        download_day = today - time_interval
        return download_day.strftime("%Y-%m-%d")

    @staticmethod
    def write_sample(sample_path, sample_download_url, session=None):
        if session is None:
            session = Base.get_session()
        if os.path.exists(sample_path):
            return True
        else:
            try:
                response = session.get(url=sample_download_url, stream=True)
                if response.status_code == 200:
                    with open(sample_path, "wb")as file:
                        for chunk in response.iter_content(chunk_size=1024):
                            file.write(chunk)
                    return True
                else:
                    return False
            except:
                return False

    @staticmethod
    def write_sample_md5(md5):
        download_date = Base.get_date()
        failed_fir = os.path.join(base_dir, "MD5&SHA256")
        if os.path.exists(failed_fir)is False:
            os.makedirs(failed_fir)
        sample_download_failed_log = os.path.join(failed_fir, "Failed%s.txt" % download_date)
        if os.path.exists(sample_download_failed_log):
            if len(md5) == 64:
                with open(sample_download_failed_log, "a+")as file:
                    file.write(md5 + "\n")
            else:
                with open(sample_download_failed_log, "r+")as file:
                    old_data = file.read()
                    file.seek(0, 0)
                    file.write(md5 + "\n" + old_data)
        else:
            with open(sample_download_failed_log, "a+")as file:
                file.seek(0, 0)
                file.write(md5 + "\n")

    @staticmethod
    def write_download_log(target, result):
        download_data = Base.get_date()
        log_dir = os.path.join(base_dir, "Download_Log")
        if os.path.exists(log_dir) is False:
            os.makedirs(log_dir)
        log_path = os.path.join(log_dir, r"%s.log" % download_data)
        data = "%s %s" % (target, result)
        if os.path.exists(log_path):
            with open(log_path, "r+")as file:
                old_data = file.read()
                file.seek(0, 0)
                file.write(data + "\n" + old_data)
        else:
            with open(log_path, "a+")as file:
                file.write(data + "\n")

    @staticmethod
    def start_info():
        sample_info = {}
        session = Base.get_session()
        download_date = Base.get_date()
        return sample_info, session, download_date

    @staticmethod
    def write_download_result(sample_info, target, session=None):
        failed_num = 0
        total_num = len(sample_info)
        if total_num is 0:
            result = "--has`t data"
        else:
            sample_folder = Base.get_download_folder()
            if session is None:
                session = Base.get_session()
            for file_name, download_url in sample_info.items():
                sample_md5 = file_name.split(".")[0]
                file_path = os.path.join(sample_folder, file_name)
                download_result = Base.write_sample(file_path, download_url, session=session)
                if download_result is False:
                    Base.write_sample_md5(sample_md5)
                    failed_num += 1
            result = "download result: failed-%s  total-%s" % (failed_num, total_num)
        Base.write_download_log(target, result)


class SampleMalc0de:

    @staticmethod
    def get_sample_info():
        Base.switch_vpn("on")
        sample_info, session, download_date = Base.start_info()
        url = "http://malc0de.com/database/"
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
        Base.switch_vpn("off")
        return sample_info

    @staticmethod
    def download_sample():
        sample_info = SampleMalc0de.get_sample_info()
        Base.write_download_result(sample_info, target="http://malc0de.com/database/")


class SampleVxvault:

    @staticmethod
    def get_sample_info(session, link):
        sample_response = session.get(url=link).text
        sample_md5 = re.findall("MD5:</B> (.*?)<BR>", sample_response)[0]
        file_name = sample_md5 + ".vir"
        sample_download_url = re.findall("Link:</B> (.*?)<BR>", sample_response)[0].replace("hxxp:", "http:")
        return file_name, sample_download_url

    @staticmethod
    def get_download_info():
        sample_info, session, download_date = Base.start_info()
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
        return sample_info

    @staticmethod
    def download_sample():
        sample_info = SampleVxvault().get_download_info()
        Base.write_download_result(sample_info, target="http://vxvault.net/ViriList.php")


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

    @staticmethod
    def get_info(session, num):
        sample_info = {}
        threat_level = ["malicious", "ambiguous", "suspicious", "-"]
        url = "https://www.hybrid-analysis.com/recent-submissions"
        params = {
            "filter": "file",
            "sort": "^timestamp",
            "page": num
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
        return sample_info

    @staticmethod
    def get_sample_download_url_dict(session):
        sample_dict = {}
        for page in range(1, 11):
            sample_info = SampleHybrid.get_info(session, page)
            sample_dict.update(sample_info)
        return sample_dict

    @staticmethod
    def download_sample():
        session = SampleHybrid.get_login_session()
        sample_info = SampleHybrid.get_sample_download_url_dict(session)
        Base.write_download_result(sample_info, target="https://www.hybrid-analysis.com", session=session)


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
    @staticmethod
    def get_all_download_url():
        url = "https://beta.virusbay.io/sample/data"
        session = SampleVirusBay.get_login()
        download_date = Base.get_date(1)
        recent = session.get(url=url).json()["recent"]
        sample_info = {}
        for info in recent:
            add_date = info["publishDate"][:10]
            _id = info["_id"]
            sample_md5 = info["md5"]
            file_name = sample_md5 + ".vir"
            link = "https://beta.virusbay.io/api/sample/%s/download/link" % _id
            sample_download_url = session.get(link).text
            if download_date == add_date:
                sample_info[file_name] = sample_download_url
        return sample_info

    @staticmethod
    def download_sample():
        sample_info = SampleVirusBay.get_all_download_url()
        Base.write_download_result(sample_info, target="https://beta.virusbay.io")


class SampleMalwareTrafficAnalysis:

    @staticmethod
    def get_sample_info():
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
        return sample_info

    @staticmethod
    def download_sample():
        target = "http://www.malware-traffic-analysis.net"
        sample_info = SampleMalwareTrafficAnalysis.get_sample_info()
        Base.write_download_result(sample_info, target=target)


class SampleVirusSign:

    @staticmethod
    def get_download_info(sample_info, session, download_date):
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
        return sample_info

    @staticmethod
    def download_sample():
        sample_info, session, download_date = Base.start_info()
        session.auth = ("infected", "infected")
        sample_info = SampleVirusSign.get_download_info(sample_info, session, download_date)
        Base.write_download_result(sample_info, target="http://VirusSign.com", session=session)


class SampleMalshare:

    @staticmethod
    def get_sample_info():
        sample_info, session, download_date = Base.start_info()
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
        return sample_info

    @staticmethod
    def download_sample():
        sample_info = SampleMalshare.get_sample_info()
        Base.write_download_result(sample_info, target="https://malshare.com")


class SampleInfosec:

    @staticmethod
    def get_download_link(link):
        session = Base.get_session()
        file_response = session.get(link).text
        sample_download_url = "http%s" % (re.findall(">hXXp(.*?)<", file_response)[0]).replace("]", "").replace("[", "")
        return sample_download_url

    @staticmethod
    def get_sample_dict():
        sample_info = {}
        download_date = Base.get_date(0)
        session = Base.get_session()
        stop_code = False
        for page in range(1, 10):
            if stop_code is False:
                url = "https://infosec.cert-pa.it/analyze/submission-page-%s.html" % page
                response = session.get(url)
                date_list = BeautifulSoup(response.text, "lxml").select("tr > td:nth-of-type(1)")
                md5_list = BeautifulSoup(response.text, "lxml").select("tr > td:nth-of-type(3)")
                for add_date, sample_md5 in zip(date_list, md5_list):
                    add_date = add_date.getText()[:10]
                    sample_md5 = sample_md5.getText()
                    file_name = sample_md5 + ".vir"
                    md5_url = "https://infosec.cert-pa.it/analyze/%s.html" % sample_md5
                    if add_date == download_date:
                        download_url = SampleInfosec.get_download_link(md5_url)
                        sample_info[file_name] = download_url
                    elif add_date < download_date:
                        stop_code = True
                        break
            else:
                break
        return sample_info

    @staticmethod
    def download_sample():
        sample_info = SampleInfosec.get_sample_dict()
        Base.write_download_result(sample_info, target="https://infosec.cert-pa.it")


class SampleMd5:

    @staticmethod
    def get_session():
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        headers = {"User-Agent": user_agent}
        session = requests.session()
        session.headers.update(headers)
        return session

    @staticmethod
    def get_date(days=1):
        today = datetime.datetime.today()
        time_interval = datetime.timedelta(days=days)
        download_day = today - time_interval
        return download_day.strftime("%Y-%m-%d")

    @staticmethod
    def copy_file(resource_path, dist_path):
        command = "copy \"%s\" \"%s\"" % (resource_path, dist_path)
        os.system(command)

    @staticmethod
    def write_md5(md5):
        download_date = SampleMd5.get_date()
        md5_file_path = os.path.join(base_dir, r"Auto%s.txt" % download_date)
        if os.path.exists(md5_file_path):
            with open(md5_file_path, "r+")as file:
                old_data = file.read()
                file.seek(0, 0)
                file.write(md5 + "\n" + old_data)
        else:
            with open(md5_file_path, "a+")as file:
                file.seek(0, 0)
                file.write(md5 + "\n")
        return md5_file_path

    @staticmethod
    def md5_hybrid():
        md5_dict = {}
        headers = {"User-Agent": "Falcon Sandbox"}
        session = requests.session()
        session.headers.update(headers)
        url = "https://www.hybrid-analysis.com/feed?json"
        response = session.get(url).json()
        for info in response["data"]:
            md5_dict[info["md5"]] = ""
        return md5_dict

    @staticmethod
    def md5_virussign():
        md5_dict = {}
        download_date = SampleMd5.get_date(1)
        session = SampleMd5.get_session()
        session.auth = ("infected", "infected")
        url = "http://virusign.com/get_hashlist.php"
        params = {
            "md5": "",
            "n": "ANY",
            "start_date": download_date,
            "end_date": download_date
        }
        response = session.get(url, params=params).text
        for md5 in response.split("\n"):
            md5 = md5.replace("\"", "")
            md5_dict[md5] = ""
        return md5_dict

    @staticmethod
    def md5_virusshare():
        url = "https://virusshare.com/hashes/VirusShare_00357.md5"

    @staticmethod
    def get_all_md5():
        download_date = SampleMd5.get_date()
        md5_file_path = os.path.join(base_dir, r"%s.txt" % download_date)
        md5_dict = {**SampleMd5.md5_virussign(), **SampleMd5.md5_hybrid()}
        with open(md5_file_path, "a+")as file:
            for md5 in md5_dict:
                file.write(md5 + "\n")
        SampleMd5.copy_file(md5_file_path, Auto_dir)


class Compression:

    @staticmethod
    def decompression_7z(file_path):
        password = "infected"
        local_7z_path = r"C:\Program Files\7-Zip"
        os.chdir(local_7z_path)
        dir_path = os.path.dirname(file_path)
        file_type = file_path[-3:]
        command_dict = {
            ".gz": "7z e -tgzip -pinfected -y \"%s\" -o\"%s\"" % (file_path, dir_path),
            "zip": "7z e -tzip -pinfected -y \"%s\" -o\"%s\"" % (file_path, dir_path),
            ".7z": "7z e -t7z -pinfected -y \"%s\" -o\"%s\"" % (file_path, dir_path),
        }
        try:
            call(command_dict[file_type], shell=True)
            return True
        except:
            return False

    @staticmethod
    def decompression_rar(file_path, password="infected"):
        local_rar_path = r"C:\Program Files\WinRAR"
        os.chdir(local_rar_path)
        dir_path = os.path.dirname(file_path)
        command = "rar e -p%s -y \"%s\" \"%s\"" % (password, file_path, dir_path)
        try:
            call(command)
            return True
        except:
            return False

    @staticmethod
    def compression(file_path, password="infected"):
        local_rar_path = r"C:\Program Files\WinRAR"
        os.chdir(local_rar_path)
        result_path = file_path + "[infected].rar"
        command = "rar a -ep -p%s \"%s\" \"%s\"" % (password, result_path, file_path)
        try:
            call(command, shell=True)
            return result_path
        except:
            return False


class FinallyDo:

    @staticmethod
    def de(folder_path):
        path_list = Base.get_list(folder_path)
        type_7z = [".gz", "zip", ".7z"]
        type_rar = ["rar"]
        for file_path in path_list:
            if file_path[-3:] in type_7z:
                result = Compression.decompression_7z(file_path)
                if result:
                    os.remove(file_path)
                else:
                    Base.move_file(file_path)
            elif file_path[-3:] in type_rar:
                result = Compression.decompression_rar(file_path)
                if result:
                    os.remove(file_path)
                else:
                    Base.move_file(file_path)
        path_list_new = Base.get_list(folder_path)
        for file_path in path_list_new:
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                if file_path[-3:] in type_7z:
                    result = Compression.decompression_7z(file_path)
                    if result:
                        os.remove(file_path)
                    else:
                        Base.move_file(file_path)
                elif file_path[-3:] in type_rar:
                    result = Compression.decompression_rar(file_path)
                    if result:
                        os.remove(file_path)
                    else:
                        Base.move_file(file_path)

    @staticmethod
    def rename(folder_path):
        path_list = Base.get_list(folder_path)
        for file_path in path_list:
            result = Base.rename_file(file_path)
            if result is False:
                os.remove(file_path)

    @staticmethod
    def copy_comp(folder_path):
        result_path = Compression.compression(folder_path)
        os.system("copy \"%s\" \"%s\"" % (result_path, Auto_dir))

    @staticmethod
    def s(folder_path):
        FinallyDo.de(folder_path)
        FinallyDo.rename(folder_path)
        FinallyDo.copy_comp(folder_path)





