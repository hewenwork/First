# encoding = utf-8
import os
from ftplib import FTP

class Ftp:

    def __init__(self):
        pass

    def login_254(self):
        ftp = FTP()
        host, port = "192.168.1.254", 21
        user, pwd = "download", "iobit201806"
        ftp.connect(host, port)
        ftp.login(user, pwd)
        print(ftp.getwelcome())
        ftp.cwd("/test/hewen")
        print(ftp.nlst())

if __name__ == "__main__":
    Ftp().login_254()
