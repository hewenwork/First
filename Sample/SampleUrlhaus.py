# encoding = utf-8
# @Author: Hewen
# @Time: 1/22/2020 11:10 AM
# @File: SampleUrlHash.py
import os
import logging
import requests
from datetime import datetime, timedelta
from subprocess import check_output, SubprocessError

download_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")  # 样本下载日期
smart_dir = r"G:\Auto"  # 转移到smartccl位置
sample_dir = r"G:\urlhaus"  # 存放Sample
log_dir = os.path.join(sample_dir, "log")  # 存放下载日志

if os.path.exists(smart_dir) is False:
    os.makedirs(smart_dir)

if os.path.exists(sample_dir) is False:
    os.makedirs(sample_dir)

if os.path.exists(log_dir) is False:
    os.makedirs(log_dir)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/78.0.3904.108 Safari/537.36",
}
session = requests.session()
session.headers.update(headers)


def log_messeage():
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        **{
            "level": logging.INFO,
            "format": "%(asctime)s - %(lineno)s - %(message)s",
            "filename": f"{log_dir}\\log{datetime.now().date()}.txt"
        })
    logger.addHandler(logging.StreamHandler())
    return logger


log = log_messeage()


class SampleUrlHash:

    def __init__(self):
        file_path = os.path.join(sample_dir, f"[infected]UrlHash{download_date}.zip")
        download_url = f"https://urlhaus-api.abuse.ch/downloads/{download_date}.zip"
        result = self.download(file_path, download_url)
        if result:
            command = f"copy \"{file_path}\" \"{smart_dir}\""
            try:
                check_output(command, shell=True)
            except SubprocessError as e:
                log.info(e)
        else:
            log.info(f"{download_date} downlaod Failed")

    @staticmethod
    def download(file_path, download_url, chunk_size=1024 * 1024 * 8):
        try:
            response = session.get(url=download_url, stream=True)
            if response.status_code != 200:
                return
            with open(file_path, "wb")as file:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    file.write(chunk)
            return True
        except Exception as e:
            log.info(e)
            return False


if __name__ == "__main__":
    SampleUrlHash()
