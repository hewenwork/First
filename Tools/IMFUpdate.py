# encoding = utf-8
# @Author: Hewen
# @Time: 10/29/2019 4:39 PM
# @File: IMFUpdate.py
import hashlib
import os
import zlib
import random


class IMFUpdate:

    def __init__(self):
        file_path_1 = r"C:\Users\hewen\Desktop\file1.exe"
        file_path_2 = r"C:\Users\hewen\Desktop\file2.exe"
        file_path_3 = r"C:\Users\hewen\Desktop\file3.ini"
        file_path_zlb = r"C:\Users\hewen\Desktop\zlb.zlb"
        with open(file_path_1, "rb")as file1:
            file_content1 = file1.read()
        with open(file_path_2, "rb")as file2:
            file_content2 = file2.read()
        with open(file_path_3, "rb")as file3:
            file_content3 = file3.read()
        with open(file_path_zlb, "wb")as file_zlb:
            data = file_content1 + file_content2 + file_content3
            file_zlb.write(zlib.compress(data))
        self.decom(1)


        # md5 = self.file_md5(r"C:\Users\hewen\Desktop\aaaa.zlb")
        # size = os.path.getsize(r"C:\Users\hewen\Desktop\aaaa.zlb")
        # for i in range(-1, 10):
        #     md51, size1 = self.com(i)
        #     print(md5, "", size, "   ", md51, " ", size1)
        #     if md5 == md51:
        #         print(i)

    @staticmethod
    def com(num):

        file_path = r"C:\Users\hewen\Desktop\aa.exe"
        new = r"C:\Users\hewen\Desktop\aa.zlb"
        with open(file_path, "rb")as file, open(new, "wb") as zlb:
            data = zlib.compress(file.read(), level=num)
            zlb.write(data)

        return IMFUpdate.file_md5(new), os.path.getsize(new)

    @staticmethod
    def decom(file_path):
        file_path = r"C:\Users\hewen\Desktop\zlb.zlb"
        with open(file_path, "rb")as file:
            result = zlib.decompress(file.read())
            with open(r"C:\Users\hewen\Desktop\bb.exe", "wb")as ff:
                ff.write(result)

    @staticmethod
    def file_md5(file_path):
        md5_object = hashlib.md5()
        try:
            with open(file_path, "rb")as file:
                md5_object.update(file.read())
            md5_result = md5_object.hexdigest()
        except Exception as e:
            print(e)
            return False
        else:
            return md5_result


if __name__ == "__main__":
    IMFUpdate()
    # threats = ["Keylogger.FakeAlert", "Trojan.Agnet", "Misleading.FakeAV", "AdWare.AdBar", "Spyware.BrowserPal"]
    # num = ["1890", "1901", "1899", "1889", "1888"]
    # start = 5000126
    # # IMFUpdate()
    # ff = r"C:\Users\hewen\Desktop\wjc\去重排序后 - Copy.txt"
    # with open(ff, "r")as file:
    #     aa = file.readlines()
    #     with open(r"C:\Users\hewen\Desktop\wjc\去.txt", "w")as nn:
    #         for line in aa:
    #             start += 1
    #             line = f"{start},{random.choice(num)},{random.choice(threats)},{line}"
    #             nn.write(line)
