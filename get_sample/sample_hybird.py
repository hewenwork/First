import os
import re
import sqlite3
import datetime
import requests
from bs4 import BeautifulSoup


class Database:

    def __init__(self):
        init_sql = '''
        create table if not exists hybird(
        datetime varchar ,
        file_name varchar unique ,
        download_url varchar
        );'''
        self.connect = sqlite3.connect("database.db")
        self.cursor = self.connect.cursor()
        self.cursor.execute(init_sql)
        self.connect.commit()
        self.datetime = datetime.datetime.now().date()

    def select_table(self, file_name):
        sql = "select * from hybird where file_name='{}';".format(file_name)
        result = self.cursor.execute(sql).fetchall()
        return result

    def execute_sql(self, sql):
        self.cursor.execute(sql)
        self.connect.commit()

    def insert_info(self, file_name, download_url):
        sql = "insert into hybird values ('{}', '{}', '{}')".format(self.datetime, file_name, download_url)
        self.execute_sql(sql)


class Base:

    def __init__(self):
        self.base_dir = os.getcwd()
        self.download_date = self.get_download_date()
        self.download_log = self.get_download_log_path()
        self.download_folder = self.get_download_folder()
        self.download_failed = self.get_download_failed_path()

    @staticmethod
    def get_download_date():
        if os.path.exists("test.txt"):
            with open("test.txt", "r")as file:
                days = int(file.read())
        else:
            days = 1
        today = datetime.datetime.today()
        time_interval = datetime.timedelta(days=days)
        download_day = today - time_interval
        return download_day.strftime("%Y-%m-%d")

    @staticmethod
    def get_session():
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        headers = {"User-Agent": user_agent}
        session = requests.session()
        session.headers.update(headers)
        return session

    @staticmethod
    def write_sample(sample_path, sample_download_url, session):
        if os.path.exists(sample_path):
            return True
        else:
            try:
                response = session.get(url=sample_download_url, timeout=5).content
                with open(sample_path, "wb")as file:
                    file.write(response)
                return True
            except requests.RequestException:
                return False
            except OSError:
                return False

    @staticmethod
    def start_info():
        sample_info = {}
        session = Base.get_session()
        download_date = Base.get_download_date()
        return sample_info, session, download_date

    def get_download_folder(self):
        download_folder = os.path.join(self.base_dir, self.download_date)
        if os.path.exists(download_folder) is False:
            os.makedirs(download_folder)
        return download_folder

    def get_download_failed_path(self):
        download_data = Base.get_download_date()
        failed_dir = os.path.join(self.base_dir, r"MD5&SHA256")
        failed_path = os.path.join(failed_dir, "Failed{}.txt".format(download_data))
        if os.path.exists(failed_dir) is False:
            os.makedirs(failed_dir)
        return failed_path

    def get_download_log_path(self):
        download_data = Base.get_download_date()
        log_dir = os.path.join(self.base_dir, r"Log")
        log_path = os.path.join(log_dir, "{}.log".format(download_data))
        if os.path.exists(log_dir) is False:
            os.makedirs(log_dir)
        return log_path

    def write_sample_md5(self, md5):
        file_path = self.download_failed
        if os.path.exists(file_path):
            if len(md5) == 64:
                with open(file_path, "a+")as file:
                    file.write(md5 + "\n")
            else:
                with open(file_path, "r+")as file:
                    old_data = file.read()
                    file.seek(0, 0)
                    file.write(md5 + "\n" + old_data)
        else:
            with open(file_path, "a+")as file:
                file.write(md5 + "\n")

    def write_download_log(self, result: object) -> object:
        log_path = self.download_log
        if os.path.exists(log_path):
            with open(log_path, "r+")as file:
                old_data = file.read()
                file.seek(0, 0)
                file.write(result + "\n" + old_data)
        else:
            with open(log_path, "a+")as file:
                file.write(result + "\n")

    def start_download(self, sample_info, session, target):
        failed_num = 0
        total_num = len(sample_info)
        if total_num is 0:
            result = "{}--has`t data".format(target)
        else:
            download_num = 0
            for file_name, download_url in sample_info.items():
                file_md5 = os.path.splitext(file_name)[0]
                file_path = os.path.join(self.download_folder, file_name)
                download_result = Base.write_sample(file_path, download_url, session)
                if download_result is False:
                    failed_num += 1
                    Base().write_sample_md5(file_md5)
                download_num += 1
                print("\rdownload", "{} / {}".format(download_num, total_num), end="")
            result = "{0} -- Failed:{1}  Total:{2}".format(target, failed_num, total_num)
        print("\n", result)
        Base().write_download_log(result=result)


class SampleHybrid:

    def __init__(self):
        headers = {"User-Agent":  "Falcon Sandbox"}
        session = requests.session()
        session.headers.update(headers)
        url = "https://www.hybrid-analysis.com/login"
        try:
            response = session.get(url)
            token = re.findall("name=\"token\" value=\"(.*?)\">", response.text)[0]
            data = {
                "email": "cicely@iobit.com",
                "password": "IObit2018",
                "token": token
            }
            session.post(url, data=data)
            self.session = session
        except requests.RequestException as e:
            exit(e)

    @staticmethod
    def write_database(info_dict):
        for file_name, download_url in info_dict.items():
            if len(Database().select_table(file_name)) < 1:
                Database().insert_info(file_name, download_url)

    def get_last_info(self):
        json_dict = {}
        url = "https://www.hybrid-analysis.com/feed?json"
        try:
            base_url = "https://www.hybrid-analysis.com/download-sample/"
            json_content = self.session.get(url).json()
            for data_type in json_content["data"]:
                md5 = data_type["md5"]
                file_name = md5 + ".gz"
                sha256 = data_type["sha256"]
                environmentId = data_type["environmentId"]
                threatlevel = data_type["threatlevel"]
                if threatlevel != 0:
                    download_url = base_url + sha256 + "?environmentId=%s" % environmentId
                    json_dict[file_name] = download_url
        except requests.RequestException as e:
            print(e)
        self.write_database(json_dict)

    def get_page_info(self):
        page_dict = {}
        url = "https://www.hybrid-analysis.com/recent-submissions"
        threat_level = ["malicious", "ambiguous", "suspicious", "-"]
        for page in range(11):
            params = {
                "filter": "file",
                "sort": "^timestamp",
                "page": page
            }
            try:
                response = self.session.get(url, params=params)
                suop = BeautifulSoup(response.text, "lxml")
                sample_download_list = suop.select("a.btn.btn-default.btn-xs.pull-right.sampledl.download-url")
                is_virus_list = suop.select("dd:nth-of-type(3)")
                for sample_download_url, is_virus in zip(sample_download_list, is_virus_list):
                    sample_sha256 = sample_download_url.get("href").split("?")[0][17:]
                    file_name = sample_sha256 + ".gz"
                    sample_download_url = "https://www.hybrid-analysis.com{}".format(sample_download_url.get("href"))
                    is_virus = is_virus.getText().strip()
                    if is_virus in threat_level:
                        page_dict[file_name] = sample_download_url
            except requests.RequestException as e:
                exit(e)
        self.write_database(page_dict)


if __name__ == "__main__":
    SampleHybrid().get_last_info()
    while True:
        datetime_now = datetime.datetime.now().strftime("%H%M%S")
        if datetime_now in ["060000", "120000", "180000", "235900"]:
            SampleHybrid().get_page_info()
        elif datetime_now == "040000":
            SampleHybrid().get_last_info()

