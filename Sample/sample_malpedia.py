# encoding = utf-8
# @Author: Hewen
# @Time: 11/5/2019 7:33 PM
# @File: sample_malpedia.py
import requests
from bs4 import BeautifulSoup

session = requests.session()
session.headers[
    "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"


class Demo:

    def __init__(self):
        # url = "https://www.exterminate-it.com/malpedia/file/http_internetspeedtracker.dl.myway.com_0.localstorage"
        # url = "https://www.exterminate-it.com/malpedia/remove-adlogix"
        # self.get_detail(url, "AdLogix")
        with open(r"C:\Users\hewen\Desktop\malpedia.txt", "r")as file:
            for line in file.readlines():
                href = line.split(":    ")[-1].strip("\n")
                sample_name = line.split("         ")[0]
                print(sample_name)
                self.get_detail(href, sample_name)
                # if self.get_detail(href) is None:
                #     print(f"{href}   is  None")

    def get_href(self):
        char_list = [chr(page) for page in range(ord("a"), ord("z") + 1)]
        num_list = [chr(page) for page in range(ord("0"), ord("9") + 1)]
        page_list = char_list + num_list
        sample_dict = {}
        with open(r"C:\Users\hewen\Desktop\malpedia.txt", "w")as file:
            for page in page_list:
                for sample_name, sample_href in self.get_num(page).items():
                    url = f"https://www.exterminate-it.com{sample_href}"
                    line = f"{sample_name.ljust(50)}:    {url}\n"
                    file.write(line)
                sample_dict.update(self.get_num(page))
                print(page)
        print(len(sample_dict))

    @staticmethod
    def get_num(num):
        page = 1
        sample_dict = {}
        while page:
            url = f"https://www.exterminate-it.com/malpedia/starting-with-{num}/{page}"
            try:
                response = session.get(url)
                suop = BeautifulSoup(response.content, "lxml").select("div.encyclopedia_files > ul > li > a")
                page += 1
            except requests.RequestException as e:
                print(e)
                break
            else:
                for href in suop:
                    sample_name = href.getText()
                    sample_href = href.get("href")
                    if sample_name not in sample_dict.keys():
                        sample_dict[sample_name] = sample_href
                    else:
                        page = False
                        break
        return sample_dict

    @staticmethod
    def get_detail(url, sample_name):
        response = session.get(url)
        suop = BeautifulSoup(response.content, "lxml")
        gray_block = suop.select(f"div [title=\"{sample_name} Files\"] div div a")
        md5_file = open(r"C:\Users\hewen\Desktop\md.txt", "a+")
        if len(gray_block) != 0:
            for i in gray_block:
                i = i.get("href")
                url_detail = f"https://www.exterminate-it.com/malpedia/{i}"
                file_detail = Demo.get_file_md5(url_detail)
                if file_detail is not None:
                    for line in file_detail:
                        md5_file.write(f"{line}\n")
        else:
            return None
        md5_file.close()

    @staticmethod
    def get_file_md5(url):
        response = session.get(url)
        suop = BeautifulSoup(response.content, "lxml")
        melements = suop.select("div [class=\"variations gray_block\"] tr")
        if len(melements) == 0:
            return None
        else:
            line_list = []
            for i in melements:
                size, md5, add_date = i.select("td")
                size = size.getText()
                md5 = md5.getText()
                line = f"{md5},{size}"
                line_list.append(line)
            return line_list


if __name__ == "__main__":
    Demo()
