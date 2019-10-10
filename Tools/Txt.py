# coding = utf-8
import os
import time
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
        chunk_size = 1024 * 8
        final_dir = r"\\192.168.1.39\f\Auto"
        response = session.get(url, stream=True, verify=False, auth=(user, pwd))
        with open(file_path, "wb")as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)
        os.system(f"copy \"{file_path}\" \"{final_dir}\"")


class Upload:

    def __init__(self):
        self.upload_file()

    @staticmethod
    def upload_file():
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


if __name__ == "__main__":
    Down()
    Upload()
    print("Task Complete")
    time.sleep(10)

