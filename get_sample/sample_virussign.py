import os
import time
import datetime
import requests
import configparser
from multiprocessing import Pool, freeze_support
freeze_support()


class VirusSign:

    def __init__(self):
        self.session = self.get_session()
        self.download_dir = self.get_setting("main", "download_folder")
        self.download_date = self.get_download_date()

    @staticmethod
    def get_session():
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        auth = ("f_yunwing1", "9kkSkk3dSd")
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
        setting_path = "setting.ini"
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

    def get_download_date(self):
        days = int(self.get_setting("main", "days"))
        today = datetime.datetime.today()
        date_interval = datetime.timedelta(days=days)
        download_date = (today - date_interval).strftime("%Y%m%d")
        return download_date

    def write_sample(self, download_path, download_url):
        try:
            response = self.session.get(url=download_url, stream=True)
            total_size = int(response.headers["content-length"])
            download_size = 0
            start_download_time = time.time()
            time.sleep(1)
            with open(download_path, "ab")as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
                    file.flush()
                    download_size += 1024
                    have_done = time.time() - start_download_time
                    remaining_time = (total_size - download_size) / (download_size / have_done)
                    print(f"\r{download_size} / {total_size} 剩余时间:{remaining_time/3600:.2f}小时 ", end="")
            return "Success"
        except requests.RequestException as e:
            self.write_log(e)
            return "Failed"

    def start_download(self):
        result = u"没有下载"
        if self.get_setting("main", "autorun") == "yes":
            download_name = "virussign.com_%s_Free.zip" % self.download_date
            download_path = os.path.join(self.download_dir, download_name)
            download_url = "http://samples.virussign.com/samples/%s" % download_name
            result = self.write_sample(download_path, download_url)
        self.write_log(result)


if __name__ == '__main__':
    pool = Pool(3)
    start_time = VirusSign.get_setting("main", "start")
    while True:
        now_time = datetime.datetime.now().strftime("%H:%M:%S")
        showinfo = f"\rNow Time:{now_time}  Start Time:{start_time}"
        print(showinfo, end="")
        if now_time == start_time:
            pool.apply_async(func=VirusSign().start_download, args=())


