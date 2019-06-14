import os
import datetime
import requests
from subprocess import check_output, SubprocessError


class Urlhaus:

    def __init__(self):
        self.base_dir = os.getcwd()
        self.dist_dir = r"\\192.168.1.39\f\Auto"
        self.session = self.get_session()
        self.download_date = self.get_download_date()

    @staticmethod
    def get_session():
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        headers = {"User-Agent": user_agent}
        session = requests.session()
        session.headers.update(headers)
        return session

    @staticmethod
    def get_download_date():
        today = datetime.datetime.today()
        date_interval = datetime.timedelta(days=1)
        download_day = today - date_interval
        return download_day.strftime("%Y-%m-%d")

    def write_log(self, result, download_url):
        log_path = os.path.join(self.base_dir, "urlhaus.log")
        data = "%s: download %s %s\n" % (self.download_date, result, download_url)
        if os.path.exists(log_path):
            with open(log_path, "r+")as file:
                old_data = file.read()
                file.seek(0, 0)
                file.write(data + old_data)
        else:
            with open(log_path, "a+")as file:
                file.write(data)

    def write_sample(self, file_path, download_url):
        try:
            file_size = 0
            response = self.session.get(url=download_url, stream=True)
            file_total_size = int(response.headers["content-length"])
            with open(file_path, "wb")as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
                    file_size += 1024
                    download_process = int(file_size/file_total_size*100)
                    print("\rDownload %s %s%%" % ("#"*download_process, download_process), end="")
            return "Successful"
        except requests.RequestException as e:
            print(e)
            return "Failed"

    def start_download(self):
        file_name = "%s.zip" % self.download_date
        file_path = os.path.join(self.base_dir, "urlhaus[infected]%s" % file_name)
        download_url = "https://urlhaus-api.abuse.ch/downloads/%s" % file_name
        download_result = self.write_sample(file_path, download_url)
        try:
            command = "copy %s %s" % (file_path, self.dist_dir)
            check_output(command)
        except SubprocessError as e:
            print(e)
        self.write_log(download_result, download_url)


if __name__ == "__main__":
    Urlhaus().start_download()






