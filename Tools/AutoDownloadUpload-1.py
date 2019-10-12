# encoding = utf-8
# @Author: Hewen
# @Time: 10/12/2019 3:20 PM
# @File: AutoDownloadUpload-1.py
import os
import re
import socket
import urllib3
import datetime
import requests
from ftplib import FTP
from subprocess import check_output, SubprocessError


class Download:

    def __new__(cls, *args, **kwargs):
        urllib3.disable_warnings()
        cls.download_date = cls.get_download_date()
        return object.__new__(cls)

    def __init__(self):
        url_all = f"https://www.snapshot.clamav.net/daily/snapshot-all-{self.download_date}.zip.001"
        url_critical = f"https://www.snapshot.clamav.net/daily/snapshot-critical-{self.download_date}.zip.001"
        self.download(url_critical)
        self.download(url_all)

    @classmethod
    def get_download_date(cls):
        date_today = datetime.datetime.now()
        date_in = datetime.timedelta(days=3)
        download_data = (date_today - date_in).strftime("%Y%m%d")
        return download_data

    @staticmethod
    def download(url):
        user = "iobit"
        pwd = "iobit#@6sample"
        session = requests.session()
        session.headers["User-Agent"] = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 5.2; Trident/5.0)"
        dir_name = r"G:\Exchange\Download"
        file_name = url.split("/")[-1][:-4]
        file_path = os.path.join(dir_name, f"[infected]{file_name}")
        chunk_size = 1024 * 8
        response = session.get(url, stream=True, verify=False, auth=(user, pwd))
        with open(file_path, "wb")as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)
        dist_dir = r"\\192.168.1.39\f\Auto"
        os.system(f"copy \"{file_path}\" \"{dist_dir}\"")


class Upload:

    def __new__(cls, *args, **kwargs):
        cls.ftp = cls.login()
        cls.date_today = datetime.datetime.today()
        return object.__new__(cls)

    def __init__(self):
        self.delete_outdate()
        self.upload_today()
        self.ftp.quit()

    @classmethod
    def login(cls):
        ftp = FTP()
        host, port = "98.129.229.244", 21  # "192.168.1.254", 21#
        user, pwd = "pftpiobit", "IObit20110617"  # "download", "iobit201806"#
        try:
            ftp.connect(host, port)
            ftp.login(user, pwd)
        except (socket.error, socket.gaierror):
            return
        else:
            return ftp

    def delete(self, file_path):
        dirname = os.path.dirname(file_path)
        self.ftp.cwd(dirname)
        self.ftp.delete(file_path)

    def upload(self, file_path, target_dir, file_name=None):
        self.ftp.cwd(target_dir)
        file = open(file_path, "rb")
        # total_size = os.path.getsize(file_path)
        if file_name is None:
            file_name = os.path.basename(file_path)
        self.ftp.voidcmd('TYPE I')
        with self.ftp.transfercmd(f"STOR {file_name}", None) as conn:
            while True:
                buf = file.read(8192)
                if not buf:
                    break
                conn.sendall(buf)
        file.close()

    def delete_outdate(self):
        dir_name = r"/web/content"
        date_delete = (self.date_today - datetime.timedelta(days=31)).strftime("%Y%m%d")
        self.ftp.cwd(dir_name)
        for file_name in self.ftp.nlst():
            if re.match(f"samples-{date_delete}.rar", file_name):
                file_path = f"{dir_name}/{file_name}"
                self.delete(file_path)
                break

    def upload_today(self):
        dir_name = r"G:\Exchange\Upload"
        dist_dir = r"/web/content"
        file_date = self.date_today.strftime("%Y%m%d")
        file_name = f"samples-{file_date}.rar"
        file_path = os.path.join(dir_name, file_name)
        if os.path.exists(file_path):
            self.upload(file_path, dist_dir)


class MakeRar:

    @staticmethod
    def get_lastest_upload_date():
        file_list = []
        upload_dir = r"G:\Exchange\Upload"
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
        auto_dir = r"G:\auto_collect"
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
            except Exception as e:
                with open(r"Error.log", "a+")as file:
                    file.write(f"{datetime.datetime.now()}: {e}\n")
                command = f"rar a -ep1 -df test.rar {file_path}"
                os.system(command)
                os.remove(r"test.rar")
        return file_list

    @staticmethod
    def force_delete(file_path):
        command = f"rar a -ep1 -df test.rar {file_path}"
        os.system(command)
        os.remove(r"test.rar")

    @staticmethod
    def get_folder_detail(folder):
        detail_dict = {}
        for file_name in os.listdir(folder):
            file_path = os.path.join(folder, file_name)
            try:
                if os.path.isfile(file_path):
                    detail_dict[file_path] = os.path.getsize(file_path)
            except Exception as e:
                with open(r"Error.log", "a+")as file:
                    file.write(f"{datetime.datetime.now()}: {e}\n")
                command = f"rar a -ep1 -df test.rar {file_path}"
                os.system(command)
                os.remove(r"test.rar")
        return detail_dict

    def make_sample(self, file_name, file_list):
        for file_path in file_list:
            command_line = f"rar a -ep1 -y -id[c,d,p,q] -pinfected {file_name} {file_path}"
            try:
                check_output(command_line, shell=True)
            except SubprocessError:
                self.force_delete(file_path)
            else:
                os.remove(file_path)
            # check_output()

    def make_rar(self):
        detail_dict = self.get_folder_detail(self.get_first_download_dir())
        file_name = f"samples-{self.get_lastest_upload_date()}.rar"
        total_size = 0
        for size in detail_dict.values():
            total_size += size
        print(total_size)

        # folder_dict = {}
        # dict_key = self.get_last_upload_date() + datetime.timedelta(days=1)
        # if datetime.datetime.weekday(dict_key) is 5:
        #     dict_key += datetime.timedelta(days=1)
        # dict_values = []
        # folder_size = 0
        # sample_size = 1024 * 1024 * 600
        # dir_path = self.get_first_download_dir()
        # file_list = self.get_file_list(dir_path)
        # for file_path in file_list:
        #     if folder_size <= sample_size:
        #         dict_values.append(file_path)
        #         folder_size += os.path.getsize(file_path)
        #         folder_dict[dict_key] = dict_values
        #     else:
        #         dict_key += datetime.timedelta(days=1)
        #         if datetime.datetime.weekday(dict_key) is 5:
        #             dict_key += datetime.timedelta(days=2)
        #         elif datetime.datetime.weekday(dict_key) is 6:
        #             dict_key += datetime.timedelta(days=1)
        #         folder_size = 0
        #         dict_values = []
        # for key, values in folder_dict.items():
        #     sample_folder = os.path.join(dir_path, datetime.datetime.strftime(key, "samples-%Y%m%d"))
        #     if os.path.exists(sample_folder) is False:
        #         os.makedirs(sample_folder)
        #     for file_path in values:
        #         try:
        #             shutil.move(file_path, sample_folder)
        #         except shutil.Error:
        #             self.force_delete(file_path)
        # for file_name in os.listdir(dir_path):
        #     file_path = os.path.join(dir_path, file_name)
        #     if os.path.isdir(file_path):
        #         target_path = os.path.join(dir_path, file_name)
        #         command_line = f"rar a -ep1 -y -id[c,d,p,q] -pinfected {target_path}.rar {file_path}"
        #         os.system(command_line)
        # rar_size = 1024 * 1024 * 100
        # for file_name in os.listdir(upload_dir):
        #     file_path = os.path.join(upload_dir, file_name)
        #     if os.path.getsize(file_path) <= rar_size:
        #         os.remove(file_path)
        # shutil.rmtree(dir_path, ignore_errors=True)


class AutoDownloadUpload:

    def __init__(self):
        try:
            Download()
            Upload()
            if datetime.datetime.now().date().day % 5 == 2:
                MakeRar()
        except Exception as e:
            with open(r"Error.log", "a+")as file:
                file.write(f"{datetime.datetime.now()}: {e}\n")
        else:
            quit()


if __name__ == "__main__":
    # AutoDownloadUpload()
    MakeRar()
