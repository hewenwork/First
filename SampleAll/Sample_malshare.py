import os
from requests_html import HTMLSession
from datetime import datetime, timedelta

session = HTMLSession()


def sample_malshare(download_date):
    sample_dir = os.path.join(r"G:\AutoCollect", download_date.strftime("%Y-%m-%d"))  # 存放Sample
    sample_date = download_date.strftime("%Y-%m-%d")
    md5_url = f"https://malshare.com/daily/{sample_date}/malshare_fileList.{sample_date}.sha1.txt"
    if download_date == datetime.today() - timedelta(days=1):
        md5_url = "https://malshare.com/daily/malshare.current.sha1.txt"
    try:
        response = session.get(md5_url)
        if response.status_code != 200:
            return False, f"{sample_date} has`t data"
        sample_list = []
        for line in response.text.split("\n")[:-1]:
            sample_md5 = line
            sample_name = sample_md5 + ".vir"
            sample_path = os.path.join(sample_dir, sample_name)
            action = "getfile"
            api_key = "2befc1c0b4d476b8527887f3f415648050638eff8dd400071f694e7356d5e49a"
            sample_url = f"https://malshare.com/api.php?api_key={api_key}&action={action}&hash={sample_md5}"
            sample_info = {
                "sample_md5": sample_md5,
                "sample_url": sample_url,
                "sample_path": sample_path,
            }
            sample_list.append(sample_info)
        return True, sample_list
    except Exception as e:
        return False, f"link: {md5_url}, Exception: {e}."


if __name__ == "__main__":
    result = sample_malshare(datetime.today() - timedelta(days=1))
    print(result)
