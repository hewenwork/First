# encoding = utf-8
# @Author: Hewen
# @Time: 11/28/2019 12:50 PM
# @File: Proxy.py
import os
import re
import telnetlib
import requests_html

session = requests_html.HTMLSession()


class Proxy:

    def __init__(self):
        a = self.get_proxy_dict()
        print(a)

    @staticmethod
    def verify(host, port):
        try:
            telnetlib.Telnet(host, port, timeout=5)
            return {host: port}
        except Exception as e:
            return e

    @staticmethod
    def get_proxy_dict():
        url = "https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list"
        try:
            result = session.get(url).text
            for proxy_type in re.findall(r"\"type\": \"(.*?)\"", result):
                print(proxy_type)
            return {
                proxy_type: {host: port}
                for proxy_type in re.findall(r"\"type\": \"(.*?)\"", result)
                for host in re.findall(r"\"host\": \"(.*?)\"", result)
                for port in re.findall(r"\"port\": \"(.*?)\",", result)
            }
        except Exception as e:
            return e


if __name__ == "__main__":
    Proxy()
