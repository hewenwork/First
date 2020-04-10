import os
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from datetime import datetime, timedelta

session = HTMLSession()


def get_feed():
    # get download dict
    url_feed = "https://www.hybrid-analysis.com/feed"
    try:
        result = session.get(url_feed, params={"json": ""}).json()
    except Exception as e:
        information = f"Failed in Get Feed {url_feed}: {e}."
        return {information}
    else:
        sha256_set = set(detail["sha256"] for detail in result["data"])
        return sha256_set


def get_latest():
    sample_set = set()
    url = "https://www.hybrid-analysis.com/submissions/sandbox/files"
    params = {
        "sort": "timestamp",
        "sort_order": "desc",
        "page": 1
    }
    selector = "a.analysis-overview-link.convert-link"
    for page in range(1, 11):
        params.update({"page": page})
        try:
            response = session.get(url, params=params).text
            soup = BeautifulSoup(response, "lxml").select(selector)
            for detail in soup:
                sha256 = detail.get("href").split("/")[-1]
                sample_set.add(sha256)
        except Exception as e:
            information = f"get {url} in page{page} error:{e}."
            sample_set.add(information)
            continue
    return sample_set


def hybird_login_session():
    url_login = "https://www.hybrid-analysis.com/login"
    user_data = {
        "login[email]": "cicely@iobit.com",
        "login[password]": "IObit>20191213"
    }
    try:
        response = session.get(url_login)
        soup = BeautifulSoup(response.text, "lxml")
        token = soup.select("input#login__token")[0].get("value")
        user_data.setdefault("login[_token]", token)
        result = session.post(url_login, data=user_data)
        if "I forgot my password" in result.text:
            return False, "login failed."
        else:
            return True, session
    except Exception as e:
        return False, f"login Exception :{e}."


def sample_hybird(download_date):
    if isinstance(download_date, datetime) is False:
        return False, f"{download_date} is not isinstance datetime."
    sample_date = datetime.today() - timedelta(days=1)
    if download_date.date() != sample_date.date():
        return False, "website not support history data download."
    sample_dir = r"G:\AutoCollect"
    sample_dir = os.path.join(sample_dir, sample_date.strftime("%Y-%m-%d"))  # 存放Sample
    sample_list = []
    login_result, login_detail = hybird_login_session()
    for sha256 in set.union(get_latest(), get_feed()):
        if login_result:
            url_base = "https://www.hybrid-analysis.com/download-sample/"
            sample_name = f"{sha256}.bin.gz"
            sample_path = os.path.join(sample_dir, sample_name)
            sample_url = f"{url_base}{sha256}"
            sample_detail = {
                "sample_md5": sha256,
                "sample_name": sample_name,
                "sample_path": sample_path,
                "sample_url": sample_url,
                "session": login_detail,
                "is_archive": True
            }
            sample_list.append(sample_detail)
        else:
            sample_detail = {"sample_md5": sha256}
            sample_list.append(sample_detail)
    return True, sample_list


if __name__ == "__main__":
    a = sample_hybird(datetime.today() - timedelta(days=1))
    print(a)
