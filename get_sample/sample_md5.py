import os
import datetime
import requests

sample_folder = os.getcwd()
copy_folder = r"\\192.168.1.36\e\md5auto\upload\md5"


class SampleMd5:

    @staticmethod
    def get_session():
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        headers = {"User-Agent": user_agent}
        session = requests.session()
        session.headers.update(headers)
        return session

    @staticmethod
    def get_date(days=1):
        today = datetime.datetime.today()
        time_interval = datetime.timedelta(days=days)
        download_day = today - time_interval
        return download_day.strftime("%Y-%m-%d")

    @staticmethod
    def copy_file(resource_path, dist_path):
        command = "copy \"%s\" \"%s\"" % (resource_path, dist_path)
        os.system(command)

    @staticmethod
    def write_md5(md5):
        download_date = SampleMd5.get_date()
        md5_file_path = os.path.join(sample_folder, r"%s.txt" % download_date)
        if os.path.exists(md5_file_path):
            with open(md5_file_path, "r+")as file:
                old_data = file.read()
                file.seek(0, 0)
                file.write(md5 + "\n" + old_data)
        else:
            with open(md5_file_path, "a+")as file:
                file.seek(0, 0)
                file.write(md5 + "\n")
        return md5_file_path

    @staticmethod
    def md5_hybrid():
        md5_dict = {}
        headers = {"User-Agent": "Falcon Sandbox"}
        session = requests.session()
        session.headers.update(headers)
        url = "https://www.hybrid-analysis.com/feed?json"
        response = session.get(url).json()
        for info in response["data"]:
            md5_dict[info["md5"]] = ""
        return md5_dict

    @staticmethod
    def md5_virussign():
        md5_dict = {}
        download_date = SampleMd5.get_date(1)
        session = SampleMd5.get_session()
        session.auth = ("infected", "infected")
        url = "http://virusign.com/get_hashlist.php"
        params = {
            "md5": "",
            "n": "ANY",
            "start_date": download_date,
            "end_date": download_date
        }
        response = session.get(url, params=params).text
        for md5 in response.split("\n"):
            md5 = md5.replace("\"", "")
            md5_dict[md5] = ""
        return md5_dict

    @staticmethod
    def md5_virusshare():
        url = "https://virusshare.com/hashes/VirusShare_00357.md5"

    @staticmethod
    def get_all_md5():
        download_date = SampleMd5.get_date()
        md5_file_path = os.path.join(sample_folder, r"%s.txt" % download_date)
        md5_dict = {**SampleMd5.md5_virussign(), **SampleMd5.md5_hybrid()}
        with open(md5_file_path, "a+")as file:
            for md5 in md5_dict:
                file.write(md5 + "\n")
        SampleMd5.copy_file(md5_file_path, copy_folder)


if __name__ == "__main__":
    SampleMd5()

