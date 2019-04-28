import os
import datetime
import requests
# test_file = os.path.join(os.path.expanduser("~"), r"Desktop\test.test")
download_folder = os.path.dirname(__file__)
log_path = os.path.join(download_folder, "urlhaus.log")
dist_dir = r"\\192.168.1.39\f\Auto"


class Urlhaus:

    # def __init__(self):
    #     self.log_path = r"G:\urlhaus\urlhaus.log"
    #     if os.path.exists(self.download_folder) is False:
    #         os.makedirs(self.download_folder)

    @classmethod
    def get_session(cls):
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        headers = {
            "User-Agent": user_agent
        }
        session = requests.session()
        session.headers.update(headers)
        return session

    @classmethod
    def get_download_date(cls):
        today = datetime.datetime.today()
        date_interval = datetime.timedelta(days=1)
        download_day = today - date_interval
        return download_day.strftime("%Y-%m-%d")

    @classmethod
    def write_log(cls, download_date, result, download_url):
        if os.path.exists(log_path):
            with open(log_path, "r+")as file:
                old_data = file.read()
                new_data = "%s: download %s %s\n" % (download_date, result, download_url)
                file.seek(0, 0)
                file.write(new_data + old_data)
        else:
            with open(log_path, "w")as file:
                data = "%s: download %s %s\n" % (download_date, result, download_url)
                file.write(data)

    def write_sample(self, sample_path, sample_download_url):
        session = self.get_session()
        if os.path.exists(sample_path):
            return True
        else:
            # init_length = 0
            try:
                responese = session.get(url=sample_download_url, stream=True)
                # content_length = responese.headers["content-length"]
                with open(sample_path, "wb")as file:
                    for chunk in responese.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                            # init_length = init_length + len(chunk)
                            # print("\r%s %s/%s" % (sample_path, init_length, content_length), end="")
                return True
            except:
                return False

    def start_download(self):
        download_date = self.get_download_date()
        download_name = "%s.zip" % download_date
        download_path = os.path.join(download_folder, "urlhaus[infected]%s" % download_name)
        download_url = "https://urlhaus-api.abuse.ch/downloads/%s" % download_name
        download_result = self.write_sample(download_path, download_url)
        copy_result = os.popen("copy %s %s" % (download_path, dist_dir)).read()
        self.write_log(download_date, download_result, download_url)
        self.write_log(download_date, copy_result, "-----")


if __name__ == "__main__":
    while True:
        date_now = datetime.datetime.now()
        if date_now.strftime("%H%M%S") == "020000":
            Urlhaus().start_download()
        # elif os.path.exists(test_file):
        #     Urlhaus().start_download()
        #     if os.path.exists(test_file):
        #         os.remove(test_file)


