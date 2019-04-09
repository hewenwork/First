#coding="utf-8"
import os
import re
import requests

def get_days_info(days):
    url = "https://malshare.com/daily/%s/malshare_fileList.%s.all.txt" % (days, days)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    respone = requests.get(url=url, headers=headers)
    for sha256 in respone.text.split("\n"):
        sha256 = sha256[74:138]
        



if __name__ == "__main__":
    days = "2017-11-08"
    get_days_info(days)