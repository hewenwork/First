import os
import datetime
import requests

base_dir = os.getcwd()
log_path = os.path.join(base_dir, "urlhaus.log")
dist_dir = r"\\192.168.1.39\f\Auto"


class Urlhaus:

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

    @staticmethod
    def write_log(result, download_url):
        download_date = Urlhaus.get_download_date()
        data = "%s: download %s %s\n" % (download_date, result, download_url)
        if os.path.exists(log_path):
            with open(log_path, "r+")as file:
                old_data = file.read()
                file.seek(0, 0)
                file.write(data + old_data)
        else:
            with open(log_path, "a+")as file:
                file.write(data)

    @staticmethod
    def write_sample(file_path, download_url):
        session = Urlhaus.get_session()
        response = session.get(url=download_url, stream=True)
        with open(file_path, "wb")as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        return True

    @staticmethod
    def start_download():
        download_date = Urlhaus.get_download_date()
        download_name = "%s.zip" % download_date
        file_path = os.path.join(base_dir, "urlhaus[infected]%s" % download_name)
        download_url = "https://urlhaus-api.abuse.ch/downloads/%s" % download_name
        download_result = Urlhaus.write_sample(file_path, download_url)
        if download_result:
            os.popen("copy %s %s" % (file_path, dist_dir)).read()
            Urlhaus.write_log("success", download_url)
        else:
            Urlhaus.write_log("failed", download_url)


if __name__ == "__main__":
    start_date = input(u"Set the start time like 080000\n")
    while True:
        now_date = datetime.datetime.now().strftime("%H%M%S")
        today_date = datetime.datetime.today()
        if now_date == start_date:
            print("start download")
            Urlhaus().start_download()
            print("\r{}\ndownload over, wait for next time".format(today_date), end="")





