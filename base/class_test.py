import os
import re
import json
import datetime
import requests
import configparser
from bs4 import BeautifulSoup
from subprocess import check_output, SubprocessError


class Base:

    def __init__(self):
        self.sample_info = {}
        self.session = self.get_session()
        self.download_date = self.get_download_date()
        self.download_log_path = self.get_download_log_path()
        self.download_folder_path = self.get_download_folder()
        self.download_failed_path = self.get_download_failed_path()

    @staticmethod
    def get_option(section, option):
        try:
            config_file = r"C:\Users\hewen\Desktop\main.ini"
            parser = configparser.ConfigParser()
            parser.read(config_file)
            result = parser.get(section, option)
            return result
        except configparser.NoOptionError as e:
            input(e)

    @staticmethod
    def write_sample(sample_path, sample_download_url, session):
        try:
            if os.path.exists(sample_path):
                return True
            else:
                response = session.get(url=sample_download_url, timeout=10)
                if response.status_code == 200:
                    with open(sample_path, "wb")as file:
                        file.write(response.content)
                return True
        except requests.RequestException as error_url:
            print(error_url, sample_download_url)
            return False
        except OSError as error_path:
            print(error_path, sample_path)
            return False

    def switch_vpn(self, turn):
        print("VPN Status: {}".format(turn))
        vpn_name = self.get_option("VPN", "name")
        vpn_user = self.get_option("VPN", "user")
        vpn_password = self.get_option("VPN", "password")
        connect_command = "rasdial  {} {} {}".format(vpn_name, vpn_user, vpn_password)
        disconnect_command = "rasdial {} /DISCONNECT".format(vpn_name)
        command_dict = {
            "on": connect_command,
            "off": disconnect_command
        }
        try:
            check_output(command_dict[turn], shell=True)
            return True
        except SubprocessError as e:
            print(e)

    def get_download_date(self):
        days = int(self.get_option("main", "days"))
        today = datetime.datetime.today()
        time_interval = datetime.timedelta(days=days)
        download_day = today - time_interval
        return download_day.strftime("%Y-%m-%d")

    def get_session(self):
        headers = {"User-Agent": self.get_option("main", "useragent")}
        session = requests.session()
        session.headers.update(headers)
        return session

    def get_download_folder(self):
        download_folder = os.path.join(self.get_option("path", "downloadfolder"), self.download_date)
        if os.path.exists(download_folder) is False:
            os.makedirs(download_folder)
        return download_folder

    def get_download_failed_path(self):
        failed_dir = self.get_option("path", "md5")
        failed_path = os.path.join(failed_dir, "Failed{}.txt".format(self.download_date))
        if os.path.exists(failed_dir) is False:
            os.makedirs(failed_dir)
        return failed_path

    def get_download_log_path(self):
        log_dir = os.path.join(self.get_option("path", "downloadfolder"), r"Log")
        log_path = os.path.join(log_dir, "{}.log".format(self.download_date))
        if os.path.exists(log_dir) is False:
            os.makedirs(log_dir)
        return log_path

    def write_sample_md5(self, md5):
        file_path = self.download_failed_path
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

    def write_download_log(self, result):
        log_path = self.download_log_path
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
            for file_name, download_url in sample_info.items():
                file_md5 = os.path.splitext(file_name)[0]
                file_path = os.path.join(self.download_folder_path, file_name)
                download_result = self.write_sample(file_path, download_url, session)
                if download_result is False:
                    failed_num += 1
                    self.write_sample_md5(file_md5)
            result = "{0} -- Failed:{1}  Total:{2}".format(target, failed_num, total_num)
        self.write_download_log(result=result)


class SampleMalc0de(Base):

    def download(self):
        url = "http://malc0de.com/database/"
        self.switch_vpn("on")
        sample_info = self.get_dict()
        self.switch_vpn("off")
        Base().start_download(sample_info=sample_info, session=self.session, target=url)

    def get_dict(self):
        url = "http://malc0de.com/database/"
        try:
            response = self.session.get(url, timeout=10)
            suop = BeautifulSoup(response.text, "lxml")
            sample_data_list = suop.select("tr > td:nth-of-type(1)")
            sample_url_list = suop.select("tr > td:nth-of-type(2)")
            sample_md5_list = suop.select("tr > td:nth-of-type(7)")
            for sample_date, sample_url, sample_md5 in zip(sample_data_list, sample_url_list, sample_md5_list):
                add_date = sample_date.getText()
                sample_md5 = sample_md5.getText()
                file_name = sample_md5 + ".vir"
                sample_url = "http://" + sample_url.getText()
                if add_date == self.download_date:
                    self.sample_info[file_name] = sample_url
        except requests.RequestException as e:
            print(e)
        return self.sample_info
