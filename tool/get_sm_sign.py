# coding=utf-8
from contextlib import closing
import requests
import chardet
import os
import datetime
import time
import json
import itertools


class get_smartccl_data():

    def __init__(self):
        self.session = self.get_login()
        self.today, self.last_date = self.day_choose()
        self.download_path = r"\\192.168.1.254\部门共享\TEST\朱亚玲\IMF\IMF手动分析\自动收集\源文件\%s" % self.today
        self.target_path = r"\\192.168.1.254\部门共享\TEST\朱亚玲\IMF\IMF手动分析\自动收集"
        # self.download_path = r"C:\Users\hewen\Desktop\Failed\原文件\%s" % self.today
        # self.target_path = r"C:\Users\hewen\Desktop\Failed\自动收集"
        if os.path.exists(self.download_path) is False:
            os.makedirs(self.download_path)
        self.get_all_info()
        self.get_one()

    def get_login(self):
        url = "http://192.168.1.19/imfsmart/interface/serverlogin.php"
        data = {
            "username": "hewen",
            "password": "hewen"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        }
        session = requests.session()
        session.headers.update(headers)
        session.post(url, data=data)
        print("login successful")
        return session

    def day_choose(self):
        today = datetime.datetime.today().date()
        user_choose = input(u"请输入要下载的开始日期, 默认7天. 回车继续")
        if user_choose == "":
            last_time = 7 - today.weekday() + 1
            last_date = today - datetime.timedelta(days=last_time)
            return str(today.strftime("%Y%m%d")), str(last_date)
        else:
            last_date = today - datetime.timedelta(days=int(user_choose))
            return str(today.strftime("%Y%m%d")), str(last_date)

    def get_file_encodeing(self, file_path):
        try:
            with open(file_path, "rb")as file:
                return chardet.detect(file.read())["encoding"]
        except:
            return "utf-8"

    def get_one(self):
        new_file_path = os.path.join(self.target_path, "SIGN%s.db" % self.today)
        with open(new_file_path, "a", encoding="utf-8")as file_final:
            for file_name in os.listdir(self.download_path):
                file_path = os.path.join(self.download_path, file_name)
                with open(file_path, "r")as file_target:
                    file_final.write(file_target.read())
        test_list = []
        with open(new_file_path, "r", encoding=self.get_file_encodeing(new_file_path))as file:
            ids = file.readlines()
            ids.sort()
            it = itertools.groupby(ids)
            for k, g in it:
                test_list.append(k)
            # print(len(test_list))
        with open(new_file_path, "w+", encoding=self.get_file_encodeing(new_file_path))as file:
            for i in test_list:
                file.writelines(i)

    def get_file(self, taskid):
        download_link = "http://﻿﻿﻿192.168.1.19:8000/%s.db?action=downdb&taskid=%s" % (taskid, taskid)
        file_path = os.path.join(self.download_path, "%s.db" % taskid)
        try:
            with closing(self.session.get(download_link))as respone:
                if respone.status_code == 200:
                    with open(file_path, "wb")as file:
                        file.write(respone.content)
        except:
            print("error")

    def get_all_info(self):
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
                complete, createtime, user, taskid = i["complete"], i["createtime"], i["user"], i["taskid"]
                if complete == 1 and createtime >= self.last_date:
                    print(complete, createtime, taskid)
                    self.get_file(taskid)


if __name__ == "__main__":
    get_smartccl_data()
    print(u"全部下载处理完成, 可以关闭此窗口了")
    time.sleep(20)
