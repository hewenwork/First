import os
import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from subprocess import check_output

download_date = "2020-03-18"


def decompression_file(target_path, pwd="infected"):
    if os.path.exists(target_path):
        file_type = target_path[-3:]
        dist_path = target_path.split(".")[0] + ".vir"
        type_command = {
            "rar": f"rar e -p{pwd} -y \"{target_path}\" \"{dist_path}\"",
            "7z": f"7z e -p{pwd} -y \"{target_path}\" -so > \"{dist_path}\"",
            "zip": f"7z e -p{pwd} -y \"{target_path}\" -so > \"{dist_path}\"",
            ".gz": f"7z e -p{pwd} -y \"{target_path}\" -so > \"{dist_path}\"",
        }
        if file_type in type_command is False:
            return True
    else:
        return False
    try:
        command = type_command[file_type]
        check_output(command, shell=True)
        os.remove(target_path)
    except Exception as e:
        return f"  error: {e}"


class Vx(scrapy.Spider):
    name = "sample_vx"
    start_urls = ["http://vxvault.net/ViriList.php"]

    def parse(self, response):
        soup = BeautifulSoup(response.body.decode("iso-8859-1"), "lxml")
        for i in soup.select("tr > td:nth-of-type(1) > a"):
            sample_link = "http://vxvault.net/" + i.attrs["href"]
            yield Request(url=sample_link, callback=self.son)

    def son(self, response):
        sample_date = re.findall(r"<B>Added:</B> (.*?)<BR>", response.body.decode("iso-8859-1"))[0]
        sample_md5 = re.findall(r"<B>MD5:</B> (.*?)<BR>", response.body.decode("iso-8859-1"))[0]
        sample_url = f"http://" + re.findall(r"<B>Link:</B> hxxp://(.*?)<BR>", response.body.decode("iso-8859-1"))[0]
        sample_info = {
            "sample_path": sample_md5,
            "sample_url": sample_url
        }
        print(sample_info)
        if sample_date == download_date:
            yield Request(url=sample_url, callback=self.son)
        elif sample_date < download_date:
            return

    def down(self, sample_info, response):
        Init_dir = r"G:\AutoCollect"
        sample_dir = os.path.join(Init_dir, download_date)  # 存放Sample
        sample_path = os.path.join(sample_dir, sample_info["sample_path"])
        with open(sample_path, "wb")as file:
            file.write(response)

            #         result = session.get(sample_link)
        #         sample_date = re.findall(r"<B>Added:</B> (.*?)<BR>", result.text)[0]
        #         if sample_date == download_date:
        #             sample_md5 = re.findall(r"<B>MD5:</B> (.*?)<BR>", result.text)[0]
        #             sample_url = f"http://" + re.findall(r"<B>Link:</B> hxxp://(.*?)<BR>", result.text)[0]
        #             sample_info = {
        #                 "sample_path": os.path.join(sample_dir, sample_md5 + ".vir"),
        #                 "sample_url": sample_url
        #             }
        #             sample_dict.update({sample_md5: sample_info})
        #         elif sample_date < download_date:
        #             break
        #     return sample_dict
        # except Exception as e:
        #     return f"error: {e}"
        # add_date = response.css("#page > table > tbody > tr:nth-child(2) > td:nth-child(1) > a")
        # print(add_date)
