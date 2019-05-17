import os
import datetime
from ftplib import FTP


class FtpFunc:

    @staticmethod
    def get_today():
        today = datetime.datetime.today()
        time_interval = datetime.timedelta(days=1)
        download_day = today - time_interval
        return download_day.strftime("%Y%m%d")

    @staticmethod
    def get_file():
        today = FtpFunc.get_today()
        local_folder = r"E:\交换样本\上传"
        upload_file_name = "samples-%s.rar" % today
        today_upload_file = os.path.join(local_folder, upload_file_name)
        if os.path.exists(today_upload_file):
            return today_upload_file
        else:
            return False

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
            return False

    @staticmethod
    def upload_file():
        today_upload_file = FtpFunc.get_file()
        if today_upload_file:
            ftp = FtpFunc.get_login()
            today = FtpFunc.get_today()
            upload_file_name = "samples-%s.rar" % today
            if ftp:
                upload_folder_path = "/web/content/"
                ftp.cwd(upload_folder_path)
                with open(today_upload_file, "rb")as file:
                    ftp.storbinary("STOR %s" % upload_file_name, file)


if __name__ == '__main__':
    FtpFunc.upload_file()
