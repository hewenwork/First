# encoding = utf-8
# @Author: Hewen
# @Time:  15:25
import os
import re
import json
import datetime
import requests


class Smart:

    url = "http://192.168.1.19/imfsmart/interface/it_taskmanager.php"
    post_data = {
        "action": "",
        "cpage": 0,
        "pagemaxitems": 15
    }

    def __new__(cls, *args, **kwargs):
        cls.session = cls.login()
        return object.__new__(cls)

    def __init__(self):
        date_start = datetime.datetime.strptime(self.input_check(u"开始"), "%Y-%m-%d")
        date_end = datetime.datetime.strptime(self.input_check(u"结束"), "%Y-%m-%d")
        self.targt_dir = os.path.join(r"\\192.168.1.254\部门共享\TEST\朱亚玲\IMF\IMF手动分析\自动收集\源文件", datetime.datetime.strftime(date_end, "%Y%m%d"))
        if os.path.exists(self.targt_dir)is False:
            os.makedirs(self.targt_dir)
        self.total_sign_path = r"\\192.168.1.254\部门共享\TEST\朱亚玲\IMF\IMF手动分析\自动收集\SigN%s.db" % datetime.datetime.strftime(date_end, "%Y%m%d")
        self.total_md5_path = r"\\192.168.1.254\部门共享\TEST\朱亚玲\IMF\IMF手动分析\自动收集\Md5N%s.db" % datetime.datetime.strftime(date_end, "%Y%m%d")
        self.getSinN(date_start, date_end)
        self.getMd5(date_start, date_end)

    def input_check(self, what):
        result = input(u"请输入%s下载的日期, 格式XXXX-XX-XX, 如2019-09-01\n" % what)
        if re.match(r"^\d{4}-\d{2}-\d{2}$", result):
            return result
        else:
            print(u"\r输入错误, 请重新输入. 格式XXXX-XX-XX, 如2019-09-01\n")
            return self.input_check(what)

    @classmethod
    def login(cls):
        url = "http://192.168.1.19/imfsmart/interface/serverlogin.php"
        data = {
            "username": "hewen",
            "password": "hewen"
        }
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"}
        session = requests.session()
        session.headers.update(headers)
        result = session.post(url, data=data).status_code
        if result == 200:
            return session
        else:
            return

    @staticmethod
    def md5Check(file_path):
        md5_dict = {}
        with open(file_path, "r", encoding="utf-8")as file:
            lines = file.readlines()
        for line in lines:
            if re.match(r"^[\w.]*?,\w*?,\w*?\n$", line):
                md5_dict[line] = ""
        with open(file_path, "w", encoding="utf-8")as file:
            for line in md5_dict.keys():
                file.write(line)

    @staticmethod
    def sigNCheck(file_path):
        sign_dict = {}
        with open(file_path, "r", encoding="utf-8")as file:
            lines = file.readlines()
        for line in lines:
            if re.match(r"^[\w.]*?,\w*?,\w*?,\w*?,\w*?\n$", line):
                sign_dict[line] = ""
        with open(file_path, "w", encoding="utf-8")as file:
            for line in sign_dict.keys():
                file.write(line)

    def getSinN(self, start, end):
        download_dict = {}
        self.post_data["action"] = "gettasks"
        cpage = 0
        stopcode = True
        while stopcode:
            response = self.session.post(self.url, data=self.post_data)
            result = json.loads(response.text[3:])
            for values in result["tasks"]:
                completetime = datetime.datetime.strptime(values["completetime"], "%Y-%m-%d %H:%M:%S")if values["completetime"]is not "" else end + datetime.timedelta(days=11)
                if start <= completetime <= end:
                    download_dict[values["taskid"]] = ""
                elif start > completetime:
                    stopcode = False
                    break
            cpage += 1
            self.post_data["cpage"] = cpage
        for taskid in download_dict.keys():
            file_path = os.path.join(self.targt_dir, f"{taskid}.db")
            downlaod_url = f"http://192.168.1.19:8000/{taskid}.db?action=downdb&taskid={taskid}"
            file_content = self.session.get(downlaod_url).content
            with open(file_path, "wb")as file:
                file.write(file_content)
        with open(self.total_sign_path, "w", encoding="utf-8")as file:
            for file_name in os.listdir(self.targt_dir):
                file_path = os.path.join(self.targt_dir, file_name)
                with open(file_path, "r")as fileSon:
                    file.write(fileSon.read())
        self.sigNCheck(self.total_sign_path)

    def getMd5(self, start, end):
        with open(self.total_md5_path, "wb")as file:
            for data in range((end - start).days + 1):
                data = (start + datetime.timedelta(days=data)).strftime("%Y-%m-%d")
                download_url = f"http://192.168.1.19:8000/?action=downmd5db&dates={data}"
                response = self.session.get(download_url)
                if response.status_code is 200:
                    content = self.session.get(download_url).content
                    file.write(content)
        self.md5Check(self.total_md5_path)


if __name__ == "__main__":
    Smart()
    input("下载完成，请手动关闭此窗口")