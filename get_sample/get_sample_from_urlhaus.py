import os
import re
import requests
import datetime
from bs4 import BeautifulSoup


count_num = 1
def get_sample(url, sample_ID):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    download_path = os.path.join(download_folder, "%s.vir" % sample_ID)
    try:
        sample = requests.get(url=url, headers=headers, timeout=20).content
        with open(download_path, "wb")as file:
            file.write(sample)
    except Exception as e:
        print(e)


def get_info(num):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    url = "https://urlhaus.abuse.ch/browse/page/%s/" % num
    respone = requests.get(url=url, headers=headers)
    suop = BeautifulSoup(respone.text, "lxml")
    for sample_data_date in suop.select("tbody > tr > td:nth-of-type(1)"):
        global count_num
        print(count_num)
        count_num += 1
        sample_data_date = sample_data_date.getText()[:10]
        if sample_data_date == yestoday:
            for sample_data in suop.select("tbody > tr > td:nth-of-type(2) > a"):
                sapmle_info_url = "https://urlhaus.abuse.ch%s" % sample_data.get("href")
                sapmle_respone = requests.get(url=sapmle_info_url, headers=headers)
                sample_date = re.findall("Date added:\<\/th\>\<td\>(.*)\<\/td\>\<\/tr\>", sapmle_respone.text)[0][:10]
                sample_download_url = re.findall("URL:\<\/th\>\<td\>(.*)\<\/td\>\<\/tr\>", sapmle_respone.text)[0]
                sample_ID = re.findall("ID:\<\/th\>\<td\>(.*)\<\/td\>\<\/tr\>", sapmle_respone.text)[0]
                if sample_date == yestoday:
                    print(sample_date, sample_download_url, sample_ID)
                    get_sample(sample_download_url, sample_ID)
                elif sample_date <= yestoday:
                    num = -1
                    break

def get_page():
    num = 1
    while num != -1:
        get_info(num)
        num += 1


# yestoday = datetime.datetime.today() - datetime.timedelta(days=1)
# yestoday = yestoday.strftime("%Y-%m-%d")
yestoday = "019-03-27"
download_folder = r"C:\Users\hewen\Desktop\auto\%s" % yestoday
if os.path.exists(download_folder) == False:
    os.makedirs(download_folder)
# get_info()
get_page()