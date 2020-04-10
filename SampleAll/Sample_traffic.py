import os
from datetime import datetime
from requests_html import HTMLSession

session = HTMLSession()


def sample_traffic(download_date):
    sample_dir = r"G:\malware_traffic_analysis"
    sample_list = []
    sample_date = download_date.strftime("%Y/%m/%d")
    url = f"http://www.malware-traffic-analysis.net/{sample_date}/"
    try:
        result = session.get(url + "index.html")
        soup = result.html.find("ul > li > a") if result.status_code == 200 else None
        if soup is None:
            return False, "has`t data"
        for line in soup:
            sample_name = line.attrs["href"]
            sample_url = f"{url}{sample_name}"
            sample_path = os.path.join(sample_dir, sample_name)
            if "-malware" in sample_name:
                sample_info = {
                    "sample_path": sample_path,
                    "sample_url": sample_url,
                    "is_archive": True
                }
                sample_list.append(sample_info)
        if len(sample_list) == 0:
            return False, f"has`t data {sample_date}"
        return True, sample_list
    except Exception as e:
        return False, e


if __name__ == "__main__":
    print(sample_traffic(datetime.today()))
