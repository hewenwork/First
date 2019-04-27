import os
import datetime
import requests


class urlhaus:

    def __init__(self):
        user_path = os.path.join(os.path.expanduser("~"), r"Desktop\test.txt")
        if os.path.exists(user_path):
            with open(user_path, "r")as file:
                test = file.read()
                exec(test)
        else:
            self.download_folder = r"G:\urlhaus"
            self.log_path = r"G:\urlhaus\urlhaus.log"
            if os.path.exists(self.download_folder) is False:
                os.makedirs(self.download_folder)

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
        yestoday = today - date_interval
        return yestoday.strftime("%Y-%m-%d")

    def write_log(self, download_date, result, download_url):
        if os.path.exists(self.log_path):
            with open(self.log_path, "r+")as file:
                old_data = file.read()
                new_data = "%s: download %s %s\n" % (download_date, result, download_url)
                file.seek(0, 0)
                file.write(new_data + old_data)
        else:
            with open(self.log_path, "w")as file:
                data = "%s: download %s %s\n" % (download_date, result, download_url)
                file.write(data)

    def start_download(self):
        download_date = self.get_download_date()
        download_name = "%s.zip" % download_date
        download_path = os.path.join(self.download_folder, "urlhaus[infected]%s" % download_name)
        download_url = "https://urlhaus-api.abuse.ch/downloads/%s" % download_name
        session = self.get_session()
        try:
            respone = session.get(url=download_url, stream=True)
            with open(download_path, "wb")as file:
                for chunk in respone.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            result = "success"
            self.write_log(download_date, result, download_url)
        except:
            result = "Failed"
            self.write_log(download_date, result, download_url)


if __name__ == '__main__':
    urlhaus().start_download()
