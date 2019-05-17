import os
import datetime
import requests
sample_dir = os.getcwd()
log_file = os.path.join(sample_dir, r"下载日志.log")


class VirusSign:

    @staticmethod
    def get_session():
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        auth = ("f_yunwing1", "9kkSkk3dSd")
        headers = {"User-Agent": user_agent}
        session = requests.session()
        session.headers.update(headers)
        session.auth = auth
        return session

    @staticmethod
    def get_download_date(days=1):
        today = datetime.datetime.today()
        date_interval = datetime.timedelta(days=days)
        download_date = today - date_interval
        return download_date.strftime("%Y%m%d")

    @staticmethod
    def write_log(result, download_url):
        download_date = VirusSign.get_download_date()
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

    @staticmethod
    def write_sample(download_path, download_url):
        session = VirusSign.get_session()
        if os.path.exists(download_path):
            start_size = os.path.getsize(download_path)
            response = session.get(url=download_url, stream=True)
            total_size = response.headers["content-length"]
            if abs(total_size - start_size) < 1024:
                return True
            else:
                session.headers.update({'Range': 'bytes=%d-' % start_size})
                response = session.get(url=download_url, stream=True)
                try:
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

    @staticmethod
    def start_download():
        download_date = VirusSign.get_download_date()
        download_name = "virussign.com_%s_Free.zip" % download_date
        download_path = os.path.join(sample_dir, download_name)
        download_url = "http://samples.virussign.com/samples/%s" % download_name
        result = VirusSign.write_sample(download_path, download_url)
        while result is False:
            result = VirusSign.write_sample(download_path, download_url)
        VirusSign.write_log("True", download_url)


if __name__ == '__main__':
    VirusSign.start_download()

