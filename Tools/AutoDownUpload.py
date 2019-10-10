# coding = utf-8
import re
import os
import shutil
import urllib3
import datetime
import requests
from ftplib import FTP
from functools import wraps

auto_dir = r"G:\auto_collect"
upload_dir = r"G:\Exchange\Upload"
download_dir = r"G:\Exchange\Download"
agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 5.2; Trident/5.0)"


def log(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            with open(r"Error.log", "a+")as file:
                file.write(f"{datetime.datetime.now()}: {e}\n")
        return func(*args, **kwargs)

    return decorator


class Down:

    @log
    def __init__(self):
        urllib3.disable_warnings()
        download_data = self.get_download_date()
        url_all = f"https://www.snapshot.clamav.net/daily/snapshot-all-{download_data}.zip.001"
        url_critical = f"https://www.snapshot.clamav.net/daily/snapshot-critical-{download_data}.zip.001"
        self.download(url_critical)
        self.download(url_all)

    @staticmethod
    def get_download_date():
        date_today = datetime.datetime.now()
        date_in = datetime.timedelta(days=3)
        download_data = (date_today - date_in).strftime("%Y%m%d")
        return download_data

    @staticmethod
    def download(url):
        user = "iobit"
        pwd = "iobit#@6sample"
        session = requests.session()
        session.headers["User-Agent"] = agent
        file_name = url.split("/")[-1][:-4]
        file_path = os.path.join(download_dir, "[infected]" + file_name)
        chunk_size = 1024 * 8
        final_dir = r"\\192.168.1.39\f\Auto"
        response = session.get(url, stream=True, verify=False, auth=(user, pwd))
        with open(file_path, "wb")as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)
        os.system(f"copy \"{file_path}\" \"{final_dir}\"")


class Upload:

    @log
    def __init__(self):
        upload_file_name = datetime.datetime.now().strftime("samples-%Y%m%d.rar")
        upload_file_path = os.path.join(upload_dir, upload_file_name)
        if os.path.exists(upload_file_path):
            ftp = FTP()
            host, port = "98.129.229.244", 21
            user, pwd = "pftpiobit", "IObit20110617"
            ftp.connect(host, port)
            ftp.login(user, pwd)
            ftp.cwd("/web/content")
            with open(upload_file_path, "rb")as file:
                ftp.storbinary("STOR " + upload_file_name, file)
            ftp.close()


class MakeRar:

    @staticmethod
    def get_last_upload_date():
        file_list = []
        for file_name in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, file_name)
            if re.match(r"^.*\d{8}\.rar$", file_path) and os.path.isfile(file_path):
                file_list.append(file_path)
        file_list.sort()
        format_data = os.path.split(file_list[-1])[-1][8:-4]
        last_upload_data = datetime.datetime.strptime(format_data, "%Y%m%d")
        return last_upload_data

    @staticmethod
    def get_first_download_dir():
        file_list = []
        for file_name in os.listdir(auto_dir):
            file_path = os.path.join(auto_dir, file_name)
            if re.match(r"^.*\d{4}-\d{2}-\d{2}$", file_path) and os.path.isdir(file_path):
                file_list.append(file_path)
        file_list.sort()
        return file_list[0]

    @staticmethod
    def get_file_list(folder):
        file_list = []
        for file_name in os.listdir(folder):
            file_path = os.path.join(folder, file_name)
            try:
                if os.path.isfile(file_path) and os.path.getsize(file_path) != 0:
                    file_list.append(file_path)
            except OSError:
                command = f"rar a -ep1 -df test.rar {file_path}"
                os.system(command)
                os.remove(r"test.rar")
        return file_list

    @staticmethod
    def force_delete(file_path):
        command = f"rar a -ep1 -df test.rar {file_path}"
        os.system(command)
        os.remove(r"test.rar")

    @log
    def make_rar(self):
        # 获取
        folder_dict = {}
        dict_key = self.get_last_upload_date() + datetime.timedelta(days=1)
        if datetime.datetime.weekday(dict_key) is 5:
            dict_key += datetime.timedelta(days=2)
        dict_values = []
        folder_size = 0
        sample_size = 1024 * 1024 * 600
        dir_path = self.get_first_download_dir()
        file_list = self.get_file_list(dir_path)
        for file_path in file_list:
            if folder_size <= sample_size:
                dict_values.append(file_path)
                folder_size += os.path.getsize(file_path)
                folder_dict[dict_key] = dict_values
            else:
                dict_key += datetime.timedelta(days=1)
                if datetime.datetime.weekday(dict_key) is 5:
                    dict_key += datetime.timedelta(days=2)
                elif datetime.datetime.weekday(dict_key) is 6:
                    dict_key += datetime.timedelta(days=1)
                folder_size = 0
                dict_values = []
        for key, values in folder_dict.items():
            sample_folder = os.path.join(dir_path, datetime.datetime.strftime(key, "samples-%Y%m%d"))
            if os.path.exists(sample_folder) is False:
                os.makedirs(sample_folder)
            for file_path in values:
                try:
                    shutil.move(file_path, sample_folder)
                except shutil.Error:
                    self.force_delete(file_path)
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)
            if os.path.isdir(file_path):
                target_path = os.path.join(upload_dir, file_name)
                command_line = f"rar a -ep1 -y -id[c,d,p,q] -pinfected {target_path}.rar {file_path}"
                os.system(command_line)
        rar_size = 1024 * 1024 * 100
        for file_name in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, file_name)
            if os.path.getsize(file_path) <= rar_size:
                os.remove(file_path)
        shutil.rmtree(dir_path, ignore_errors=True)


if __name__ == "__main__":
    MakeRar()
    # start_time_str = "15:00:00"
    # while True:
    #     date_now = datetime.datetime.now().strftime("%H:%M:%S")
    #     if date_now == start_time_str:
    #         Down()
    #         Upload()
