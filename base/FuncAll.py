# encoding = utf-8
# @Author: Hewen
# @Time: 1/21/2020 3:35 PM
# @File: FuncAll.py
import os
import hashlib
import logging

import requests


class FuncAll:

    def __init__(self):
        print(1)


def get_md5(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb")as file:
                content = file.read()
            md5 = hashlib.md5(content).hexdigest()
        except Exception as e:
            return False, e
        else:
            return True, md5
    else:
        return False, "file not exists"


def log(log_path):
    logger = logging.getLogger(__name__)
    logging.basicConfig(**{
        "level": logging.INFO,
        "format": "%(asctime)s - %(lineno)s - %(message)s",
        "filename": log_path
    })
    logger.addHandler(logging.StreamHandler())  # 输出屏幕
    return logger


class Download:

    def __init__(self, file_path, download_url, session=None, **kwargs):
        self.file_path = file_path
        self.download_url = download_url
        self.session = self.get_session(session)

    def result(self, **kwargs):
        stream = self.ifstram(**kwargs)
        if stream is not False:
            return self.download_chunk(stream)
        else:
            return self.download_normal(**kwargs)

    # 自建session
    @staticmethod
    def get_session(session):
        agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
        if session is None:
            session = requests.session()
            session.headers["user-agent"] = agent
        else:
            session = session
        return session

    # 是否支持流式下载
    def ifstram(self, **kwargs):
        try:
            result = self.session.get(self.download_url, stream=True, **kwargs)
            if result.status_code == 200:
                return result
            else:
                return 403
        except requests.exceptions.RequestException:
            return False

    # 断点续传
    def download_chunk(self, content):
        chunk_size = 1021 * 1024
        try:
            with open(self.file_path, "wb")as file:
                for chunk in content.iter_content(chunk_size=chunk_size):
                    file.write(chunk)
        except Exception as e:
            return e
        else:
            return True

    # 正常下载
    def download_normal(self, **kwargs):
        try:
            with open(self.file_path, "wb")as file, self.session.get(self.download_url, **kwargs)as content:
                file.write(content.content)
            return True
        except Exception as e:
            return e

    # 协程下载
    def download_muti(self):
        pass


if __name__ == "__main__":
    pass
