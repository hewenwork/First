# encoding = utf-8
# @Author: Hewen
# @Time: 10/14/2019 10:31 AM
# @File: DouDou.py
import requests as rs
import urllib3

urllib3.disable_warnings()


class DouDou:

    def __init__(self):
        uid = "6745743096291707659"
        url = f'https://api.amemv.com/aweme/v1/aweme/post/?max_cursor=0&user_id={uid}&count=20&aid=1128'
        h = {'user-agent': 'mobile'}
        req = rs.get(url, headers=h, verify=False)
        data = req.json()
        print(data)

if __name__ == "__main__":
    DouDou()
