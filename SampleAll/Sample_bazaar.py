import os
from requests_html import HTMLSession
from datetime import datetime, timedelta

api = "768fca1913d08f2e7479da1865f1b11a"

sample_dir = r"G:\Abuse"


# def sample_bazaar(download_date=None):
#     if isinstance(download_date, datetime) is False:
#         return False, f"{download_date} is not isinstance datetime"
#     sample_date = download_date.strftime("%Y-%m-%d")
#     url = "https://mb-api.abuse.ch/api/v1/"
#     data = {
#         "API-KEY": api,
#         # "query": "get_file",
#         # "sha256_hash": None
#         "selector": 100,
#         "query": "get_recent"
#     }
#     session = HTMLSession()
#     response = session.post(url, data=data).json()
#     if response["query_status"] != "ok":
#         return False, f"query_status is not ok."
#     for file_info in response["data"]:
#         sha256_hash = file_info.setdefault("sha256_hash")
#         md5_hash = file_info.setdefault("md5_hash")
#         first_seen = datetime.strptime(file_info.setdefault("first_seen"), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
#         file_name = file_info.setdefault("file_name")
#         print(sha256_hash, md5_hash, first_seen, file_name)


def sample_bazaar(download_date):
    if isinstance(download_date, datetime) is False:
        return False, f"{download_date} is not isinstance datetime"
    if download_date.date() == datetime.today().date():
        return False, "Can`t Download today data"
    sample_date = download_date.strftime("%Y-%m-%d")
    sample_name = f"[infected]_mb-api_{sample_date}.zip"
    sample_url = f"https://mb-api.abuse.ch/downloads/{sample_date}.zip"
    sample_dict = {
        "sample_name": sample_name,
        "sample_path": os.path.join(sample_dir, sample_name),
        "sample_url": sample_url
    }
    sample_list = [sample_dict]
    return True, sample_list


if __name__ == "__main__":
    a = sample_bazaar(datetime(year=2020, month=4, day=6))
    print(a)
