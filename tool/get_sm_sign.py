# coding=utf-8
import os
import time
import json
import chardet
import datetime
import requests
today = datetime.datetime.today().strftime("%Y-%m-%d")
# base_dir = r"C:\Users\hewen\Desktop\20190521\新建文件夹"
# final_file = r"C:\Users\hewen\Desktop\20190521\新建文件夹\SIGN{}.db".format(today)
base_dir = r"\\192.168.1.254\部门共享\TEST\朱亚玲\IMF\IMF手动分析\自动收集\源文件"
final_file = r"\\192.168.1.254\部门共享\TEST\朱亚玲\IMF\IMF手动分析\自动收集\SIGN{}.db".format(today)
'''
        self.download_path = r"\\192.168.1.254\部门共享\TEST\朱亚玲\IMF\IMF手动分析\自动收集\源文件\%s" % self.today
        self.target_path = r"\\192.168.1.254\部门共享\TEST\朱亚玲\IMF\IMF手动分析\自动收集"
'''


class GetSign:

    def __init__(self):
        self.session = self.get_login()
        self.start_date, self.end_date = self.download_date()
        self.download_folder_path = self.get_download_dir()
        self.start_download()
        self.get_final_file()

    @staticmethod
    def get_login():
        url = "http://192.168.1.19/imfsmart/interface/serverlogin.php"
        data = {
            "username": "hewen",
            "password": "hewen"
        }
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"}
        session = requests.session()
        session.headers.update(headers)
        session.post(url, data=data)
        print("login successful\n")
        return session

    @staticmethod
    def download_date():
        start_date = input(u"请输入要下载的开始日期. 如2019-05-01 回车继续:\n")
        end_date = input(u"请输入要下载的结束日期, 如2019-05-20 回车继续:\n")
        # start_date = "2019-05-01"
        # end_date = "2019-05-20"
        return start_date, end_date

    @staticmethod
    def get_file_encoding(file_path):
        try:
            with open(file_path, "rb")as file:
                return chardet.detect(file.read())["encoding"]
        except:
            return "utf-8"

    @staticmethod
    def get_download_dir():
        download_folder_path = os.path.join(base_dir, today)
        if os.path.exists(download_folder_path)is False:
            os.makedirs(download_folder_path)
        return download_folder_path

    def write_file(self, taskid, user):
        download_url = "http://﻿﻿﻿192.168.1.19:8000/{0}.db?action=downdb&taskid={0}".format(taskid)
        response = self.session.get(download_url)
        if response.status_code == 200:
            file_path = os.path.join(self.download_folder_path, taskid + ".db")
            with open(file_path, "wb")as file:
                file.write(response.content)

    def get_sign_dict(self):
        sign_dict = {}
        data = {
            "action": "gettasks",
            "cpage": 0,
            "pagemaxitems": 15
        }
        info_url = "http://192.168.1.19/imfsmart/interface/it_taskmanager.php"
        info_link = self.session.post(url=info_url, data=data)
        pages = json.loads(info_link.text[3:])["pages"]
        for page in range(0, pages):
            data.update({"cpage": page})
            info_link = self.session.post(url=info_url, data=data)
            info_dict = json.loads(info_link.text[3:])["tasks"]
            for i in info_dict:
                completetime, user, taskid = i["completetime"][:10], i["user"], i["taskid"]
                if self.end_date >= completetime >= self.start_date:
                    print(completetime, taskid)
                    sign_dict[taskid] = user
        return sign_dict

    def start_download(self):
        sign_dict = self.get_sign_dict()
        for taskid, user in sign_dict.items():
            self.write_file(taskid, user)

    def get_final_file(self):
        with open(final_file, "wb")as file:
            for file_name in os.listdir(self.download_folder_path):
                file_path = os.path.join(self.download_folder_path, file_name)
                file.write(open(file_path, "rb").read())
        final_dict = {}
        with open(final_file, "rb+")as file:
            for i in file.readlines():
                final_dict[i] = 1
            file.seek(0, 0)
            for j in final_dict:
                file.write(j)


if __name__ == "__main__":
    GetSign()
    print(u"全部下载处理完成, 可以关闭此窗口了")
    time.sleep(20)
