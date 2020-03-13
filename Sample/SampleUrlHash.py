# encoding = utf-8
# @Author: He wen
# @Time: 1/22/2020 11:10 AM
# @File: SampleUrlHash.py
import os
import requests_html
from datetime import datetime, timedelta
from subprocess import check_output, SubprocessError

smart_dir = r"G:\Auto"  # 转移到smartccl位置
sample_dir = r"G:\Urlhash"  # 存放Sample
log_dir = os.path.join(sample_dir, "log")  # 存放下载日志

if os.path.exists(smart_dir) is False:
    os.makedirs(smart_dir)

if os.path.exists(sample_dir) is False:
    os.makedirs(sample_dir)

if os.path.exists(log_dir) is False:
    os.makedirs(log_dir)

download_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")  # 样本下载日期
file_path = os.path.join(sample_dir, f"[infected]UrlHash{download_date}.zip")
download_url = f"https://urlhaus-api.abuse.ch/downloads/{download_date}.zip"
log_path = os.path.join(log_dir, f"{download_date}.log")

session = requests_html.HTMLSession()


def log(info):
    with open(log_path, "a+", encoding="utf-8")as file:
        file.write(f"{datetime.today()}{info}\n")


def download(path, url):
    chunk_size = 1024 * 1024 * 8
    try:
        response = session.get(url=url, stream=True)
        if response.status_code != 200:
            log("status: != 200")
            return False
    except Exception as e:
        log(e)
        return False
    else:
        with open(path, "wb")as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                file.write(chunk)
        return True


def task():
    command = f"copy \"{file_path}\" \"{smart_dir}\""
    if download(file_path, download_url):
        try:
            check_output(command, shell=True)
        except SubprocessError as e:
            log(e)
        else:
            log(f"{download_date} download Successful")
    else:
        log(f"{download_date} download Failed")


if __name__ == "__main__":
    task()
