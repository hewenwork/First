# encoding = utf-8
# @Author: Hewen
# @Time: 11/21/2019 10:37 AM
# @File: IPPool.py
import json
import socket
import requests
import telnetlib
from faker import Faker


class IPPool:

    def __init__(self):
        self.session = self.init_session()
        # ip_dict = self.get_ip_dict()
        # for host, port in ip_dict.items():
        #     result = self.verify(host, port)
        #     if result:


    @staticmethod
    def init_session():
        session_ = requests.session()
        header = Faker().user_agent()
        session_.headers["User-Agent"] = header
        return session_

    def get_ip_dict(self):
        url = "https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list"
        try:
            proxies_dict = {
                "http": [],
                "https": []
            }
            result = self.session.get(url).content.decode()
            for line in result.split("\n")[:-1]:
                line_dict = json.loads(line)
                host = line_dict["host"]
                port = line_dict["port"]
                proxy = {host: port}
                if line_dict["type"] == "http":
                    proxies_dict["http"].append(proxy)
                else:
                    proxies_dict["https"].append(proxy)
        except requests.RequestException as e:
            exit(f"Http error :{e}")
        except json.decoder.JSONDecodeError as e:
            exit(f"Json error :{e}")
        else:
            return proxies_dict

    @staticmethod
    def verify(proxy):
        verify_url = "http://icanhazip.com"
        try:
            telnetlib.Telnet(host, port, timeout=5)
            result = requests.get(verify_url, proxies=proxy).text
        except socket.timeout:
            return False
        else:
            if host == result:
                return True
            else:
                return False


if __name__ == "__main__":
    IPPool()
