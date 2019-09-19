# coding = utf-8
import re
import os
import urllib3
import datetime
import requests
from ftplib import FTP
agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
download_dir = r"G:\Exchange\Download"
upload_dir = r"G:\Exchange\Upload"
auto_dir = r"G:\auto_collect"


class Down:

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
        file_size = 0
        chunk_size = 1024 * 10
        final_dir = r"\\192.168.1.39\f\Auto"
        try:
            response = session.get(url, stream=True, verify=False, auth=(user, pwd))
            file_total_size = int(response.headers["content-length"])
            with open(file_path, "wb")as file:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        file.write(chunk)
                        file_size += len(chunk)
                        percent = int(
                            file_size / file_total_size * 100) if file_size != file_total_size else "Download Over \n"
                        print(f"\rDownload: {file_name} {percent}%", end=" ")
            os.system(f"copy \"{file_path}\" \"{final_dir}\"")
        except Exception as e:
            print(e)


class Upload:

    def __init__(self):
        result_upload = self.upload_file()
        print(result_upload)
        result_make = self.make_rar()
        print(result_make)

    @staticmethod
    def upload_file():
        ftp = FTP()
        host, port = "98.129.229.244", 21
        user, pwd = "pftpiobit", "IObit20110617"
        ftp.connect(host, port)
        ftp.login(user, pwd)
        upload_file_name = datetime.datetime.now().strftime("samples-%Y%m%d.rar")
        upload_file_path = os.path.join(upload_dir, upload_file_name)
        if "ready" in ftp.getwelcome() and os.path.exists(upload_file_path):
            ftp.cwd("/web/content")
            bufsize = 1024
            file = open(upload_file_path, "rb")
            ftp.storbinary(f"STOR {upload_file_name}", file, bufsize)
            file.close()
            ftp.quit()
            return "Upload Finish\nStart Make Archive"
        else:
            return "Today has`t sample,\n Make New Sample Archvie...\n"

    @staticmethod
    def force_delete(file_path):
        try:
            command = f"rar a -ep1 -df test.rar {file_path}"
            os.system(command)
            os.remove(r"test.rar")
        except Exception as e:
            print(e)

    @staticmethod
    def get_last_upload_data():
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
            file_list.append(file_path)
        for file_path in file_list:
            try:
                os.path.getsize(file_path)
            except Exception as e:
                print(e)
                command = f"rar a -ep1 -df test.rar {file_path}"
                os.system(command)
                os.remove(r"test.rar")
        file_list = []
        for file_name in os.listdir(folder):
            file_path = os.path.join(folder, file_name)
            file_list.append(file_path)
        return file_list

    def make_rar(self):
        dir_path = self.get_first_download_dir()
        file_list = self.get_file_list(dir_path)
        co_size = 1024 * 1024 * 600
        init_size = 0
        init_data = self.get_last_upload_data()
        init_data += datetime.timedelta(days=1)
        if datetime.datetime.weekday(init_data) is 5:
            init_data += datetime.timedelta(days=2)
        for file_path in file_list:
            if init_size <= co_size:
                sample_path = os.path.join(upload_dir, datetime.datetime.strftime(init_data, "samples-%Y%m%d"))
                command_line = f"rar a -ep1 -y -id[c,d,p,q] -pinfected {sample_path}.rar {file_path}"
                os.system(command_line)
                init_size += os.path.getsize(file_path)
            else:
                init_size = 0
                init_data += datetime.timedelta(days=1)
                if datetime.datetime.weekday(init_data) is 5:
                    init_data += datetime.timedelta(days=2)
                elif datetime.datetime.weekday(init_data) is 6:
                    init_data += datetime.timedelta(days=1)
        os.rename(dir_path, dir_path + u"已上传")
        rar_size = 1024 * 1024 * 100
        for file_name in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, file_name)
            if os.path.getsize(file_path) <= rar_size:
                os.remove(file_path)
        return "Finish"


if __name__ == "__main__":
    Upload().make_rar()
    # print(__file__)
    # if __file__[-2:] == "py":
    #     MakeApp(__file__)
    # start_time_str = "15:00:00"
    # while True:
    #     date_now = datetime.datetime.now().strftime("%H:%M:%S")
    #     print(f"\rNow time: {date_now}  Start time: {start_time_str}", end="")
    #     if date_now == start_time_str:
    #         print("Start Download\n")
    #         Down()
    #         print("Start Upload")
    #         Upload()
