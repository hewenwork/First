from bs4 import BeautifulSoup
from First.SampleAll.InitFile import *


def sample_hybird():
    """
    this function is get all sha256 and deal it,
    one: feed
    two: get latest 10 page
    :return: if login failed, not return, just deal sha256
    """
    sample_dict = {}
    feed_result, feed_detail = get_feed()
    latest_result, latest_detail = get_latest()
    if feed_result:
        sample_dict.update(feed_detail)
    else:
        write_log(feed_detail)
    if latest_result:
        sample_dict.update(latest_detail)
    else:
        write_log(latest_detail)
    url_base = "https://www.hybrid-analysis.com/download-sample/"
    login_result, login_detail = hybird_login_session()
    if login_result:
        for sha256, detail in sample_dict.items():
            sample_name = sha256 + ".bin.gz"
            sample_path = os.path.join(sample_all_dir, sample_name)
            sample_url = url_base + sha256
            sample_detail = {
                "sample_path": sample_path,
                "sample_url": sample_url,
                "session": login_detail
            }
            sample_dict.update({sha256: sample_detail})
        return True, sample_dict
    else:
        information = f"{login_detail}, just analysis sha256"
        for sha256 in sample_dict.keys():
            write_md5(sha256)
        return False, information


def hybird_login_session():
    """
    :return: if login successful return session, else False
    """
    # update login session
    url_login = "https://www.hybrid-analysis.com/login"
    try:
        token = session.get(url_login).html.find("input#login__token")[0].attrs["value"]
        user_data = {
            "login[email]": "cicely@iobit.com",
            "login[password]": "IObit>20191213",
            "login[_token]": token
        }
        result = session.post(url_login, data=user_data)
        if "I forgot my password" in result.text:
            return False, "login failed."
        else:
            return True, session
    except Exception as e:
        write_log(f"login failed :{e}.")


def get_latest():
    url = "https://www.hybrid-analysis.com/submissions/sandbox/files"
    params = {
        "sort": "timestamp",
        "sort_order": "desc",
        "page": 1
    }
    sample_dict = {}
    for page in range(1, 11):
        params.update({"page": page})
        try:
            response = session.get(url, params=params).text
            result, detail = parse(response)
            if result:
                sample_dict.update(detail)
            else:
                write_log(detail)
        except Exception as e:
            information = f"get {url} in page{page} error:{e}."
            write_log(information)
    return True, sample_dict


def get_feed():
    # get download dict
    url_feed = "https://www.hybrid-analysis.com/feed"
    try:
        result = session.get(url_feed, params={"json": ""}).json()
        sample_dict = {detail["sha256"]: {} for detail in result["data"]}
        return True, sample_dict
    except Exception as e:
        information = f"Failed in Get Feed {url_feed}: {e}."
        return False, information


def parse(content):
    """
    :param content: html response
    :return: sha256
    """
    try:
        soup = BeautifulSoup(content, "lxml")
        selector = "a.analysis-overview-link.convert-link"
        return True, {i.get("href").split("/")[-1]: {} for i in soup.select(selector)}
    except Exception as e:
        return False, f"BeautifulSoup: {e}."


if __name__ == "__main__":
    sample_hybird()
