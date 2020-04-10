import os
from requests_html import HTMLSession
from datetime import datetime, timedelta


def login():
    session = HTMLSession()
    data = {
        "email": "niwangxiu@gmail.com",
        "password": "testvirus0504L"
    }
    login_url = "https://beta.virusbay.io/login"
    try:
        response = session.post(url=login_url, data=data)
        token = response.json()["token"]
        authorization = {"Authorization": "JWT %s" % token}
        session.headers.update(authorization)
        return session
    except Exception as e:
        return f"login failed, Exception: {e}."


def sample_virusbay(download_date):
    sample_dir = os.path.join(r"G:\AutoCollect", download_date.strftime("%Y-%m-%d"))  # 存放Sample
    sample_date = download_date.strftime("%Y-%m-%d")
    session = login()
    if isinstance(session, HTMLSession) is False:
        return False, session
    data_url = "https://beta.virusbay.io/sample/data"
    recent = session.get(url=data_url).json()["recent"]
    sample_list = []
    for sample in recent:
        add_date = sample["publishDate"][:10]
        sample_md5 = sample["md5"]
        sample_name = sample_md5 + ".vir"
        sample_path = os.path.join(sample_dir, sample_name)
        sample_link = "https://beta.virusbay.io/api/sample/%s/download/link" % sample["_id"]
        if add_date == sample_date:
            try:
                sample_url = session.get(sample_link).text
            except Exception as e:
                sample_url = f"Exception parse: {e}"
            sample_info = {
                "sample_md5": sample_md5,
                "sample_url": sample_url,
                "sample_path": sample_path,
            }
            sample_list.append(sample_info)
    return True, sample_list


if __name__ == "__main__":
    print(sample_virusbay(datetime.today() - timedelta(days=1)))
    # print(isinstance("session", HTMLSession))
