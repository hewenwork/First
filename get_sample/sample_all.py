import os
import re
import time
import datetime
import requests
from bs4 import BeautifulSoup
from get_sample import compresion
sample_dir = os.path.dirname(__file__)
failed_log = os.path.join(sample_dir, r"下载失败.txt")
log_file = os.path.join(sample_dir, r"下载日志.log")
test_file = os.path.join(os.path.expanduser("~"), r"Desktop\test.test")


class GetSample:

    def __init__(self):
        self.session = self.get_session()
        self.download_date = self.get_download_date()
        self.download_folder = os.path.join(sample_dir, self.download_date)
        if os.path.exists(self.download_folder) is False:
            os.makedirs(self.download_folder)
        self.failed_num = 0
        self.success_num = 0

    @staticmethod
    def get_download_date():
        today = datetime.datetime.today()
        time_interval = datetime.timedelta(days=1)
        download_day = today - time_interval
        return download_day.strftime("%Y-%m-%d")

    @staticmethod
    def get_session():
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        headers = {"User-Agent": user_agent}
        session = requests.session()
        session.headers.update(headers)
        return session

    @staticmethod
    def write_failed_info(failed_info):
        if os.path.exists(failed_log):
            if len(failed_info) == 64:
                with open(failed_log, "a+")as file:
                    new_data = "%s\n" % failed_info
                    file.write(new_data)
            else:
                with open(failed_log, "r+")as file:
                    old_data = file.read()
                    new_data = "%s\n" % failed_info
                    file.seek(0, 0)
                    file.write(new_data + old_data)
        else:
            with open(failed_log, "a+")as file:
                data = "%s\n" % failed_info
                file.write(data)

    def write_download_log(self, target):
        if os.path.exists(log_file):
            with open(log_file, "r+")as file:
                old_data = file.read()
                new_data = "%s: %s :Failed%s, Success%s\n" % (self.download_date, target, self.failed_num, self.success_num)
                file.seek(0, 0)
                file.write(new_data + old_data)
        else:
            with open(log_file, "a")as file:
                data = "%s: %s :Failed%s, Success%s\n" % (self.download_date, target, self.failed_num, self.success_num)
                file.write(data)

    def write_sample(self, sample_name, sample_download_url):
        file_path = os.path.join(self.download_folder, sample_name)
        if os.path.exists(file_path):
            return True
        else:
            try:
                response = self.session.get(sample_download_url, stream=True, timeout=10)
                if response.status_code == 200:
                    download_timeout = 120
                    start_time = time.time()
                    sample_file = open(file_path, "wb")
                    for chunk in response.iter_content(chunk_size=1024):
                        end_time = time.time()
                        if end_time < start_time + download_timeout:
                            sample_file.write(chunk)
                        else:
                            os.remove(file_path)
                            return False
                    sample_file.close()
                    return True
                else:
                    return False
            except:
                if os.path.exists(file_path):
                    os.remove(file_path)
                return False

    def sample_vxvault(self):
        url = "http://vxvault.net/ViriList.php"
        try:
            response = self.session.get(url=url)
            if response.status_code == 200:
                suop = BeautifulSoup(response.text, "lxml")
                suop_url = suop.select("tr > td:nth-of-type(2) > a:nth-of-type(2)")
                suop_md5 = suop.select("tr > td:nth-of-type(3) > a")
                sample_md5_list = [sample_md5.getText() for sample_md5 in suop_md5]
                sample_url_list = ["http://vxvault.net/%s" % sample_info.get("href") for sample_info in suop_url]
                for sample_url, sample_md5 in zip(sample_url_list, sample_md5_list):
                    try:
                        sample_respone = self.session.get(url=sample_url).text
                        sample_add_date = re.findall("Added:<\\/B> (.*?)<BR>", sample_respone)[0]
                        sample_name = sample_md5 + ".vir"
                        sample_download_url = re.findall("Link:<\\/B> (.*?)<BR>", sample_respone)[0].replace("hxxp:",
                                                                                                             "http:")
                        if sample_add_date == self.download_date:
                            if self.write_sample(sample_name, sample_download_url):
                                self.success_num += 1
                            else:
                                self.failed_num += 1
                                self.write_failed_info(sample_md5)
                        elif sample_add_date < self.download_date:
                            break
                    except:
                        pass
                self.write_download_log(url)
        except:
            self.write_download_log("(error: code404) " + url)

    def sample_malware_traffic_analysis(self):
        url = "http://www.malware-traffic-analysis.net/%s/index.html" % self.download_date.replace("-", "/")
        try:
            if self.session.get(url).status_code == 200:
                sample_suop = BeautifulSoup(self.session.get(url).text, "lxml").select("ul > li > a")
                for download_url in sample_suop:
                    if "-malware" in download_url.get("href"):
                        sample_download_url = url.replace("index.html", download_url.get("href"))
                        sample_name = download_url.get("href")
                        if self.write_sample(sample_name, sample_download_url):
                            self.success_num += 1
                        else:
                            self.failed_num += 1
                self.write_download_log("www.malware-traffic-analysis.net")
            else:
                self.write_download_log("(error: code501) " + "www.malware-traffic-analysis.net")
        except:
            self.write_download_log("(error: code404)" + "www.malware-traffic-analysis.net")

    def sample_virusbay(self):
        url = "https://beta.virusbay.io/login"
        data = {"email": "niwangxiu@gmail.com",
                "password": "testvirus0504L"}
        try:
            response = self.session.post(url, data=data)
            token = response.json()["token"]
            authorization = {"Authorization": "JWT %s" % token}
            self.session.headers.update(authorization)
            url = "https://beta.virusbay.io/sample/data"
            recent = self.session.get(url).json()["recent"]
            sample_md5_list = []
            sample_download_url_list = []
            for info in recent:
                add_date = info["publishDate"][:10]
                _id = info["_id"]
                sample_md5 = info["md5"]
                sample_name = sample_md5 + ".vir"
                url = "https://beta.virusbay.io/api/sample/%s/download/link" % _id
                sample_download_url = self.session.get(url).text
                sample_download_url_list.append(sample_download_url)
                sample_md5_list.append(sample_md5)
                if add_date == self.download_date:
                    del self.session.headers["Authorization"]
                    if self.write_sample(sample_name, sample_download_url):
                        self.success_num += 1
                    else:
                        self.failed_num += 1
                        self.write_failed_info(sample_md5)
                    self.session.headers.update(authorization)
                elif add_date < self.download_date:
                    break
            self.write_download_log("https://beta.virusbay.io")
        except:
            self.write_download_log(u"(error: log in failed) " + "https://beta.virusbay.io")

    def sample_virussign(self):
        self.session.auth = ("infected", "infected")
        url = "http://virusign.com/get_hashlist.php"
        params = {
            "sha256": "",
            "n": "ANY",
            "start_date": self.download_date,
            "end_date": self.download_date
        }
        try:
            response = self.session.get(url, params=params).text
            for sha256 in response.split("\n"):
                sha256 = sha256.replace("\"", "")
                sample_name = sha256 + ".7z"
                sample_download_url = "http://virusign.com/file/%s" % sample_name
                if self.write_sample(sample_name, sample_download_url):
                    self.success_num += 1
                else:
                    self.failed_num += 1
                    self.write_failed_info(sha256)
            self.write_download_log("http://virusign.com")
        except:
            self.write_download_log("(error : get JSON failed)" + "http://virusign.com")

    def sample_malshare(self):
        api_key = "2befc1c0b4d476b8527887f3f415648050638eff8dd400071f694e7356d5e49a"
        url = "https://malshare.com/api.php"
        params = {
            "api_key": api_key,
            "action": "getlist"
        }
        try:
            response = self.session.get(url=url, params=params).json()
            for sample_info in response:
                sample_md5 = sample_info["md5"]
                sample_name = sample_md5 + ".vir"
                sample_download_url = "https://malshare.com/api.php?api_key=%s&action=getfile&hash=%s" % (
                    api_key, sample_md5)
                if self.write_sample(sample_name, sample_download_url):
                    self.success_num += 1
                else:
                    self.failed_num += 1
                    self.write_failed_info(sample_md5)
            self.write_download_log("https://malshare.com")
        except:
            self.write_download_log("(error: get JSON failed) " + "https://malshare.com")

    def sample_hybird(self):
        user_data = {
            "User-Agent": "Falcon Sandbox",
            "api-key": "0ccgsgk0w00w4ogwcgk4o4s0ggw8gg4og04wsko8kw4s8wgocks400cgsg88400g"
        }
        self.session.headers.update(user_data)
        url = "https://www.hybrid-analysis.com/api/v2/feed/latest"
        try:
            sample_data = self.session.get(url).json()["data"]
            sample_sha256_list = [sample["sha256"] for sample in sample_data if sample["threat_level"] != 0]
            for sha256 in sample_sha256_list:
                sample_name = sha256 + ".vir.gz"
                sample_download_url = "https://www.hybrid-analysis.com/api/v2/overview/%s/sample" % sha256
                result = self.write_sample(sample_name, sample_download_url)
                if result:
                    self.success_num += 1
                    time.sleep(15)
                else:
                    self.failed_num += 1
                    time.sleep(15)
                    self.write_failed_info(sha256)
        except:
            self.write_download_log("(error: get JSON failed)" + "www.hybrid-analysis.com")
        self.write_download_log("www.hybrid-analysis.com")

    def sample_infosec(self):
        for page in range(50):
            url = "https://infosec.cert-pa.it/analyze/submission-page-%s.html" % page
            try:
                response = self.session.get(url)
                date_list = BeautifulSoup(response.text, "lxml").select("tr > td:nth-of-type(1)")
                md5_list = BeautifulSoup(response.text, "lxml").select("tr > td:nth-of-type(3)")
                for add_date, sample in zip(date_list, md5_list):
                    add_date = add_date.getText()[:10]
                    sample_md5 = sample.getText()
                    sample_name = sample_md5 + ".vir"
                    md5_url = "https://infosec.cert-pa.it/analyze/%s.html" % sample_md5
                    if add_date == self.download_date:
                        try:
                            file_respone = self.session.get(md5_url).text
                            sample_download_url = "http%s" % (re.findall(">hXXp(.*?)<", file_respone)[0]).replace("]",
                                                                                                                  "").replace(
                                "[", "")
                            if self.write_sample(sample_name, sample_download_url):
                                self.success_num += 1
                            else:
                                self.failed_num += 1
                                self.write_failed_info(sample_md5)
                        except:
                            self.write_failed_info(sample_md5)
                    elif add_date < self.download_date:
                        break
            except:
                self.write_download_log("(error: code404)" + "https://infosec.cert-pa.it")
                break
        self.write_download_log("https://infosec.cert-pa.it")

    def sample_malc0de(self):
        url = "http://malc0de.com/database/"
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                suop = BeautifulSoup(response.text, "lxml")
                sample_data_list = suop.select("tr > td:nth-of-type(1)")
                sample_url_list = suop.select("tr > td:nth-of-type(2)")
                sample_md5_list = suop.select("tr > td:nth-of-type(7)")
                for sample_data, sample_url, sample_md5 in zip(sample_data_list, sample_url_list, sample_md5_list):
                    add_data = sample_data.getText()
                    sample_download_url = "http://" + sample_url.getText()
                    sample_md5 = sample_md5.getText()
                    sample_name = sample_md5 + ".vir"
                    if add_data == self.download_date:
                        if self.write_sample(sample_name, sample_download_url):
                            self.success_num += 1
                        else:
                            self.failed_num += 1
                            self.write_failed_info(sample_md5)
                    elif add_data < self.download_date:
                        break
                self.write_download_log("http://malc0de.com")
        except:
            self.write_download_log("(error: VPN) " + "http://malc0de.com")
        self.write_download_log("(error: VPN) " + "http://malc0de.com")

    def start_download(self):
        GetSample().sample_vxvault()
        GetSample().sample_malware_traffic_analysis()
        GetSample().sample_virusbay()
        GetSample().sample_virussign()
        GetSample().sample_malshare()
        GetSample().sample_hybird()
        GetSample().sample_infosec()
        GetSample().sample_malc0de()
        return self.download_folder


if __name__ == '__main__':
    if os.path.exists(test_file):
        try:
            step1 = GetSample().start_download()
            # step2 = compresion.CompressionFunc().decompression_delete_rename_compression_move(step1)
        except:
            GetSample().write_download_log("jieyashibai")
        os.remove(test_file)
    while True:
        start = datetime.datetime.now().strftime("%H%M%S")
        if start == "030000":
            time.sleep(1)
            try:
                step1 = GetSample().start_download()
                # step2 = compresion.CompressionFunc().decompression_delete_rename_compression_move(step1)
            except:
                GetSample().write_download_log("jieyashibai")


