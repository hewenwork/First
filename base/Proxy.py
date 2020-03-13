# encoding = utf-8
# @Author: Hewen
# @Time: 11/28/2019 12:50 PM
# @File: Proxy.py
import os
import logging
import json
import socket

import requests
import telnetlib
from faker import Faker

option = {
    "filemode": "a+",
    "filename": f"{os.path.basename(__file__)}_debug.log",
    "level": logging.INFO,
    "format": "%(asctime)s--: %(lineno)d: %(funcName)s: %(levelname)s - %(message)s"
}
logging.basicConfig(**option)
log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())  # print in screen


class Proxy:

    def __init__(self):
        self.session = self.init_session()
        a = self.get_proxy_dict()
        print(a)

    @staticmethod
    def init_session():
        session_ = requests.session()
        header = Faker().user_agent()
        session_.headers["User-Agent"] = header
        return session_

    def get_proxy_dict(self):
        url = "https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list"
        proxies_dict = {
            "http": [],
            "https": []
        }
        try:
            result = self.session.get(url).text.replace("\n", ",")
            for line in result.split("\n")[-1]:
                line_dict = json.loads(line)
                host = line_dict["host"]
                port = line_dict["port"]
                proxy = {host: port}
                if line_dict["type"] == "http":
                    proxies_dict["http"].append(proxy)
                else:
                    proxies_dict["https"].append(proxy)
        except requests.RequestException as e:
            log.info(e)
        except json.decoder.JSONDecodeError as e:
            log.info(e)
        else:
            return proxies_dict

    @staticmethod
    def verify(host, port):
        verify_url = "http://icanhazip.com"
        try:
            telnetlib.Telnet(host, port, timeout=5)
        except socket.timeout as e:
            log.info(e)
            return False
        else:
            return True


if __name__ == "__main__":
    Proxy()
