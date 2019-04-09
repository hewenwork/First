import datetime
import threading
import time

import requests


class virussign():

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
        self.session = requests.session()
        self.session.headers.update(self.headers)
        self.session.auth = ("f_yunwing1", "9kkSkk3dSd")

    def get_sample(self, url, download_path):
        with open(download_path, "ab")as file:
            respone = self.session.get(url, stream=True)
            for chunk in respone.iter_content(chunk_size=512):
                if chunk:
                    file.write(chunk)

    def start_download(self, iter_content, download_path):
        with open(download_path, "ab")as file:
            file.write(iter_content)
        print("over")

    def get_url(self):
        downlaod_day = datetime.datetime.today() - datetime.timedelta(days=1)
        url = "http://samples.virussign.com/samples/virussign.com_%s_Free.zip" % downlaod_day.strftime("%Y%m%d")
        return url

    def start_downlod(self):
        threading.BoundedSemaphore(5)
        url = self.get_url()
        download_path = r"C:\Users\hewen\Desktop\report"
        respone = self.session.get(url, stream=True)
        print(respone.headers["Content-Length"])
        for chunk in respone.iter_content(chunk_size=1024 * 1024):
            if chunk:
                print(respone.iter_content() / chunk)
                threading.Thread(target=self.start_download, args=(chunk, download_path)).start()


virussign().start_downlod()
