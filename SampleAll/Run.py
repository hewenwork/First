import os
import re
import sys
from time import sleep
from requests_html import HTMLSession
from datetime import datetime, timedelta
from First.SampleAll.Download import download
from First.SampleAll.Sample_hybird import sample_hybird
from First.SampleAll.Sample_vxvault import sample_vxvault
from First.SampleAll.Sample_infosec import sample_infosec
from First.SampleAll.Sample_traffic import sample_traffic
from First.SampleAll.Sample_malshare import sample_malshare
from First.SampleAll.Sample_virusbay import sample_virusbay
from First.SampleAll.Sample_virussign import sample_virusign
from First.SampleAll.Compression import extract, archive
from First.SampleAll.Sample_urlhaus import sample_urlhaus
from First.SampleAll.Sample_LimitedFree import sample_limitedfree
from First.SampleAll.Sample_bazaar import sample_bazaar
from First.SampleAll.Sample_snapshot import sample_snapshot

download_date = datetime.today()  # 程序开始时间

log_log_dir = r"G:\SampleLog\DownloadLog"  # 存放下载日志位置
log_path = os.path.join(log_log_dir, "%s.log" % download_date.strftime("%Y%m%d"))  # 存放下载日志位置

log_md5_dir = r"G:\SampleLog\MD5"  # 存放下载的MD5位置
md5_path = os.path.join(log_md5_dir, "%s.txt" % download_date.strftime("%Y%m%d"))  # 存放下载的MD5位置

smart_file_dir = r"G:\Auto"  # 转移到smartccl位置
smart_md5_dir = r"\\192.168.1.39\e\VTSpider\MD5SHA256"  # 转移MD5到39位置
try:
    open(md5_path, "w").close()
    if os.path.exists(log_log_dir) is False:
        os.makedirs(log_log_dir)
    if os.path.exists(log_md5_dir) is False:
        os.makedirs(log_md5_dir)
except Exception as e:
    exit(e)

if len(sys.argv) > 1:
    input_date = sys.argv[-1]
    if re.match(r"%Y%m%d", input_date) is not None:
        sample_date = datetime.strptime(sys.argv[-1], "%Y%m%d")
    else:
        sample_date = None
        exit("data error, ex:20200301")
else:
    sample_date = datetime.today() - timedelta(days=1)


def write_log(info):
    with open(log_path, "a+", encoding="utf-8") as file:
        line = f"{datetime.today()}: {info}\n"
        file.write(line)
        print(line)


def write_hash(sample_hash):
    if sample_hash is None:
        return
    try:
        if re.match(r"^[a-zA-Z0-9]{32}$|^[a-zA-Z0-9]{64}$", sample_hash):
            with open(md5_path, "r+", encoding="utf-8") as file:
                if len(sample_hash) == 32:
                    data = f"{sample_hash}\n" + file.read()
                    file.seek(0)
                else:
                    data = f"{sample_hash}\n"
                    file.seek(0, 2)
                file.write(data)
    except Exception as er:
        write_log(f"write has Exception:{er}.")


def trans(file_path, dist):
    if os.path.exists(file_path) is False:
        return f"target file: {file_path} not exists."
    if os.path.exists(dist) is False:
        return f"dist dir: {dist} not exists."
    try:
        os.system(f"copy \"{file_path}\" \"{dist}\"")
        return f"copy {file_path} to {dist} Successful."
    except Exception as e:
        return f"copy {file_path} to {dist} Exception: {e}."


# def run_sample_archive():
#     sample_archive = {
#         "https://urlhaus-api.abuse.ch": sample_urlhaus,
#         "http://samples.virussign.com/samples": sample_limitedfree,
#         "https://bazaar.abuse.ch/browse/": sample_bazaar,
#         "http://www.malware-traffic-analysis.net": sample_traffic,
#         "https://www.snapshot.clamav.net/daily": sample_snapshot
#     }
#     for website, info in sample_archive.items():
#         write_log(f"------START WEBSITE: {website}")
#         result, detail = info(sample_date)
#         write_log(f"Requests website: {website} ---{result}.")
#         if result is False:
#             write_log(detail)
#         else:
#             for sample_info in detail:
#                 sample_url = sample_info.setdefault("sample_url")
#                 sample_path = sample_info.setdefault("sample_path")
#                 write_log(f"URL: {sample_url}")
#                 write_log(f"PATH: {sample_path}")
#                 download_result, information = download(sample_path, sample_url, **sample_info)
#                 write_log(information)
#                 if download_result:
#                     trans_result = trans(sample_path, smart_file_dir)
#                     write_log(trans_result)
#         write_log(f"------END WEBSITE: {website}.\n")
#
#
# def run_sample_all():
#     sample_all_dir = r"G:\AutoCollect"
#     sample_all_dir = os.path.join(sample_all_dir, sample_date.strftime("%Y-%m-%d"))  # 存放Sample
#     sample_final_path = sample_all_dir + "[infected].rar"  # 完成后压缩文件名
#     if os.path.exists(sample_all_dir) is False:
#         os.makedirs(sample_all_dir)
#     sample_all_dict = {
#         "https://www.hybrid-analysis.com": sample_hybird,
#         "http://www.virusign.com/get_hashlist.php": sample_virusign,
#         "https://malshare.com/api.php": sample_malshare,
#         "http://vxvault.net/ViriList.php/ViriFiche.php": sample_vxvault,
#         "https://beta.virusbay.io/sample/data": sample_virusbay,
#         "https://infosec.cert-pa.it/analyze/": sample_infosec
#     }
#     for website, info in sample_all_dict.items():
#         write_log(f"------START WEBSITE: {website}")
#         file_num = 0
#         result, detail = info(sample_date)
#         write_log(f"Requests website: {website} ---{result}.")
#         if result is False:
#             write_log(detail)
#         else:
#             file_num = len(detail)
#             for sample_info in detail:
#                 sample_md5 = sample_info.setdefault("sample_md5")
#                 if sample_md5 is not None:
#                     write_hash(sample_hash=sample_md5)
#                 sample_name = sample_info.setdefault("sample_name")
#                 sample_url = sample_info.setdefault("sample_url")
#                 is_archive = sample_info.setdefault("is_archive", False)
#                 sample_path = sample_info.setdefault("sample_path", os.path.join(sample_all_dir, sample_name))
#                 sleep(1)
#                 write_log(f"PATH: {sample_path}")
#                 write_log(f"URL: {sample_url}")
#                 download_result, download_information = download(sample_path, sample_url, **sample_info)
#                 write_log(download_information)
#                 if download_result is False:
#                     continue
#                 if is_archive:
#                     extract_result, extract_detail = extract(sample_path)
#                     extract_detail = f"extract_result: {extract_detail}."
#                     write_log(extract_detail)
#                     try:
#                         os.remove(sample_path)
#                         write_log(f"delete archive file: ok.")
#                     except Exception as e:
#                         write_log(f"delete failed, Exception: {e}.")
#                 break
#         write_log(f"------END WEBSITE: {website}. Files: {file_num}\n")
#     trans(md5_path, smart_md5_dir)
#     archive_result, archive_detail = archive(sample_all_dir, sample_final_path)
#     write_log(archive_detail)
#     if archive_result:
#         trans_result = trans(sample_final_path, smart_file_dir)
#         write_log(trans_result)


def test():
    sample_list = [
        {"website": "https://www.hybrid-analysis.com", "function": sample_hybird, "is_trans": False},
        {"website": "http://www.virusign.com/get_hashlist.php", "function": sample_virusign, "is_trans": False},
        {"website": "https://malshare.com/api.php", "function": sample_malshare, "is_trans": False},
        {"website": "http://vxvault.net/ViriList.php/ViriFiche.php", "function": sample_vxvault, "is_trans": False},
        {"website": "https://beta.virusbay.io/sample/data", "function": sample_virusbay, "is_trans": False},
        {"website": "https://infosec.cert-pa.it/analyze/", "function": sample_infosec, "is_trans": False},
        {"website": "https://urlhaus-api.abuse.ch", "function": sample_urlhaus, "is_trans": True},
        {"website": "http://samples.virussign.com/samples", "function": sample_limitedfree, "is_trans": True},
        {"website": "https://bazaar.abuse.ch/browse/", "function": sample_bazaar, "is_trans": True},
        {"website": "http://www.malware-traffic-analysis.net", "function": sample_traffic, "is_trans": True},
        {"website": "https://www.snapshot.clamav.net/daily", "function": sample_snapshot, "is_trans": True},
    ]
    for value in sample_list:
        website = value["website"]
        function = value["function"]
        is_trans = value["is_trans"]
        write_log(f"------START WEBSITE: {website}")
        result, detail = function(sample_date)
        download_num = 0
        if result:
            total_num = len(detail)
            for sample_dict in detail:
                sample_md5 = sample_dict.setdefault("sample_md5")
                sample_url = sample_dict.setdefault("sample_url")
                sample_path = sample_dict.setdefault("sample_path")
                is_archive = sample_dict.setdefault("is_archive", False)
                write_hash(sample_md5) if sample_md5 is not None else None
                write_log(f"URL: {sample_url}")
                write_log(f"PATH: {sample_path}")
                download_result, download_information = download(sample_path, sample_url, **sample_dict)
                write_log(download_information)
                download_num += 1 if download_result else 0
                if is_trans and download_result:
                    trans_detail = trans(sample_path, smart_file_dir)
                    write_log(trans_detail)
                if is_archive and download_result and is_trans is False:
                    extract_detail = extract(sample_path)
                    write_log(extract_detail)
                    try:
                        os.remove(sample_path)
                        write_log(f"delete archive file {sample_path}: ok.")
                    except Exception as delete_error:
                        write_log(f"delete failed, Exception: {delete_error}.")
        else:
            total_num = 0
            write_log(detail)
        write_log(f"total_num: {total_num}, download_num: {download_num}.")
        write_log(f"------END WEBSITE: {website}\n")


if __name__ == "__main__":
    test()
