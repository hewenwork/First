import os
import re
import shutil
import hashlib
import datetime
import requests
from bs4 import BeautifulSoup

# base_dir = os.getcwd()
base_dir = r"C:\Users\hewen\Desktop\20190526\aa"
sample_copy_folder = r"\\192.168.1.39\f\Auto"


class Base:

    @staticmethod
    def move_file(resource_file):
        dist_dir = os.path.join(base_dir, "解压失败")
        file_name = resource_file.split("/")[-1]
        new_file_path = os.path.join(dist_dir, file_name)
        if os.path.exists(new_file_path):
            os.remove(resource_file)
        else:
            shutil.move(resource_file, dist_dir)

    @staticmethod
    def get_sample_folder():
        download_data = Base.get_date()
        sample_folder = os.path.join(base_dir, download_data)
        if os.path.exists(sample_folder) is False:
            os.makedirs(sample_folder)
        return sample_folder

    @staticmethod
    def get_session():
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        headers = {"User-Agent": user_agent}
        session = requests.session()
        session.headers.update(headers)
        return session

    @staticmethod
    def get_file_md5(file_path):
        try:
            with open(file_path, "rb")as md5_file:
                md5_con = hashlib.md5()
                md5_con.update(md5_file.read())
                md5_result = str(md5_con.hexdigest())
                return md5_result.upper()
        except OSError:
            return False

    @staticmethod
    def get_list(folder_path):
        file_list = []
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            file_list.append(file_path)
        return file_list

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
    def switch_vpn():
        os.system("chcp 437")
        connect_status = "netstat -an"
        connect_command = "rasdial  US usa vpn2014"
        disconnect_command = "rasdial US /DISCONNECT"
        result = os.popen(connect_status).read()
        if "1723" in result:
            os.popen(disconnect_command).read()
        else:
            os.popen(connect_command).read()

    @staticmethod
    def copy_file(resource_path, dist_path):
        command = "copy \"%s\" \"%s\"" % (resource_path, dist_path)
        os.system(command)

    @staticmethod
    def write_md5(md5):
        download_date = Base.get_date()
        md5_file_path = os.path.join(base_dir, r"md5_info\%s.txt" % download_date)
        if os.path.exists(md5_file_path):
            with open(md5_file_path, "r+")as file:
                old_data = file.read()
                file.seek(0, 0)
                file.write(md5 + "\n" + old_data)
        else:
            with open(md5_file_path, "a+")as file:
                file.seek(0, 0)
                file.write(md5 + "\n")

    @staticmethod
    def write_download_log(target, result):
        download_data = Base.get_date()
        data = "%s %s %s" % (download_data, target, result)
        log_path = os.path.join(base_dir, "download_log.txt")
        if os.path.exists(log_path):
            with open(log_path, "r+")as file:
                old_data = file.read()
                file.seek(0, 0)
                file.write(data + "\n" + old_data)
        else:
            with open(log_path, "a+")as file:
                file.write(data + "\n")

    @staticmethod
    def decompression(file_path):
        local_rar_path = r"C:\Program Files\WinRAR"
        local_7z_path = r"C:\Program Files\7-Zip"
        password = "infected"
        dir_path = os.path.dirname(file_path)
        command_dict = {
            ".gz": [local_7z_path, "7z e -tgzip -p%s -y \"%s\" -o%s" % (password, file_path, dir_path)],
            "zip": [local_7z_path, "7z e -tzip -p%s -y \"%s\" -o%s" % (password, file_path, dir_path)],
            ".7z": [local_7z_path, "7z e -t7z -p%s -y \"%s\" -o%s" % (password, file_path, dir_path)],
            "rar": [local_rar_path, "rar e -p%s -y \"%s\" %s" % (password, file_path, dir_path)]
        }
        file_type = file_path[-3:]
        if file_type in command_dict.keys():
            compression_path = command_dict[file_type][0]
            command = command_dict[file_type][-1]
            os.chdir(compression_path)
            try:
                result = os.popen(command).read()
                if "OK" in result.upper():
                    os.remove(file_path)
                    return True
                else:
                    return False
            except:
                return False
        else:
            return True

    @staticmethod
    def compression(file_path):
        password = "infected"
        result_path = file_path + "[infected].rar"
        local_rar_path = r"C:\Program Files\WinRAR"
        command = "rar a -ep -p%s %s %s" % (password, result_path, file_path)
        os.chdir(local_rar_path)
        try:
            result = os.popen(command).read()
            if "OK" in result.upper():
                return result_path
            else:
                return False
        except:
            return False

    @staticmethod
    def rename(file_path):
        file_md5 = Base.get_file_md5(file_path)
        new_file_path = os.path.join(os.path.dirname(file_path), file_md5 + ".vir")
        if new_file_path == file_path:
            if os.path.exists(new_file_path):
                return True
        else:
            os.renames(file_path, new_file_path)


class SampleMalc0de:

    @staticmethod
    def get_sample_info():
        sample_info = {}
        session = Base.get_session()
        download_date = Base.get_date(1)
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
                sample_url = "http://" + sample_url.getText()
                if add_date == download_date:
                    sample_info[sample_md5] = sample_url
            return sample_info
        else:
            return False

    @staticmethod
    def download_sample():
        Base.switch_vpn()
        sample_info = SampleMalc0de.get_sample_info()
        Base.switch_vpn()
        if sample_info is False:
            Base.write_download_log("http://malc0de.com/database/", "--has`t sample")
        else:
            failed_num = 0
            total_num = len(sample_info)
            sample_folder = Base.get_sample_folder()
            for md5, download_url in sample_info.items():
                file_path = os.path.join(sample_folder, md5 + ".vir")
                download_result = Base.write_sample(file_path, download_url)
                if download_result is False:
                    Base.write_md5(md5)
                    failed_num += 1
            result = "download result: failed-%s  total-%s" % (failed_num, total_num)
            Base.write_download_log("http://malc0de.com/database/", result)


class SampleVxvault:

    @staticmethod
    def get_sample_info(session, link):
        sample_response = session.get(url=link).text
        sample_md5 = re.findall("MD5:<\\/B> (.*?)<BR>", sample_response)[0]
        sample_download_url = re.findall("Link:<\\/B> (.*?)<BR>", sample_response)[0].replace("hxxp:", "http:")
        return sample_md5, sample_download_url

    @staticmethod
    def get_download_info():
        sample_info = {}
        download_date = Base.get_date()
        session = Base.get_session()
        url = "http://vxvault.net/ViriList.php"
        response = session.get(url=url)
        suop = BeautifulSoup(response.text, "lxml")
        suop_add_date = suop.select("tr > td:nth-of-type(1) > a")
        suop_url = suop.select("tr > td:nth-of-type(2) > a:nth-of-type(2)")
        for add_date, link in zip(suop_add_date, suop_url):
            add_date = add_date.getText()
            link = "http://vxvault.net/" + link.get("href")
            if add_date == download_date[5:]:
                sample_md5, sample_download_url = SampleVxvault.get_sample_info(session, link)
                sample_info[sample_md5] = sample_download_url
            elif add_date < download_date[5:]:
                break
        return sample_info

    @staticmethod
    def download_sample():
        sample_info = SampleVxvault().get_download_info()
        if sample_info == {}:
            Base.write_download_log("http://vxvault.net/ViriList.php", "--has`t sample")
        else:
            failed_num = 0
            total_num = len(sample_info)
            sample_folder = Base.get_sample_folder()
            for md5, download_url in sample_info.items():
                file_path = os.path.join(sample_folder, md5 + ".vir")
                download_result = Base.write_sample(file_path, download_url)
                if download_result is False:
                    failed_num += 1
                else:
                    Base.write_md5(md5)
            result = "download result: failed-%s  total-%s" % (failed_num, total_num)
            Base.write_download_log("http://vxvault.net/ViriList.php", result)


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
            sample_download_url = "https://www.hybrid-analysis.com%s" % sample_download_url.get("href")
            is_virus = is_virus.getText().strip()
            if is_virus in threat_level:
                sample_info[sample_sha256] = sample_download_url
        return sample_info

    @staticmethod
    def get_sample_download_url_dict():
        sample_dict = {}
        session = SampleHybrid.get_login_session()
        for page in range(1, 11):
            sample_info = SampleHybrid.get_info(session, page)
            sample_dict.update(sample_info)
        return sample_dict

    @staticmethod
    def download_sample():
        sample_dict = SampleHybrid.get_sample_download_url_dict()
        failed_num = 0
        total_num = len(sample_dict)
        session = SampleHybrid.get_login_session()
        sample_folder = Base.get_sample_folder()
        for sha256, download_url in sample_dict.items():
            file_path = os.path.join(sample_folder, sha256 + ".vir.gz")
            download_result = Base.write_sample(file_path, download_url, session=session)
            if download_result is False:
                failed_num += 1
                Base.write_md5(sha256)
        result = "download result: failed-%s  total-%s" % (failed_num, total_num)
        Base.write_download_log("https://www.hybrid-analysis.com", result)


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
            link = "https://beta.virusbay.io/api/sample/%s/download/link" % _id
            sample_download_url = session.get(link).text
            if download_date == add_date:
                sample_info[sample_md5] = sample_download_url
        return sample_info

    @staticmethod
    def download_sample():
        sample_info = SampleVirusBay.get_all_download_url()
        if sample_info == {}:
            Base.write_download_log("https://beta.virusbay.io", "--has`t sample")
        else:
            failed_num = 0
            total_num = len(sample_info)
            sample_folder = Base.get_sample_folder()
            for md5, download_url in sample_info.items():
                file_path = os.path.join(sample_folder, md5 + ".vir")
                download_result = Base.write_sample(file_path, download_url)
                if download_result is False:
                    failed_num += 1
                    Base.write_md5(md5)
            result = "download result: failed-%s  total-%s" % (failed_num, total_num)
            Base.write_download_log("https://beta.virusbay.io", result)


class SampleMalwareTrafficAnalysis:

    @staticmethod
    def get_sample_info():
        sample_info = {}
        session = Base.get_session()
        download_date = Base.get_date(9).replace("-", "/")
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
        sample_info = SampleMalwareTrafficAnalysis.get_sample_info()
        if sample_info == {}:
            Base.write_download_log("http://www.malware-traffic-analysis.net", "--has`t sample")
        else:
            failed_num = 0
            total_num = len(sample_info)
            sample_folder = Base.get_sample_folder()
            for file_name, download_url in sample_info.items():
                file_path = os.path.join(sample_folder, file_name)
                download_result = Base.write_sample(file_path, download_url)
                if download_result is False:
                    failed_num += 1
            result = "download result: failed-%s  total-%s" % (failed_num, total_num)
            Base.write_download_log("http://www.malware-traffic-analysis.net", result)


class SampleVirusSign:

    @staticmethod
    def get_login_session():
        session = Base.get_session()
        session.auth = ("infected", "infected")
        return session

    @staticmethod
    def get_download_info():
        download_date = Base.get_date()
        session = SampleVirusSign.get_login_session()
        url = "http://virusign.com/get_hashlist.php"
        params = {
            "sha256": "",
            "n": "ANY",
            "start_date": download_date,
            "end_date": download_date
        }
        response = session.get(url, params=params).text
        sample_info = {}
        for sha256 in response.split("\n"):
            sha256 = sha256.replace("\"", "")
            sample_download_url = "http://virusign.com/file/%s.7z" % sha256
            sample_info[sha256] = sample_download_url
        return sample_info

    @staticmethod
    def download_sample():
        sample_info = SampleVirusSign.get_download_info()
        if sample_info == {}:
            Base.write_download_log("http://virusign.com", "--has`t sample")
        else:
            failed_num = 0
            total_num = len(sample_info)
            sample_folder = Base.get_sample_folder()
            session = SampleVirusSign.get_login_session()
            for sha256, download_url in sample_info.items():
                file_path = os.path.join(sample_folder, sha256 + ".7z")
                download_result = Base.write_sample(file_path, download_url, session=session)
                if download_result is False:
                    failed_num += 1
                    Base.write_md5(sha256)
            result = "download result: failed-%s  total-%s" % (failed_num, total_num)
            Base.write_download_log("http://virusign.com", result)


class SampleMalshare:

    @staticmethod
    def get_sample_info():
        sample_dict = {}
        session = Base.get_session()
        api_key = "2befc1c0b4d476b8527887f3f415648050638eff8dd400071f694e7356d5e49a"
        url = "https://malshare.com/api.php"
        params = {
            "api_key": api_key,
            "action": "getlist"
        }
        response = session.get(url=url, params=params).json()
        for sample_info in response:
            sample_md5 = sample_info["md5"]
            sample_download_url = \
                "https://malshare.com/api.php?api_key=%s&action=getfile&hash=%s" % (api_key, sample_md5)
            sample_dict[sample_md5] = sample_download_url
        return sample_dict

    @staticmethod
    def download_sample():
        sample_info = SampleMalshare.get_sample_info()
        if sample_info == {}:
            Base.write_download_log("https://malshare.com", "--has`t sample")
        else:
            failed_num = 0
            total_num = len(sample_info)
            sample_folder = Base.get_sample_folder()
            for md5, download_url in sample_info.items():
                file_path = os.path.join(sample_folder, md5 + ".vir")
                download_result = Base.write_sample(file_path, download_url)
                if download_result is False:
                    failed_num += 1
                    Base.write_md5(md5)
            result = "download result: failed-%s  total-%s" % (failed_num, total_num)
            Base.write_download_log("https://malshare.com", result)


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
                    md5_url = "https://infosec.cert-pa.it/analyze/%s.html" % sample_md5
                    if add_date == download_date:
                        download_url = SampleInfosec.get_download_link(md5_url)
                        sample_info[sample_md5] = download_url
                    elif add_date < download_date:
                        stop_code = True
                        break
            else:
                break
        return sample_info

    @staticmethod
    def download_sample():
        sample_info = SampleInfosec.get_sample_dict()
        if sample_info == {}:
            Base.write_download_log("https://infosec.cert-pa.it", "--has`t sample")
        else:
            failed_num = 0
            total_num = len(sample_info)
            sample_folder = Base.get_sample_folder()
            for md5, download_url in sample_info.items():
                file_path = os.path.join(sample_folder, md5 + ".vir")
                download_result = Base.write_sample(file_path, download_url)
                if download_result is False:
                    failed_num += 1
                    Base.write_md5(md5)
            result = "download result: failed-%s  total-%s" % (failed_num, total_num)
            Base.write_download_log("https://infosec.cert-pa.it", result)


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
        md5_file_path = os.path.join(base_dir, r"md5_info/%s.txt" % download_date)
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
    def download_sample():
        download_date = SampleMd5.get_date()
        md5_file_path = os.path.join(base_dir, r"md5_info/%s.txt" % download_date)
        md5_dict = {**SampleMd5.md5_virussign(), **SampleMd5.md5_hybrid()}
        with open(md5_file_path, "a+")as file:
            for md5 in md5_dict:
                file.write(md5 + "\n")
        SampleMd5.copy_file(md5_file_path, md5_copy_folder)


class CompressionFunc:

    @staticmethod
    def rename_all(folder_path):
        file_list = Base.get_list(folder_path)
        for file_path in file_list:
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                rename_result = Base.rename(file_path)
                if rename_result is False:
                    os.remove(file_path)

    @staticmethod
    def decompression_all(folder_path):
        file_list = Base.get_list(folder_path)
        for file_path in file_list:
            decompression_result = Base.decompression(file_path)
            if decompression_result is False:
                Base.move_file(file_path)
        file_list = Base.get_list(folder_path)
        for file_path in file_list:
            decompression_result = Base.decompression(file_path)
            if decompression_result is False:
                Base.move_file(file_path)

    @staticmethod
    def final_deal(folder_path):
        CompressionFunc.decompression_all(folder_path)
        CompressionFunc.rename_all(folder_path)
        result_path = Base.compression(folder_path)
        if result_path:
            Base.copy_file(result_path, sample_copy_folder)


def start_func():
    # try:
    #     SampleMalc0de.download_sample()
    # finally:
    #     pass
    # try:
    #     SampleVxvault.download_sample()
    # finally:
    #     pass
    # try:
    #     SampleHybrid.download_sample()
    # finally:
    #     pass
    # try:
    #     SampleVirusBay.download_sample()
    # finally:
    #     pass
    # try:
    #     SampleMalwareTrafficAnalysis.download_sample()
    # finally:
    #     pass
    # try:
    #     SampleVirusSign.download_sample()
    # finally:
    #     pass
    try:
        SampleMalshare.download_sample()
    finally:
        pass
    try:
        SampleInfosec.download_sample()
    finally:
        pass
    # try:
    #     SampleMd5.download_sample()
    # finally:
    #     pass
    # try:
    #     final_folder = Base.get_sample_folder()
    #     CompressionFunc.final_deal(final_folder)
    # finally:
    #     pass


if __name__ == '__main__':
    start_func()
    # while True:
    #     now = datetime.datetime.today().strftime("%H%M%S")
    #     if now == "060000":
    #         try:
    #             start_func()
    #         finally:
    #             pass
