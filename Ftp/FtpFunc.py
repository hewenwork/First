# encoding = utf-8
# @Author: He wen
# @Time: 10/11/2019 3:41 PM
# @File: FtpFunc.py
import os
import re
import socket
import datetime
from ftplib import FTP


class FtpFunc:

    def __new__(cls, *args, **kwargs):
        cls.ftp = cls.login()
        cls.date_today = datetime.datetime.today()
        return object.__new__(cls)

    def __init__(self):
        # self.delete_outdated()
        # self.upload_today()
        self.ftp.quit()
        quit()

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
        dir_name = os.path.dirname(file_path)
        self.ftp.cwd(dir_name)
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

    def delete_outdated(self):
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


if __name__ == "__main__":
    FtpFunc()
