import os
import re
import requests_html
from datetime import datetime, timedelta
from subprocess import check_output, STDOUT

Init_dir = r"G:\VirusSign"  # 样本存放位置
smart_file_dir = r"G:\Auto"  # 转移到smartccl位置
log_dir = os.path.join(Init_dir, "log")  # 下载日志和异常记录位置
if os.path.exists(Init_dir) is False:
    os.makedirs(Init_dir)

if os.path.exists(log_dir) is False:
    os.makedirs(log_dir)

auth = ("infected", "infected")  # 下载验证
session = requests_html.HTMLSession()


def write_log(log_path, info):
    with open(log_path, "a+", encoding="utf-8")as file:
        file.write(f"{datetime.today()}: {info}\n")


def download(sample_path, sample_url):
    try:
        content = session.get(sample_url, auth=auth, timeout=30).content
        with open(sample_path, "wb")as file:
            file.write(content)
        return True
    except Exception as e:
        return e


def sample_virusign(start_date, end_date):
    url = f"http://www.virusign.com/get_hashlist.php"
    params = {
        "sha256": "",
        "start_date": start_date,
        "end_date": end_date
    }
    try:
        response = session.get(url, params=params, timeout=40).text
        return {
            sha256 + ".7z": f"http://virusign.com/file/{sha256}.7z"
            for sha256 in re.findall(r"\"(\w{64})\"", response)
        }
    except Exception as e:
        return e


def de(target_path, dist_path, password="infected"):
    if os.path.exists(target_path) is False:
        return False
    command = f"7z e -p{password} -y \"{target_path}\" -so > \"{dist_path}\""
    try:
        check_output(command, shell=True, stderr=STDOUT)
        os.remove(target_path)
        return True
    except Exception as e:
        return e


def co(file_path, dist_path):
    if os.path.exists(file_path) is False:
        return False
    command = f"rar a -ep -pinfected -id[c,d,p,q] -y \"{dist_path}\" \"{file_path}\""
    try:
        check_output(command, shell=True)
        return True
    except Exception as e:
        return e


def start_download():
    dir_list = [dir_name for dir_name in os.listdir(Init_dir) if re.match(r"\d{4}-\d{2}-\d{2}", dir_name)]
    dir_list.reverse()
    download_date = datetime.strptime(dir_list[0], "%Y-%m-%d") + timedelta(days=1)
    download_date = download_date.strftime("%Y-%m-%d")
    sample_dir = os.path.join(Init_dir, download_date)  # 存放Sample
    log_path = os.path.join(log_dir, f"{download_date}.log")  # 存放下载日志
    if os.path.exists(sample_dir) is False:
        os.makedirs(sample_dir)
    sample_dict = sample_virusign(download_date, download_date)
    total_num = len(sample_dict)
    if type(sample_dict) is str:
        write_log(log_path, sample_dict)
    elif total_num == 0:
        info = "Has`t data"
        write_log(log_path, info)
    else:
        info = f"http://www.virusign.com/get_hashlist.php?start_date={download_date} find sample {total_num}"
        write_log(log_path, info)
        for sample_name, sample_url in sample_dict.items():
            sample_path = os.path.join(sample_dir, sample_name)
            dist_path = os.path.join(sample_dir, sample_name.replace(".7z", ".vir"))
            if download(sample_path, sample_url) is True:
                decompression = de(sample_path, dist_path)
                info = f"{sample_path} download successful, decompression result: {decompression}"
                write_log(log_path, info)
            else:
                info = f"{sample_path} download failed"
                write_log(log_path, info)
    compression_path = os.path.join(Init_dir, download_date + "[infected].rar")
    compression = co(sample_dir, compression_path)
    if compression is True:
        try:
            os.system(f"copy \"{compression_path}\" \"{smart_file_dir}\"")
        except Exception as e:
            write_log(log_path, e)


while 1:
    start_download()
