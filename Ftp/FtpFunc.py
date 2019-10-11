# encoding = utf-8
# @Author: Hewen
# @Time: 10/11/2019 3:41 PM
# @File: FtpFunc.py
import os
import time
import socket
from ftplib import FTP


class FtpFunc:

    def __init__(self):
        self.ftp = self.login()
        file_path = r"C:\Users\hewen\Desktop\ProtonVPN_win_v1.10.1.exe"
        self.upload(file_path, r"/web/content", file_name="ss.exe")
        print(self.ftp.pwd())
        # self.delete()
        self.ftp.quit()

    @staticmethod
    def login():
        ftp = FTP()
        host, port = "98.129.229.244", 21#"192.168.1.254", 21#
        user, pwd = "pftpiobit", "IObit20110617"#"download", "iobit201806"#
        try:
            ftp.connect(host, port)
            ftp.login(user, pwd)
        except (socket.error, socket.gaierror):
            print('Error, cannot reach ' + host)
            return
        else:
            return ftp

    def delete(self, file_path):
        dirname = os.path.dirname(file_path)
        self.ftp.cwd(dirname)
        self.ftp.delete(file_path)

    def upload(self, file_path, target_dir, file_name=None):
        a = time.time()
        self.ftp.cwd(target_dir)
        file = open(file_path, "rb")
        total_size = os.path.getsize(file_path)
        global sent_size
        sent_size = 0
        if file_name is None:
            file_name = os.path.basename(file_path)
            self.ftp.storbinary(f"STOR {file_name}", file, callback=self.callback)
        else:
            self.ftp.storbinary(f"STOR {file_name}", file, callback=lambda sent: self.callback(sent, total_size), blocksize=1024*200)
        file.close()
        print(time.time() - a)

    @staticmethod
    def callback(sent, total_size):
        global sent_size
        sent_size += len(sent)
        print(f"{sent_size} / {total_size}")


if __name__ == "__main__":
    FtpFunc()
