import os
import re
import time
import shutil
import hashlib
import datetime
import requests
from bs4 import BeautifulSoup
from contextlib import closing


class get_sample:

    def __init__(self):
        start_dir = r"F:\auto_collect"
        self.session = self.get_session()
        self.download_date = self.get_download_date()
        self.download_folder = os.path.join(start_dir, self.download_date)
        self.failed_log = os.path.join(start_dir, r"下载失败.txt")
        self.log_file = os.path.join(start_dir, r"下载日志.log")
        self.failed_num = 0
        self.success_num = 0
        if os.path.exists(self.download_folder) is False:
            os.makedirs(self.download_folder)

    @staticmethod
    def get_download_date():
        today = datetime.datetime.today()
        time_interval = datetime.timedelta(days=1)
        yestoday = today - time_interval
        return yestoday.strftime("%Y-%m-%d")

    @staticmethod
    def get_session():
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        headers = {"User-Agent": user_agent}
        session = requests.session()
        session.headers.update(headers)
        return session

    def write_download_log(self, target):
        log_file = r"F:\auto_collect\下载日志.log"
        if os.path.exists(log_file):
            with open(log_file, "r+")as file:
                old_data = file.read()
                new_data = u"%s: %s :失败%s, 成功%s\n" % (self.download_date, target, self.failed_num, self.success_num)
                file.seek(0, 0)
                file.write(new_data + old_data)
        else:
            with open(log_file, "a")as file:
                data = u"%s: %s :失败%s, 成功%s\n" % (self.download_date, target, self.failed_num, self.success_num)
                file.write(data)

    def write_failed_info(self, failed_info):
        if os.path.exists(self.failed_log):
            if len(failed_info) == 64:
                with open(self.failed_log, "r+")as file:
                    old_data = file.read()
                    new_data = "%s\n" % failed_info
                    file.write(new_data + old_data)
            else:
                with open(self.failed_log, "a+")as file:
                    file.writelines("%s\n" % failed_info)
        else:
            with open(self.failed_log, "wb")as file:
                data = "%s\n" % failed_info
                file.write(data)

    def write_sample(self, sample_name, sample_download_url):
        file_path = os.path.join(self.download_folder, sample_name)
        try:
            with closing(self.session.get(sample_download_url, stream=True, timeout=10))as response:
                if response.status_code == 200 and os.path.exists(file_path) is False:
                    download_timeout = 120
                    start_time = time.time()
                    with open(file_path, "wb")as file:
                        for chunk in response.iter_content(chunk_size=1204):
                            end_time = time.time()
                            if end_time < start_time + download_timeout:
                                file.write(chunk)
                            else:
                                os.remove(file_path)
                                break
                    return True
                elif os.path.exists(file_path):
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
            respone = self.session.get(url=url)
            if respone.status_code == 200:
                suop = BeautifulSoup(respone.text, "lxml")
                suop_url = suop.select("tr > td:nth-of-type(2) > a:nth-of-type(2)")
                suop_md5 = suop.select("tr > td:nth-of-type(3) > a")
                sample_md5_list = [sample_md5.getText() for sample_md5 in suop_md5]
                sample_url_list = ["http://vxvault.net/%s" % sample_info.get("href") for sample_info in suop_url]
                for sample_url, sample_md5 in zip(sample_url_list, sample_md5_list):
                    try:
                        sample_respone = self.session.get(url=sample_url).text
                        sample_add_date = re.findall("Added:<\/B> (.*?)<BR>", sample_respone)[0]
                        sample_name = sample_md5 + ".vir"
                        sample_download_url = re.findall("Link:<\/B> (.*?)<BR>", sample_respone)[0].replace("hxxp:",
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
            self.write_download_log("(错误: 访问主页出错) " + url)

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
                self.write_download_log("(错误: 今日无资源) " + "www.malware-traffic-analysis.net")
        except:
            self.write_download_log("(错误: 访问主页超时)" + "www.malware-traffic-analysis.net")

    def sample_virusbay(self):
        url = "https://beta.virusbay.io/login"
        data = {
            "email": "niwangxiu@gmail.com",
            "password": "testvirus0504L"
        }
        try:
            respone = self.session.post(url, data=data)
            token = respone.json()["token"]
            Authorization = {"Authorization": "JWT %s" % token}
            self.session.headers.update(Authorization)
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
                    self.session.headers.update(Authorization)
                elif add_date < self.download_date:
                    break
            self.write_download_log("www.malware-traffic-analysis.net")
        except:
            self.write_download_log(u"(错误: 登陆失败) " + "www.malware-traffic-analysis.net")

    def sample_virussign(self):
        self.session.auth=("infected", "infected")
        url = "http://virusign.com/get_hashlist.php"
        params = {
            "sha256": "",
            "n": "ANY",
            "start_date": self.download_date,
            "end_date": self.download_date
        }
        try:
            respone = self.session.get(url, params=params).text
            for sha256 in respone.split("\n"):
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
            self.write_download_log("(错误: 获取JSON文件错误)" + "http://virusign.com")

    def sample_malshare(self):
        api_key = "2befc1c0b4d476b8527887f3f415648050638eff8dd400071f694e7356d5e49a"
        url = "https://malshare.com/api.php"
        params = {
            "api_key": api_key,
            "action": "getlist"
        }
        try:
            respone = self.session.get(url=url, params=params).json()
            for sample_info in respone:
                sample_md5 = sample_info["md5"]
                sample_name = sample_md5 + ".vir"
                sample_download_url = "https://malshare.com/api.php?api_key=%s&action=getfile&hash=%s" % (api_key, sample_md5)
                if self.write_sample(sample_name, sample_download_url):
                    self.success_num += 1
                else:
                    self.failed_num += 1
                    self.write_failed_info(sample_md5)
            self.write_download_log("https://malshare.com")
        except:
            self.write_download_log("(错误: 获取JSON文件失败) " + "https://malshare.com")

    def sample_hybird(self):
        user_data = {
            "User-Agent": "Falcon Sandbox",
            "api-key": "0ccgsgk0w00w4ogwcgk4o4s0ggw8gg4og04wsko8kw4s8wgocks400cgsg88400g"
        }
        self.session.headers.update(user_data)
        url = "https://www.hybrid-analysis.com/api/v2/feed/latest"
        try:
            sample_data = self.session.get(url).json()["data"]
            for sample in sample_data:
                if sample["threat_level"] != 0:
                    sha256 = sample["sha256"]
                    sample_name = sha256 + ".vir.gz"
                    sample_download_url = "https://www.hybrid-analysis.com/api/v2/overview/%s/sample" % sha256
                    if self.write_sample(sample_name, sample_download_url):
                        self.success_num += 1
                        time.sleep(15)
                    else:
                        self.failed_num += 1
                        self.write_failed_info(sha256)
            self.write_download_log("www.hybrid-analysis.com")
        except:
            self.write_download_log("(错误:获取JSON数据出错)" + "www.hybrid-analysis.com")

    def sample_infosec(self):
        for page in range(50):
            url = "https://infosec.cert-pa.it/analyze/submission-page-%s.html" % page
            try:
                respone = self.session.get(url)
                date_list = BeautifulSoup(respone.text, "lxml").select("tr > td:nth-of-type(1)")
                md5_list = BeautifulSoup(respone.text, "lxml").select("tr > td:nth-of-type(3)")
                for add_date, sample in zip(date_list, md5_list):
                    add_date = add_date.getText()[:10]
                    sample_md5 = sample.getText()
                    sample_name = sample_md5 + ".vir"
                    md5_url = "https://infosec.cert-pa.it/analyze/%s.html" % sample_md5
                    if add_date == self.download_date:
                        try:
                            file_respone = self.session.get(md5_url).text
                            sample_download_url = "http%s" % (re.findall(">hXXp(.*?)<", file_respone)[0]).replace("]", "").replace("[", "")
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
                self.write_download_log("(错误: 访问超时)" + "https://infosec.cert-pa.it")
                break
        self.write_download_log("https://infosec.cert-pa.it")

    def sample_malc0de(self):
        url = "http://malc0de.com/database/"
        try:
            respone = self.session.get(url)
            if respone.status_code == 200:
                suop = BeautifulSoup(respone.text, "lxml")
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
            else:
                self.write_download_log("(错误:没有链接VPN) " + "http://malc0de.com")
        except:
            self.write_download_log("(错误:没有链接VPN) " + "http://malc0de.com")

    def start_download(self):
        get_sample().sample_vxvault()
        get_sample().sample_malware_traffic_analysis()
        get_sample().sample_virusbay()
        get_sample().sample_virussign()
        get_sample().sample_malshare()
        get_sample().sample_hybird()
        # get_sample().sample_infosec()
        get_sample().sample_malc0de()
        return self.download_folder


class final_deal:

    def __init__(self):
        self.local_rar_path = r"C:\Program Files\WinRAR"
        self.local_7z_path = r"C:\Program Files\7-Zip"
        self.compression_failed_folder = r"F:\auto_collect\解压失败"
        self.rename_failed_folder = r"F:\auto_collect\重命名失败"
        self.smartccl_folder = r"\\192.168.1.39\f\Auto"

    @staticmethod
    def get_file_md5(file_path):
        try:
            with open(file_path, 'rb')as md5_file:
                md5_con = hashlib.md5()
                md5_con.update(md5_file.read())
                md5_result = str(md5_con.hexdigest()).upper()
                return md5_result
        except:
            return False

    def rename_file(self, file_path):
        file_md5 = self.get_file_md5(file_path)
        if file_md5:
            file_dir = os.path.dirname(file_path)
            new_file_name = file_md5 + ".vir"
            new_file_path = os.path.join(file_dir, new_file_name)
            if file_path != new_file_path and os.path.exists(new_file_path)is False:
                os.rename(file_path, new_file_path)
                return True
            elif file_path != new_file_path and os.path.exists(new_file_path):
                os.remove(file_path)
                return True
            elif file_path == new_file_path:
                return True
        else:
            shutil.move(file_path, self.rename_failed_folder)

    def rename_all(self, folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            file_size = os.path.getsize(file_path)
            if file_size < 1024:
                try:
                    if os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    elif os.path.isfile(file_path):
                        os.remove(file_path)
                except:
                    shutil.move(file_path, self.rename_failed_folder)
            else:
                result = self.rename_file(file_path)
                if result is False:
                    shutil.move(file_path, self.rename_failed_folder)

    def decompression(self, file_path):
        password = "infected"
        dir_path = os.path.dirname(file_path)
        command_dict = {
            ".gz": [self.local_7z_path, "7z e -tgzip -p%s -y \"%s\" -o%s" % (password, file_path, dir_path)],
            "zip": [self.local_7z_path, "7z e -tzip -p%s -y \"%s\" -o%s" % (password, file_path, dir_path)],
            ".7z": [self.local_7z_path, "7z e -t7z -p%s -y \"%s\" -o%s" % (password, file_path, dir_path)],
            "rar": [self.local_rar_path, "rar e -p%s -y \"%s\" %s" % (password, file_path, dir_path)]
        }
        file_type = file_path[-3:]
        if file_type in command_dict.keys():
            try:
                compression_path = command_dict[file_type][0]
                command = command_dict[file_type][-1]
                os.chdir(compression_path)
                result = os.popen(command).read()
                if "OK" in result.upper():
                    return True
                else:
                    return False
            except:
                return False
        else:
            return None

    def decompression_all(self, folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            result = self.decompression(file_path)
            if result is True:
                os.remove(file_path)
            elif result is False:
                shutil.move(file_path, self.compression_failed_folder)
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            result = self.decompression(file_path)
            if result is True:
                os.remove(file_path)
            elif result is False:
                shutil.move(file_path, self.compression_failed_folder)

    def compression_folder(self, folder_path):
        try:
            password = "infected"
            result_path = folder_path + "[infected].rar"
            command = "rar a -ep -p%s %s %s" % (password, result_path, folder_path)
            os.chdir(self.local_rar_path)
            result = os.popen(command).read()
            if "OK" in result.upper():
                return result_path
            else:
                return False
        except:
            return False

    def compression_delete_rename_compression_move(self, folder_path):
        self.decompression_all(folder_path)
        self.rename_all(folder_path)
        result_path = self.compression_folder(folder_path)
        os.popen("copy %s[infected].rar %s" % (result_path, self.smartccl_folder))


class virustotal:

    def __init__(self):
        pass

    @classmethod
    def get_api_list(cls):
        api_list = ["706b1ba7ca5cccacd694a0ad413355c0f7c79e69879dad761c0af972d96c4a4b",
                    "f567f0b7f9dc9ca33c7b2a915132182b3d0aa2041d8152a673d2c537262a4b59",
                    "c9c25db562e33cbd035d3bee5dacf7f29c16e9cf2a6876eb8ebdc448c1299783",
                    "fac93fc5e0a003d4dbeebd01c816e19b11d5277bcad1621a68c6d734c9bcc7d8",
                    "65eff1d41d939e788a954153b66373cb7f9cdf0da4d73cbc14df335852493422",
                    "40421da302a6e45c3e955fe0f1d76924cfa49467133aafea42f542c630a5319f",
                    "82b4902ff87fbcf639f6111ba3f071d96ff0b2a12f49c59b0d2855f79e24d8ff",
                    "ea29708b3537d44ed0128153c637ee6885f40d1904c4cb8380be9cc0b6efe645",
                    "5bf0eda5eb7a809a8b608c9bfaef388824ba8516f7a6d8c426e0ccec6c01ac4f",
                    "fc1d01c033379b5b86e117479108a212349d1fa57c945b89b7dd2fc740d600be",
                    "5046773a6aae5773f29fb28ee91921d09c7de1495de6cbd40bfb1fa1cf7631d6",
                    "fbfe18a11027d5e4e789b811def7c11d0b1b75594fe0eb8921d95a2851bac931",
                    "1b0e1d01e17868beecc14a4dfb7f22d2fef06706f93b554d2b4ba1b800a55603",
                    "6b3f5de93d93206aa4889c181cdf5b7002ac865b810069db397d312bbf4e42f0",
                    "91bad4a656720e1de7537be04f464f8062989dbc08ec51c4c4d654d6d97f4281",
                    "37f81e01da6e9d6f4e31371492e4cde03e50b131c2e6accfcdee124c930e003d",
                    "3507c4aa288448a73310cda1e33bb19de2b47c8fd4c902c19f2e407b71e09ac2",
                    "6017361002eb8477100d61115e18f9ba65d064fe6202a3bd84bcc14efcb5e782",
                    "70fec267ef56a12afaba9e190a0c3f7e0945369f54a81020ba79742525a3d788",
                    "37d6f523beb706a23226cc8903c3d2451076ee27c7e6f16eed50d671703494f1",
                    "ae992f62476015ddfc7493af71e4a7f3cee9fa295dedd912c2233d9876c088f4",
                    "c1a490ee725534df6ad7a2d87c1c51aa85a4d8857b7bfca535b8e841efcbceb4",
                    "2035f0c619d9174d5ec2c524da6d324c78f5226c828b388d739ebd208e2e0057",
                    "a91830d649b6401bd8bbf93af2ae03a4ef144a9099b2d86865302601b67b2e50",
                    "c5f366a6454a6873a6c933056639eda3bb2f6258ea9b0681b8a7e0ba92ff7f92",
                    "5a0b7111a31b1a087707e77b9af670a5fe13ad22a7e7546974aeeb31da5f88fd",
                    "c236ee12022a624992842f087a2f70ebd8ae3655bbc070ba08f67010cd416da8",
                    "6b7d3a0cd0d4a5774c45fd4e63bdcdcb0e40702e0f1a64c839f7ae0f4630c8b9",
                    "1924ded88606de6418aa9755c3fdca58c1a07ad29eee84c0408f5a7a8e874491",
                    "3f63fa9db75c4b0639e6ffd77b94c0348bb57b93eff84a92f4c188cb38113e5b",
                    "6400437961db158b192c1164e14f77e3a74498cdee61cffab5f15b6fbdba30a1",
                    "e340e830b8fd5b8de38c105ada4dd08e0e5209e015649b4f5ba460382d35a6f1",
                    "c6d86db4898f79f20da8d5ef37c213669624fddb3c2e6cdb0a7839e95970c0bd",
                    "ae0f1ea6e927b48da938a443a659be360107c529b8fce92a065c21f463bb1ef0",
                    "69c7530121cb0ec667c8a7efb7ea49339bc0288e6394b16890883fe6888adf10",
                    "4561a6189e6f432e9f886636af119d7cdc6d2e110ddf064fe7a21304eea50898",
                    "c156de20bc8685af1a8aad33f5964e9224b450db2ada42584a268af28a8bc450",
                    "e2fd0cd961bdeaf2d054871299a6c2f056d7a5dbda813b93000a81a64087b341",
                    "ac8be0c9088ed1020bfcd4448a1028e1ec879acfd3f41141c961b7690a1e956b",
                    "656961bd78c2435b25f3aeae2057d14684f13d6f89242e42d782a255f8272ae9",
                    "bf33b55b49c2b8fe06dca09e114e2226cffcac2d214f8c8cd92a976e7f0fe696",
                    "fb007f45821a070fe8c60fbab00e38f43e27d218b63b281eceeebfa24b682b40",
                    "ebb69c2b5fc6bd3f67ff36f28c66cd489e025a321fb0f4e40c985c34e97c9b09s",
                    "e63fff6ec2f1d351b56e263e6903cf7199ecba26bd01046c69f4f92b3d79d09e",
                    "6172001af0588434c0ff9d7d78da7b1556939a252709f663987fa3bcbc7009ce",
                    "ae52dc0bf7fb17444515f9911e243d03442ac4bf9448aa44dc6f3cf6f88a1fad",
                    "6e58eb435d8eb9e137ce7cb9c63ffce33081e9dababd094c2fcdfc4647139086",
                    "010696052677d9f1962e8a1de5cb22e1ddeed5ed854ab6eae6836de2d1a6498e",
                    "cdd061806b4cc5264b8fde9cb61c9093d3396a6bafb7b77bda27a208d8cc1804",
                    "9bfb9694197e0812e6fc735fc90eb21b4e3e6dd1f058ad452b5b48df4ea70dd9",
                    "6fcd7437a39b77c405601a83c02a16d882b7c258a82b24499cd1660cc428df3a",
                    "92bb1fdbb853890322be3291b2955135d9479e1307f3fe1af8aba403843e8cc8",
                    "286087a0e2c1d52e66126467807d9ec33d0a1ba15148e2280252ad060e50f501",
                    "b847e5bc4203cdb8245f5d6c8ab5e8606b31a73ef268f3ab474da288a419b8aa",
                    "3f8ef86651609fb3fda4134d6433762efa5bbc30ca1cd1b491c584e410a1d384",
                    "d8ac8c77f6c3b297750c0ba92484f06a8037075049ff79101b921d6d36104559",
                    "a7450f5a40fccd2d761d83593ce8f918960b49de12b6ec172759ab485591fa71",
                    "5926cc5a2d8ff785ba7973228aa5053183d61111d02c9a0a6a98ea76c05f8ac7",
                    "de25ed07259c081b8bd873a8248022c6c138419f95339cea8eecf02313d7f6e0",
                    "ee07787779550e5031d061220fd30eb504ac7bceac820736005c878acba5f15b",
                    "2243746e5f13d38e8907355aa543b9eeb53a9a5df02c07f976ee03fc4f086781",
                    "a5efd48f0b928a7a77ba0c20e803991d3ebe50add87a97e7a680cd802e64bc88",
                    "6c78677baf1f91105bd165578eb4ed36b702ee52b5aba06a9c22d54c52d98d8d",
                    "b9b4d1cf70ad6c849df565e9b4fc11dbc508d915332a42a9cbca175c76097b7c",
                    "626f13733c1ab37b459fe2b362a9d9c037822be429c3a8b59ec89a6631b2a55b",
                    "5dc4d2be4a434cd2b7abc651cb3e9a09ec311770cd8474310ab0d91445d466ec",
                    "27ef571e4443ffc42395e69a939106a7f8740951c83aecb14d63959ea779b7ea",
                    "d09dca26deddad1aadeb767f2762b80c6e0570596b5671a0e32c70afa4a853c9",
                    "809886425d3c5e955849890d3ac2c235f63cebd57aff0454fd5d5fe98160c559",
                    "6d3305d504ccd66c95fb23de209aabbef50793746e9bed97cb46a5ad3be3d1a9",
                    "392ff7ebbfee647c2141e7b4ac4c9ee3d7242608a4ff8b56ba943daf2b40c4a6",
                    "0106dfd35f87f68df9cd3a6fb5decd71de0f6dba6c954fc4d7003ed152b4279d",
                    "78c0d9b5d93eec1a6118d0c27c05d2cf43ca1b1d8f85a5b64491134781b8a5c0",
                    "33a9068c3937d8e17846767c8c344ff4f932140704362e2546d2c4dc5d85e436",
                    "a5424fa7a0b9a81d2b11845dba0a694da2a9763e06fb9392e6d2af59469a1fd8",
                    "40dde2e5940bccd39ec8a3af05c2ce46cc4aa7ad4f2599d9eab832b6fbfd5661",
                    "d5a63233aa9309c2d53f15bf945e01ffccaea56727f87ed2e2779e686b3aa758",
                    "ca8073c043cc387b585657e17f8c8ea9fa3dcec37679403aec98b76a77e439ae",
                    "9d75fb43e225104caaf9ff567b13969850ee132dc0842158cec82cd397dca5f5",
                    "c6225b29a41a9084271387b16130332efb838003fdcd6b6bb1001c1e07dbc230"]
        return api_list

    @classmethod
    def get_session(cls):
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        headers = {"User-Agent": user_agent}
        session = requests.session()
        session.headers.update(headers)
        return session

    @classmethod
    def imf_rule(cls, report_json):
        if report_json["positives"] >= 15:
            return True
        else:
            init_num = 0
            anti_virus = ["Avast", "Avira", "AVG", "F-Secure", "Kaspersky", "McAfee", "VIPRE", "BitDefender", "Comodo",
                          "Microsoft", "Panda", "TrendMicro-HouseCall"]
            for i in anti_virus:
                if i in report_json["scans"]:
                    if report_json["scans"][i]["detected"] is True:
                        init_num += 1
            if init_num >= 5:
                return True
            else:
                return False

    @classmethod
    def get_report_json(cls, api, resouce):
        url = "https://www.virustotal.com/vtapi/v2/file/report"
        params = {
            "apikey": api,
            "resource": resouce
        }
        try:
            session = virustotal.get_session()
            respone = session.get(url, params=params).json()
            if respone["response_code"] != 0:
                return respone
            else:
                return False
        except:
            return False

    @classmethod
    def get_size(cls, permalink):
        try:
            session = virustotal.get_session()
            respone = session.get(permalink).text
            file_size = re.findall("File size</span>\n.*\\( (.*?) bytes \\)", respone)[0]
            if file_size is None:
                return False
            else:
                return file_size
        except:
            return False

    @classmethod
    def deal_file(cls, file_path):
        md5_info_list = []
        old_file = open(file_path, "r")
        old_data = old_file.read().split("\n")
        old_file.close()
        api_list = virustotal.get_api_list()
        api_len = len(api_list)
        with open(file_path, "w")as file:
            for resuoce in old_data:
                api = api_list[old_data.index(resuoce) % api_len]
                report_json = virustotal.get_report_json(api, resuoce)
                if report_json is not False:
                    md5 = report_json["md5"]
                    result = virustotal.imf_rule(report_json)
                    if result:
                        permalink = report_json["permalink"]
                        file_size = virustotal.get_size(permalink)
                        if file_size is not False:
                            md5_info = "Trojan.Generic,%s,%s\n" % (md5, file_size)
                            md5_info_list.append(md5_info)
            file.writelines(md5_info_list)


if __name__ == '__main__':
    test_file = os.path.join(os.path.expanduser("~"), r"Desktop\test.test")
    while True:
        date_now = datetime.datetime.now()
        if date_now.strftime("%H%M%S") == "020000":
            time.sleep(1)
            download_folder = get_sample().start_download()
            final_deal().compression_delete_rename_compression_move(download_folder)
        elif date_now.weekday() == 6 and date_now.strftime("%H%M%S") == "120000":
            resouce_path = r"F:\auto_collect\下载失败.txt"
            virustotal.deal_file(resouce_path)
            dist_path = r"C:\Users\hewen\Desktop\2019-04-14\MD5N%s.db" % date_now.strftime("%Y%m%d")
            os.popen("move %s %s" % (resouce_path, dist_path))
        elif os.path.exists(test_file):
            download_folder = get_sample().start_download()
            final_deal().compression_delete_rename_compression_move(download_folder)
            if os.path.exists(test_file):
                os.remove(test_file)

