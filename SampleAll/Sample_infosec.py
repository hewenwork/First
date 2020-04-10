import re
import os
from datetime import datetime
from requests_html import HTMLSession

session = HTMLSession()


def sample_infosec(download_date):
    if isinstance(download_date, datetime) is False:
        return False, f"{download_date} is not isinstance datetime"
    sample_date = download_date.strftime("%Y-%m-%d")
    sample_dir = os.path.join(r"G:\AutoCollect", sample_date)  # 存放Sample
    if os.path.exists(sample_dir) is False:
        try:
            os.makedirs(sample_dir)
        except Exception as e:
            return False, f"Make dir {sample_dir} Exception: {e}."
    url = "https://infosec.cert-pa.it/analyze/"
    sample_list = []
    try:
        response = session.get(url + "submission.html").text
        md5_list = re.findall(f"<td>{sample_date} .*</td>\n.*\n.*<td><a href=\"/analyze/(.*).html\">", response)
        if len(md5_list) == 0:
            return False, "has`t data"
        for sample_md5 in md5_list:
            sample_name = f"{sample_md5}.vir"
            sample_path = os.path.join(sample_dir, sample_name)
            sample_response = session.get(url + sample_md5 + ".html").text
            link = re.findall(r"rel=\"nofollow\">.*?\.(.*?)</span><span class", sample_response)[0]
            sample_url = "http://" + link.strip("[").strip("]")
            sample_info = {
                "sample_md5": sample_md5,
                "sample_url": sample_url,
                "sample_path": sample_path,
                "is_archive": False
            }
            sample_list.append(sample_info)
        return True, sample_list
    except Exception as e:
        return False, f"Exception: {e}."


if __name__ == "__main__":
    print(sample_infosec(datetime.today()))
