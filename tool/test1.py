import os
import datetime
import requests

base_dir = os.getcwd()


class SnapShot:

    def __init__(self):
        date_download = self.get_date_download()
        session = self.get_session()
        self.download_sample(session, date_download)

    @staticmethod
    def get_session():
        user = "iobit"
        pwd = "iobit#@6sample"
        session = requests.session()
        session.auth = (user, pwd)
        return session

    @staticmethod
    def get_date_download(days=1):
        date_today = datetime.datetime.today()
        date_interval = datetime.timedelta(days=days)
        date_download = date_today - date_interval
        return date_download.strftime("%Y%m%d")

    @staticmethod
    def download_sample(session, date_download):
        file_name = "SnapShot{}.zip".format(date_download)
        path_sample = os.path.join(base_dir, file_name)
        uel_download = "https://www.snapshot.clamav.net/daily/snapshot-all-{}.zip.001".format(date_download)
        response = session.get(uel_download, stream=True, verify=False)
        file_size = 0
        file_total_size = response.headers["content-length"]
        with open(path_sample, "wb")as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    file_size += chunk
                    print("\rdownload: {}".format("#" * int(100 * file_size / file_total_size), end=""))


SnapShot()
