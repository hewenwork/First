import os
import datetime
import requests


class Urlhaus:

    def __new__(cls, *args, **kwargs):
        today = datetime.datetime.today()
        date_interval = datetime.timedelta(days=1)
        download_day = today - date_interval
        cls.download_date = download_day.strftime("%Y-%m-%d")
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        cls.session = requests.session()
        cls.session.headers["User-Agent"] = user_agent
        cls.dist_dir = r"\\192.168.1.39\f\Auto"
        cls.download_dir = os.getcwd()
        return object.__new__(cls)

    def __init__(self, downlaod_date=None):
        if downlaod_date is not None:
            self.download_date = downlaod_date
        file_path = os.path.join(self.download_dir, f"urlhaus[infected]{self.download_date}.zip")
        download_url = f"https://urlhaus-api.abuse.ch/downloads/{self.download_date}.zip"
        download_result = self.write_sample(file_path, download_url)
        try:
            command = f"copy {file_path} {self.dist_dir}"
            os.system(command)
        except Exception as e:
            print(e)
        self.write_log(download_result, download_url)

    def write_log(self, result, download_url):
        log_path = os.path.join(self.download_dir, "DownloadHistory.log")
        data = f"{self.download_date}: download {result} {download_url}\n"
        with open(log_path, "a+")as file:
            file.write(data)

    def write_sample(self, file_path, download_url):
        start_size = 0
        chunk_size = 1024 * 1024
        try:
            response = self.session.get(url=download_url, stream=True)
            if response.status_code == 200:
                total_size = int(response.headers["content-length"])
                with open(file_path, "wb")as file:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        file.write(chunk)
                        start_size += 1024
                        download_process = int(start_size / total_size * 100)
                        print("\rDownload %s %s%%" % ("#" * download_process, download_process), end="")
                return "Successful"
            else:
                return "Today has`t Data"
        except requests.RequestException as e:
            return f"Failed: {e}"


if __name__ == "__main__":
    show_info = "Choose Download Mode:\nDownload Yestoday: 1\nDownload Everyday: 2\nDownload Assignation Date: 3\nMode:"
    download_mode = input(show_info)
    if download_mode == "1":
        Urlhaus()
    elif download_mode == "2":
        while True:
            date_now = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"\rNow time: {date_now}  Start time: 09:00:00", end="")
            if date_now == "09:00:00":
                print("Start Download\n")
                Urlhaus()
    elif download_mode == "3":
        assignation = input("Pls input assignation date like:2019-08-08\n")
        Urlhaus(downlaod_date=assignation)
    else:
        print("Pls input the Num of Download Mode")
