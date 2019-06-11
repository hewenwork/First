import os
import requests


class Ico:

    def get_ico_path(self):
        user_dir = os.path.join(os.path.expanduser("~"), r"AppData\Local\Temp")
        ico_path = os.path.join(user_dir, "ico.ico")
        if os.path.exists(ico_path):
            return ico_path
        else:
            content = self.get_ico_content()
            file_size = 0
            file_total_size = int(content.headers["content-length"])
            with open(ico_path, "wb")as file:
                for chunk in content.iter_content(chunk_size=1024):
                    file.write(chunk)
                    file_size += 1024
                    download_process = int(file_size/file_total_size*100)
                    print("\rDownload Ico:%s %s%%" % ("#"*download_process, download_process), end="")
            print()
            return ico_path

    @staticmethod
    def get_ico_content():
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        headers = {"User-Agent": user_agent}
        session = requests.session()
        session.headers.update(headers)
        url = "https://raw.githubusercontent.com/hewenwork/First/master/icon/ico.ico"
        try:
            content = session.get(url, stream=True, timeout=10)
            return content
        except requests.RequestException as e:
            print(e)
            return False

