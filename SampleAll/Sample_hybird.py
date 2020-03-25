from First.SampleAll.InitFile import *


def sample_hybird():
    # update login session
    url_login = "https://www.hybrid-analysis.com/login"
    try:
        token = session.get(url_login).html.find("input#login__token")[0].attrs["value"]
        user_data = {
            "login[email]": "cicely@iobit.com",
            "login[password]": "IObit>20191213",
            "login[_token]": token
        }
        session.post(url_login, data=user_data)
    except Exception as e:
        return False, e

    sample_dict = {}
    # get download dict
    url_feed = "https://www.hybrid-analysis.com/feed"
    try:
        result = session.get(url_feed, params={"json": ""})
        data = result.json()["data"]
        url_base = "https://www.hybrid-analysis.com/download-sample/"
        for detail in data:
            sample_md5 = detail["md5"]
            file_name = sample_md5 + ".bin.gz"
            file_path = os.path.join(sample_dir, file_name)
            download_url = url_base + detail["sha256"]
            sample_info = {
                "sample_path": file_path,
                "sample_url": download_url,
                "session": session
            }
            sample_dict.update({sample_md5: sample_info})
        return True, sample_dict
    except Exception as e:
        return False, e
