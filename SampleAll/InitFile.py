import re
import os
from datetime import datetime, timedelta
from subprocess import check_output, SubprocessError
from requests_html import HTMLSession

session = HTMLSession()
download_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")  # 样本下载日期

Init_dir = r"G:\AutoCollect"
sample_dir = os.path.join(Init_dir, download_date)  # 存放Sample
if os.path.exists(sample_dir) is False:
    os.makedirs(sample_dir)

log_dir = os.path.join(Init_dir, "log")  # 存放MD5和SSD
log_path = os.path.join(log_dir, f"{download_date}.log")  # 存放下载日志
if os.path.exists(log_dir) is False:
    os.makedirs(log_dir)

smart_file_dir = r"G:\Auto"  # 转移到smartccl位置
smart_log_dir = r"\\192.168.1.39\e\VTSpider\MD5SHA256"  # 转移到39位置

urlhaus_dir = r"G:\Urlhaus"
if os.path.exists(urlhaus_dir) is False:
    os.makedirs(urlhaus_dir)


def write_log(info):
    try:
        with open(log_path, "a+", encoding="utf-8")as file:
            file.write(f"{datetime.today()}:  {info}\n")
    except PermissionError as e:
        with open("error.log", "a+")as file:
            file.write(f"{e}")
