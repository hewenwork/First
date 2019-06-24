import os
import datetime
import requests


class VirusSign:

    def __init__(self):
        self.base_dir = os.getcwd()
        self.session = self.get_session()
        self.download_date = self.get_download_date()

    @staticmethod
    def get_session():
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        auth = ("infected", "infected")
        headers = {"User-Agent": user_agent}
        session = requests.session()
        session.headers.update(headers)
        session.auth = auth
        return session

    def get_sample_dict(self, download_date):
        download_dict = {}
        download_dir = os.path.join(self.base_dir, download_date)
        os.makedirs(download_dir)
        session = VirusSign.get_session()
        url = "http://virusign.com/get_hashlist.php"
        params = {
            "sha256": "",
            "n": "ANY",
            "start_date": download_date,
            "end_date": download_date
        }
        response = session.get(url, params=params).text
        for sha256 in response.split("\n")[:-1]:
            sha256 = sha256.replace("\"", "")
            sample_name = sha256 + ".7z"
            sample_path = os.path.join(download_dir, sample_name)
            sample_download_url = "http://virusign.com/file/%s" % sample_name
            download_dict[sample_path] = sample_download_url
        return download_dict

    def write_sample(self, file_path, download_url):
        if os.path.exists(file_path):
            return True
        else:
            try:
                response = self.session.get(download_url, timeout=5, stream=True)
                with open(file_path, "wb")as file:
                    file.write(response.content)
                return True
            except requests.RequestException as e:
                if os.path.exists(file_path):
                    os.remove(file_path)
                print(e)
                return False

    def get_download_date(self):
        start_date = "2012-02-02"
        end_date = "2019-04-01"

        for file_name in os.listdir(self.base_dir):
            file_path = os.path.join(self.base_dir, file_name)
            if os.path.isdir(file_path):
                if file_name > start_date and file_name[:2] == "20":
                    start_download_date = file_name
        download_date = datetime.datetime.strptime(start_download_date, "%Y-%m-%d") + datetime.timedelta(days=1)
        return download_date.strftime("%Y-%m-%d")

    @staticmethod
    def download_sample():
        download_date = VirusSign.get_start_download_date()
        sample_dict = VirusSign.sample_dict(download_date)
        session = VirusSign.get_session()
        for file_path, download_url in sample_dict.items():
            VirusSign.write_sample(session, file_path, download_url)


if __name__ == "__main__":
    VirusSign.download_sample()



