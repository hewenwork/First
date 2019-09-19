# encoding = utf-8
# @Author: Hewen
# @Time:  12:04
import datetime
import os
import shutil
from ftplib import FTP


class Demo:

    def __init__(self):
        print(self.upload_file())
        print(1111)

    @staticmethod
    def upload_file():
        ftp = FTP()
        host, port = "192.168.1.254", 21
        user, pwd = "download", "iobit201806"
        ftp.connect(host, port)
        ftp.login(user, pwd)
        print(ftp.getwelcome())
        upload_file_name = datetime.datetime.now().strftime("samples-%Y%m%d.rar")
        upload_file_path = os.path.join(r"G:\Exchange\Upload", upload_file_name)
        if os.path.exists(upload_file_path):
            ftp.cwd("/test/hewen")
            bufsize = 1024
            with open(upload_file_path, "rb")as file:
                result = ftp.storbinary("STOR " + upload_file_name, file, bufsize)
                print(result)
            ftp.quit()
            return "Upload Finish\nStart Make Archive"
        else:
            return "Today has`t sample,\n Make New Sample Archvie...\n"

if __name__ == "__main__":
    Demo()
