import os
import requests


class Ico:

    def __init__(self):
        user_dir = os.path.join(os.path.expanduser("~"), r"AppData\Local\Temp")
        self.ico_path = os.path.join(user_dir, "ico.ico")
        self.get_ico_path()

    def get_ico_path(self):
        if os.path.exists(self.ico_path):
            return self.ico_path
        else:
            self.download_ico()
            return self.ico_path

    def download_ico(self):
        url = "https://raw.githubusercontent.com/hewenwork/First/master/icon/ico.ico"
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"}
        session = requests.session()
        session.headers.update(headers)
        try:
            file_size = 0
            content = session.get(url, stream=True, timeout=10)
            file_total_size = int(content.headers["content-length"])
            with open(self.ico_path, "wb")as file:
                for chunk in content.iter_content(chunk_size=1024):
                    file.write(chunk)
                    file_size += 1024
                    download_process = int(file_size / file_total_size * 100)
                    print("\rDownload Ico:%s %s%%" % ("#" * download_process, download_process), end="")
            return self.ico_path
        except requests.RequestException as e:
            print(e)

