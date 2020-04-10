import os
import re
from datetime import datetime
from requests_html import HTMLSession

session = HTMLSession()


def sample_virusign(download_date):
    sample_dir = os.path.join(r"G:\AutoCollect", download_date.strftime("%Y-%m-%d"))  # 存放Sample
    sample_date = download_date.strftime("%Y-%m-%d")
    url = f"http://www.virusign.com/get_hashlist.php"
    params = {
        "md5": "",
        "sha256": "",
        "start_date": sample_date,
        "end_date": sample_date
    }
    auth = ("infected", "infected")
    try:
        sample_list = []
        response = session.get(url, params=params, timeout=40).text
        for sample_sha256 in re.findall(r"\"(\w{64})\"", response):
            sample_name = f"{sample_sha256}.7z"
            sample_path = os.path.join(sample_dir, sample_name)
            sample_url = f"http://virusign.com/file/{sample_sha256}.7z"
            sample_info = {
                "sample_md5": sample_sha256,
                "sample_url": sample_url,
                "sample_path": sample_path,
                "auth": auth,
                "is_archive": True
            }
            sample_list.append(sample_info)
        if len(sample_list) == 0:
            information = f"website today num is 0."
            return False, information
        else:
            return True, sample_list
    except Exception as e:
        information = f"parse website error: {e}."
        return False, information


if __name__ == "__main__":
    a = sample_virusign(datetime(year=2020, month=3, day=30))
    print(a)
