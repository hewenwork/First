import re
import os
from datetime import datetime
from requests_html import HTMLSession

session = HTMLSession()


def sample_vxvault(download_date):
    sample_dir = os.path.join(r"G:\AutoCollect", download_date.strftime("%Y-%m-%d"))  # 存放Sample
    url = "http://vxvault.net/ViriList.php/"
    sample_date = download_date.strftime("%m-%d")
    sample_list = []
    try:
        soup = session.get(url).html.find("tr > td:nth-of-type(1) > a")
        for add_date_element in soup:
            add_date = add_date_element.text
            if add_date < sample_date:
                break
            if add_date == sample_date:
                page_link = "http://vxvault.net/" + add_date_element.attrs["href"]
                result = get_sample_detail(page_link)
                if isinstance(result, tuple):
                    sample_md5, sample_url = result
                    sample_name = f"{sample_md5}.vir"
                    sample_path = os.path.join(sample_dir, sample_name)
                    sample_info = {
                        "sample_url": sample_url,
                        "sample_path": sample_path
                    }
                    sample_list.append(sample_info)
        if len(sample_list) == 0:
            return False, f"website: : {url},  has`t data."
        else:
            return True, sample_list
    except Exception as e:
        return False, f"Get Failed, url: {url}, error: {e}."


def get_sample_detail(page_link):
    try:
        result = session.get(page_link)
        sample_md5 = re.findall(r"<B>MD5:</B> (.*?)<BR>", result.text)[0]
        sample_url = f"http://" + re.findall(r"<B>Link:</B> hxxp://(.*?)<BR>", result.text)[0]
        return sample_md5, sample_url
    except Exception as e:
        return f"Get Failed, url: {page_link}, error: {e}."


if __name__ == "__main__":
    a = sample_vxvault(datetime(day=8, month=4, year=2020))
    print(a)
