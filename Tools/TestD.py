# encoding = utf-8
# @Author: Hewen
# @Time: 12/17/2019 5:10 PM
# @File: TestD.py
import os
import logging

logging.basicConfig(**{
    "filemode": "a+",
    "filename": f"{os.path.basename(__file__)}_debug.log",
    "level": logging.INFO,
    "format": "%(asctime)s--: %(lineno)d: %(funcName)s: %(levelname)s - %(message)s"
})
log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())  # print in screen


class TestD:

    def __init__(self):
        b = r"C:\Users\hewen\Desktop\CookieFix-04.db"
        a = r"C:\Users\hewen\Desktop\CookieFix-12.db"
        dict_a = {}
        with open(a, encoding="utf-8")as file:
            content = file.readlines()
            for line in content:
                line = line.split(",")[0]
                dict_a[line] = 0
        with open(b, encoding="utf-8")as file:
            for line in file.readlines():
                line = line.split(",")[0]
                if line in dict_a:
                    print(line)

if __name__ == "__main__":
    TestD()
