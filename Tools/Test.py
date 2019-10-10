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

    def upload_file(self):
        ftp = FTP()
        host, port = "192.168.1.254", 21
        user, pwd = "download", "iobit201806"
        ftp.connect(host, port)
        ftp.login(user, pwd)
        upload_file_name = datetime.datetime.now().strftime("samples-%Y%m%d.rar")
        upload_file_path = os.path.join(r"G:\Exchange\Upload", upload_file_name)
        global total, sent_size
        sent_size = 0
        total = os.path.getsize(upload_file_path)
        if os.path.exists(upload_file_path):
            ftp.cwd("/test/hewen")
            with open(upload_file_path, "rb")as file:
                ftp.storbinary("STOR " + upload_file_name, file, callback=self.call)
            ftp.quit()
            return "Upload Finish\nStart Make Archive"
        else:
            return "Today has`t sample,\n Make New Sample Archvie...\n"

    def call(self, *args):
        global total, sent_size
        sent_size += len(*args)
        process = int(sent_size/total * 100)
        print(f"\rUpload file: {sent_size} of {total} The process is {process}%", end="")
class A:
    def __init__(self):
        print(1)
        self.b()

    @staticmethod
    def a():
        print("a")

    def b(self):
        A.a()

if __name__ == "__main__":
    A()
    # Demo()


