import os
import re
import requests
import datetime
from bs4 import BeautifulSoup


def get_sample(sha256):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "Authorization": "Basic aW5mZWN0ZWQ6aW5mZWN0ZWQ="
    }
    url = "http://virusign.com/file/%s.7z" % sha256
    try:
        with open(r"C:\Users\hewen\Desktop\auto\%s.vir" % sha256, "wb")as file:
            file.write(requests.get(url=url, headers=headers).content)
    except Exception as e:
        print(e)

def get_info(download_date):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    for d in range(5):
        p = 1
        while p != -1:
            url = "http://virusign.com/home.php?d=%d&r=100&c=hashes&o=date&s=DESC&n=EXACT&p=%s" % (d, p)
            p += 1
            respone = requests.get(url=url, headers=headers)
            suop = BeautifulSoup(respone.text, "lxml")
            date_list=suop.select("tr > td:nth-of-type(2)")
            sha256_list = suop.select("tr > td:nth-of-type(4)")
            for date, sha256 in zip(date_list, sha256_list):
                date = date.getText()
                sha256 = sha256.getText().split(" ")[-1]
                if date == download_date:
                    print(date, sha256)
                    get_sample(sha256)
                elif date < download_date:
                    p = -1
if __name__ == "__main__":
    download_date = "2019-03-27"
    get_info(download_date)
