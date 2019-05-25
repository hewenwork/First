import datetime
import json
import requests
dir_folder = r"C:\Users\hewen\Desktop\20190520"


class SmartCclFunc:

    def __init__(self):
        session = SmartCclFunc.get_login()
        if session:
            self.session = session
        else:
            exit("error: login failed, pls check your connect")
        self.data = {
            "action": "",
            "cpage": 0,
            "pagemaxitems": 15
        }
        self.sign_dict = {}
        self.sign_download_date = "2019-04-01"
        self.md5_dict = {}
        self.md5_download_date = "2019-05-01"

    @staticmethod
    def get_date(days=1):
        today = datetime.datetime.today()
        time_interval = datetime.timedelta(days=days)
        download_day = today - time_interval
        return download_day.strftime("%Y-%m-%d")

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
        result = session.post(url, data=data).status_code
        if result == 200:
            return session
        else:
            return False

    def write_file(self, file_path, download_url):
        response = self.session.get(download_url).content
        with open(file_path, "w")as file:
            file.write(response)

    def get_sign_pages(self):
        url = "http://192.168.1.19/imfsmart/interface/it_taskmanager.php"
        self.data["action"] = "gettasks"
        info_link = self.session.post(url=url, data=self.data)
        pages = json.loads(info_link.text[3:])["pages"]
        return pages

    def get_sign_page_info(self, page):
        url = "http://192.168.1.19/imfsmart/interface/it_taskmanager.php"
        self.data.update({"cpage": page})
        page_info = self.session.post(url=url, data=self.data).text[3:]
        page_dict = json.loads(page_info)
        for info in page_dict["tasks"]:
            createtime, user, taskid = info["createtime"][:10], info["user"], info["taskid"]
            if createtime <= self.sign_download_date:
                self.sign_dict[taskid] = user
            else:
                break

    def get_md5_page_info(self, page):
        url = "http://192.168.1.19/imfsmart/interface/it_taskmanager.php"
        self.data.update({"cpage": page})
        page_info = self.session.post(url=url, data=self.data).text[3:]
        print(page_info)
        page_dict = json.loads(page_info)
        for info in page_dict["md5s"]:
            createtime, user, taskid = info["createtime"][:10], info["user"], info["taskid"]
            if createtime <= self.sign_download_date:
                self.sign_dict[taskid] = user
            else:
                break

    def get_md5_pages(self):
        url = "http://192.168.1.19/imfsmart/interface/it_md5mgr.php"
        self.data["action"] = "getmd5s"
        info_link = self.session.post(url=url, data=self.data)
        pages = json.loads(info_link.text[3:])["pages"]
        return pages

    def get_sign_dict(self):
        pages = self.get_sign_pages()
        list(map(self.get_sign_page_info, range(1, pages)))
        print(self.sign_dict)
        return self.sign_dict

    def get_md5_dict(self):
        pages = self.get_md5_pages()
        list(map(self.get_sign_page_info, range(1, pages)))
        print(self.md5_dict)
        return self.md5_dict


    def get_md5(self):
        # self.session
        pass


SmartCclFunc().get_md5_page_info(0)