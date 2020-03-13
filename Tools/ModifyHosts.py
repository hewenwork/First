# encoding = utf-8
# @Author: Hewen
# @Time: 10/24/2019 10:41 AM
# @File: ModifyHosts.py
import os
hosts_path = r"C:\Windows\System32\drivers\etc\hosts"


class ModifyHosts:

    def __init__(self):
        with open(hosts_path, "a+")as file:
            file.write("hello")


if __name__ == "__main__":
    ModifyHosts()
