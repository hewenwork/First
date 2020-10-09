# -*- coding: UTF-8 -*-
"""
@author: Hewen
@file:IObitWeb.py
@time:2020/09/03
"""
from urllib.parse import urljoin
from requests_html import HTMLSession

session = HTMLSession()
attr = ["interface.iobit.com", "download.iobit.com", "update.iobit.com"]


def get_source(url_path):
    for url_base in attr:
        url = urljoin(url_base, url_path)
        response = session.head(url)
        if response.status_code == 200:
            return session.get(url).content
    return False


if __name__ == "__main__":
    print(urljoin(attr[0], "aa/aa.txt"))
