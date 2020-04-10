import os
from urllib3 import disable_warnings
from requests_html import HTMLSession
from datetime import datetime, timedelta

disable_warnings()
sample_dir = r"G:\snapshot"
user = "iobit"
pwd = "iobit#@6sample"
auth = (user, pwd)
session = HTMLSession()
option = {
    "auth": auth,
    "stream": True,
    "verify": False
}


def sample_snapshot(download_date):
    sample_date = download_date.strftime("%Y%m%d")
    sample_list = []
    sample_all_dict = parse_all(sample_date)
    sample_critical_dict = parse_critical(sample_date)
    sample_list.append(sample_all_dict) if isinstance(sample_all_dict, dict) else None
    sample_list.append(sample_critical_dict) if isinstance(sample_critical_dict, dict) else None
    if len(sample_list) > 0:
        return True, sample_list
    else:
        return False, f"has`t data {sample_date}."


def parse_all(sample_date):
    sample_url = f"https://www.snapshot.clamav.net/daily/snapshot-all-{sample_date}.zip.001"
    sample_name = f"[infected]_snapshot_all_{sample_date}.zip"
    sample_path = os.path.join(sample_dir, sample_name)
    try:
        length_all = session.get(sample_url, **option).headers["content-length"]
        if int(length_all) > 1024:
            sample_all_dict = {
                "sample_url": sample_url,
                "sample_path": sample_path,
                "auth": (user, pwd),
                "stream": True,
                "verify": False
            }
            return sample_all_dict
        else:
            return False
    except Exception as e:
        return e


def parse_critical(sample_date):
    sample_url = f"https://www.snapshot.clamav.net/daily/snapshot-critical-{sample_date}.zip.001"
    sample_name = f"[infected]_snapshot_critical_{sample_date}.zip"
    sample_path = os.path.join(sample_dir, sample_name)
    try:
        length_critical = session.get(sample_url, **option).headers["content-length"]
        if int(length_critical) > 1024:
            sample_critical_dict = {
                "sample_url": sample_url,
                "sample_path": sample_path,
                "auth": (user, pwd),
                "stream": True,
                "verify": False
            }
            return sample_critical_dict
        else:
            return False
    except Exception as e:
        return e


if __name__ == "__main__":
    print(sample_snapshot(datetime(year=2020, month=4, day=1)))
