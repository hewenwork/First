import re
import os
from datetime import datetime, timedelta
from subprocess import check_output, SubprocessError
from requests_html import HTMLSession

session = HTMLSession()
download_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")  # 样本下载日期

Init_dir = r"G:\AutoCollect"
sample_all_dir = os.path.join(Init_dir, download_date)  # 存放Sample
if os.path.exists(sample_all_dir) is False:
    os.makedirs(sample_all_dir)

log_dir = r"G:\SampleLog"  # 存放MD5和下载日志
log_log_dir = os.path.join(log_dir, "DownloadLog")
log_md5_dir = os.path.join(log_dir, "MD5")
log_path = os.path.join(log_log_dir, f"{download_date}.log")  # 存放下载日志
md5_path = os.path.join(log_md5_dir, f"{download_date}.log")  # 存放下载失败的MD5
if os.path.exists(log_dir) is False:
    try:
        os.makedirs(log_dir)
        os.makedirs(log_log_dir)
        os.makedirs(log_md5_dir)
    except Exception as _:
        with open("error.log", "a+")as _file:
            _file.write(f"{datetime.today()}: {_}\n")

sample_urlhaus_dir = r"G:\Urlhaus"
if os.path.exists(sample_urlhaus_dir) is False:
    os.makedirs(sample_urlhaus_dir)

smart_file_dir = r"G:\Auto"  # 转移到smartccl位置
smart_log_dir = r"\\192.168.1.39\e\VTSpider\MD5SHA256"  # 转移到39位置
smart_md5_path = os.path.join(smart_log_dir, f"{download_date}MD5.txt")


def write_log(info):
    try:
        with open(log_path, "a+", encoding="utf-8")as _:
            _.write(f"{datetime.today()}:  {info}\n")
    except Exception as _:
        with open("error.log", "a+")as _:
            _file.write(f"{datetime.today()}: {_}\n")


def write_md5(md5):
    file = open(md5_path, "a+", encoding="utf-8")
    line = f"{md5}\n"
    try:
        if len(md5) == 32:
            old_data = file.read()
            file.seek(0, 0)
            file.write(line + old_data)
        else:
            file.write(line)
    except Exception as e:
        with open("error.log", "a+")as _:
            _.write(f"{datetime.today()}: {e}\n")
    file.close()


if __name__ == "__main__":
    write_md5("ade449592745b54724fa70ec488b99fdaaaaaaaaaaaaaaaaaaaaaaaa")
