import os
import winreg

import requests
import datetime


def get_sample_snapshot():
    today = datetime.datetime.today().date()
    yyestoday = today - datetime.timedelta(days=5)
    file_name = "snapshot-all-%s.zip.001" % yyestoday.strftime("%Y%m%d")
    url = "https://www.snapshot.clamav.net/daily/%s" % file_name
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "Authorization": "Basic aW9iaXQ6aW9iaXQjQDZzYW1wbGU="
    }
    download_path = os.path.join(download_folder, file_name)
    try:
        response = requests.get(url, headers=headers, verify=False)
        with open(download_path, "wb")as file:
            file.write(response.content)
    except BaseException as e:
        print("source error : %s" % e)

def get_folder_path():
    key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"\SOFTWARE\hewen")
    print(1)
if __name__ == "__main__":
    download_folder = r"C:\Users\hewen\Desktop"
    get_folder_path()
    # get_sample_snapshot()
