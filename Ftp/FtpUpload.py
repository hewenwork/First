# encoding = utf-8
# @Author: Hewen
# @Time:  14:32
import datetime
import os
from ftplib import FTP


class Upload:

    def __init__(self, path_upload_file):
        self.upload_file(path_upload_file)

    def upload_file(self, path_upload_file):
        global ftp
        ftp = FTP()
        host, port = "98.129.229.244", 21
        user, pwd = "pftpiobit", "IObit20110617"
        ftp.connect(host, port)
        ftp.login(user, pwd)
        upload_file_name = os.path.basename(path_upload_file)
        if os.path.exists(path_upload_file):
            global total, sent_size
            total = os.path.getsize(path_upload_file)
            sent_size = 0
            ftp.cwd("/web/content")
            with open(path_upload_file, "rb")as file:
                ftp.storbinary("STOR " + upload_file_name, file, callback=self.call)
                print("xxxx")
            return "Upload Finish\nStart Make Archive"
        else:
            return "Today has`t sample,\n Make New Sample Archvie...\n"

    @staticmethod
    def call(*args):
        global total, sent_size
        sent_size += len(*args)
        process = int(sent_size/total * 100)
        print(f"\rUpload file: {sent_size} of {total} The process is {process}%", end="")



if __name__ == "__main__":
    print(Upload(r"C:\Users\hewen\Desktop\md5.exe"))
    input("aaaaaaaaaaaaaaaaaa")

    