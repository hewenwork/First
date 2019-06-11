import requests


class VirusShareMd5:

    def __init__(self):
        url = "https://virusshare.com/hashes/VirusShare_"
        url_list = [url + "00{}.md5".format(i).zfill(3) for i in range(0, 366)]
        for i in url_list:
            print(i)


VirusShareMd5()
# file_path = r"C:\Users\hewen\Desktop\00000.md5.txt"
# with open(file_path, "r+")as file:
#     file.seek(202)
#     old_data = file.read()
#     file.seek(0, 0)
#     file.write(old_data)