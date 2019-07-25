import os
import datetime
import requests
import configparser
from contextlib import closing


class VirusSign:

    def __init__(self):
        self.session = self.get_session()
        self.base_dir = self.get_setting("main", "dir")

    @staticmethod
    def get_session():
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        auth = ("infected", "infected")
        headers = {"User-Agent": user_agent}
        session = requests.session()
        session.headers.update(headers)
        session.auth = auth
        return session

    @staticmethod
    def write_log(result):
        log = r"下载日志.log"
        log_time = datetime.datetime.now()
        data = f"{log_time}:  {result}\n"
        with open(log, "a+")as file:
            file.write(data)

    @classmethod
    def get_setting(cls, section, option):
        con = configparser.ConfigParser()
        setting_path = "VirusSign.ini"
        try:
            con.read(setting_path)
            result = con.get(section, option)
            return result
        except configparser.NoSectionError as e:
            VirusSign.write_log(u"没有配置文件或section--" + str(e))
            print(e)
        except configparser.NoOptionError as e:
            VirusSign.write_log(u"没有配置节点--" + str(e))
            print(e)

    def get_sample_dict(self, download_date):
        download_dict = {}
        url = "http://virusign.com/get_hashlist.php"
        params = {
            "sha256": "",
            "n": "ANY",
            "start_date": download_date,
            "end_date": download_date
        }
        with closing(self.session.get(url, params=params, timeout=20))as response:
            if len(response.text) != 0:
                for sha256 in response.text.split("\n")[:-1]:
                    sha256 = sha256.replace("\"", "")
                    sample_name = sha256 + ".7z"
                    sample_download_url = "http://virusign.com/file/%s" % sample_name
                    download_dict[sample_download_url] = sample_download_url
        return download_dict

    def write_sample(self, file_path, download_url):
        try:
            if os.path.exists(file_path)is False:
                response = self.session.get(download_url, timeout=5, stream=True)
                with open(file_path, "wb")as file:
                    file.write(response.content)
                return True
        except requests.exceptions as e:
            self.write_log(e)

    def get_download_date(self):
        start_date = datetime.datetime.strptime("2012-02-02", "%Y-%m-%d")
        end_date = datetime.datetime.strptime("2019-04-01", "%Y-%m-%d")
        date_interval = end_date - start_date
        for days in range(date_interval.days):
            run_date = (start_date + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
            print(run_date)
            print(self.get_sample_dict(run_date))


if __name__ == "__main__":
    a = VirusSign().get_sample_dict("2011-07-01")
    print(a)



