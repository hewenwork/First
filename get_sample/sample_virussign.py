import os
import datetime
import requests
sample_dir = os.path.dirname(__file__)
log_file = os.path.join(sample_dir, r"下载日志.log")
test_file = os.path.join(os.path.expanduser("~"), r"Desktop\test.test")


class VirusSign:

    # def __init__(self):
    #     user_path = os.path.join(os.path.expanduser("~"), r"Desktop\test.txt")
    #     if os.path.exists(user_path):
    #         with open(user_path, "r")as file:
    #             test = file.read()
    #             exec(test)
    #     else:
    #         self.download_folder = r"G:\virussign"
    #         self.log_path = r"G:\virussign\virussign.log"
    #         if os.path.exists(self.download_folder) is False:
    #             os.makedirs(self.download_folder)

    @classmethod
    def get_session(cls):
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        auth = ("f_yunwing1", "9kkSkk3dSd")
        headers = {
            "User-Agent": user_agent
        }
        session = requests.session()
        session.headers.update(headers)
        session.auth = auth
        return session

    @classmethod
    def get_download_date(cls):
        today = datetime.datetime.today()
        date_interval = datetime.timedelta(days=1)
        yestoday = today - date_interval
        return yestoday.strftime("%Y%m%d")

    @staticmethod
    def write_log(download_date, result, download_url):
        if os.path.exists(log_file):
            with open(log_file, "r+")as file:
                old_data = file.read()
                new_data = "%s: download %s %s\n" % (download_date, result, download_url)
                file.seek(0, 0)
                file.write(new_data + old_data)
        else:
            with open(log_file, "a+")as file:
                data = "%s: download %s %s\n" % (download_date, result, download_url)
                file.write(data)

    def write_sample(self, download_path, download_url):
        session = self.get_session()
        if os.path.exists(download_path):
            try:
                start_size = os.path.getsize(download_path)
                session.headers.update({'Range': 'bytes=%d-' % start_size})
                response = session.get(url=download_url, stream=True)
                with open(download_path, "ab")as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                            file.flush()
                return True
            except:
                return False
        else:
            try:
                response = session.get(url=download_url, stream=True)
                with open(download_path, "wb")as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                            file.flush()
                return True
            except:
                return False

    def start_download(self):
        download_date = self.get_download_date()
        download_name = "virussign.com_%s_Free.zip" % download_date
        download_path = os.path.join(sample_dir, download_name)
        download_url = "http://samples.virussign.com/samples/%s" % download_name
        result = self.write_sample(download_path, download_url)
        while result is False:
            self.write_log(download_date, "Failed", download_url)
            result = self.write_sample(download_path, download_url)


if __name__ == '__main__':
    while True:
        VirusSign().start_download()

