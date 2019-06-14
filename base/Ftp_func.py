import os
import datetime
from ftplib import FTP


class FtpFunc:

    def __init__(self):
        self.date = datetime.datetime.today().strftime("%Y%m%d")
        self.ftp = self.get_login()
        self.upload_file = self.get_file()
        self.upload_file_name = "samples-%s.rar" % self.date
        self.ftp.cwd("/web/content/")
        with open(self.upload_file, "rb")as file:
            self.ftp.storbinary("STOR %s" % self.upload_file_name, file)

    @staticmethod
    def get_login():
        ftp = FTP()
        host, port = "98.129.229.244", 21
        user, pwd = "pftpiobit", "IObit20110617"
        ftp.connect(host, port)
        ftp.login(user, pwd)
        if "server ready" in ftp.getwelcome():
            return ftp
        else:
            exit("Ftp Error")

    def get_file(self):
        local_folder = r"E:\交换样本\上传"
        upload_file_name = "samples-%s.rar" % self.date
        upload_file = os.path.join(local_folder, upload_file_name)
        if os.path.exists(upload_file):
            return upload_file
        else:
            exit("No File")


if __name__ == "__main__":
    FtpFunc()
