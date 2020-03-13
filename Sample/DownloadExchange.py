# encoding = utf-8
# @Author: Hewen
# @Time: 12/31/2019 2:23 PM
# @File: DownloadExchange.py
import datetime
import os
import logging

import requests
import urllib3

logging.basicConfig(**{
    "filemode": "a+",
    "filename": f"{os.path.basename(__file__)}_debug.log",
    "level": logging.INFO,
    "format": "%(asctime)s--: %(lineno)d: %(funcName)s: %(levelname)s - %(message)s"
})
log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())  # print in screen

download_dir = r"G:\Exchange\Download"
auto_dir = r"\\192.168.1.39\f\Auto"

agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 5.2; Trident/5.0)"
urllib3.disable_warnings()


class DownloadExchange:

    def __init__(self):
        download_data = self.get_download_date()
        url_all = f"https://www.snapshot.clamav.net/daily/snapshot-all-{download_data}.zip.001"
        url_critical = f"https://www.snapshot.clamav.net/daily/snapshot-critical-{download_data}.zip.001"
        self.download(url_critical)
        self.download(url_all)

    @staticmethod
    def get_download_date():
        date_today = datetime.datetime.now()
        date_in = datetime.timedelta(days=3)
        download_data = (date_today - date_in).strftime("%Y%m%d")
        return download_data

    @staticmethod
    def download(url):
        user = "iobit"
        pwd = "iobit#@6sample"
        session = requests.session()
        session.headers["User-Agent"] = agent
        file_name = url.split("/")[-1][:-4]
        file_path = os.path.join(download_dir, "[infected]" + file_name)
        chunk_size = 1024 * 8
        try:
            response = session.get(url, stream=True, verify=False, auth=(user, pwd))
            with open(file_path, "wb")as file:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        file.write(chunk)
            os.system(f"copy \"{file_path}\" \"{auto_dir}\"")
        except Exception as e:
            return False, e
        else:
            return True, datetime.datetime.now()




if __name__ == "__main__":
    DownloadExchange()
