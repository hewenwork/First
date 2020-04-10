import os
from time import sleep
from datetime import datetime

from requests import RequestException
from requests_html import HTMLSession
from urllib3 import HTTPConnectionPool, HTTPSConnectionPool


# def download(file_path=None, url=None, **kwargs):
#     if file_path is None:
#         return False, "No path to save."
#     if os.path.exists(file_path):
#         return False, f"File exists {file_path}."
#     file_dir = os.path.dirname(file_path)
#     if os.path.exists(file_dir) is False:
#         try:
#             os.makedirs(file_dir)
#         except Exception as e:
#             return False, f"Make dir {file_dir} Exception: {e}."
#     if url is None:
#         return False, f"No url to Requests."
#     session = kwargs.setdefault("session", HTMLSession())
#     method = kwargs.setdefault("method", "get")
#     verify = kwargs.setdefault("verify", True)
#     option = {
#         "auth": kwargs.setdefault("auth"),
#         "params": kwargs.setdefault("params"),
#         "stream": kwargs.setdefault("stream", True),
#         "timeout": (30, 30),
#         "verify": verify
#     }
#     try:
#         response = session.request(method=method, url=url, **option)
#         status_code = response.status_code
#         if status_code != 200:
#             return False, f"Request {url} Failed status_code: {status_code}"
#     except Exception as e:
#         return False, f"Request {url} Exception: {e}"
#     try:
#         with open(file_path, "wb")as file:
#             content_length = response.headers.setdefault("content-length")
#             if content_length is None:
#                 file.write(response.content)
#             elif option["stream"]:
#                 file_size = 0
#                 total_size = int(content_length)
#                 if option["stream"]:
#                     for chunk in response.iter_content(chunk_size=1024):
#                         file.write(chunk)
#                         file.flush()
#                         file_size += len(chunk)
#                         percent = "{:.2%}".format(file_size / total_size)
#                         print(f"\r{datetime.today()}: {file_size}/{total_size}-- percent:{percent}", end="")
#                     print()
#             else:
#                 file.write(response.content)
#         return True, f"Download successful: {file_path}."
#     except Exception as e:
#         if os.path.exists(file_path):
#             os.remove(file_path)
#         return False, f"Save {file_path} Exception: {e}."


def download(file_path, url, **kwargs):
    if file_path is None:
        return False, "No path to save."
    file_dir = os.path.dirname(file_path)
    if os.path.exists(file_dir) is False:
        try:
            os.makedirs(file_dir)
        except Exception as e:
            return False, f"Make dir {file_dir} Exception: {e}."
    if url is None:
        return False, f"No url to Requests."
    session = kwargs.setdefault("session", HTMLSession())
    method = kwargs.setdefault("method", "get")
    verify = kwargs.setdefault("verify", True)
    option = {
        "auth": kwargs.setdefault("auth"),
        "params": kwargs.setdefault("params"),
        "stream": kwargs.setdefault("stream", True),
        "timeout": (30, 20),
        "verify": verify
    }
    if os.path.exists(file_path):
        with open(file_path, "rb")as file:
            file_size = len(file.read())
    else:
        file_size = 0
    session.headers.update({"Range": f"bytes={file_size}-"})
    response = session.request(method=method, url=url, **option)
    status_code = response.status_code
    if status_code == 416:
        return False, f"Request: {url}, status_code: {status_code}.Range overflow."
    if status_code == 404:
        return False, f"Request: {url}, status_code: {status_code}.data not found."
    if status_code == 403:
        return False, f"Request: {url}, status_code: {status_code}.Access Denied."
    if status_code == 429:
        return False, f"Request: {url}, status_code: {status_code}.Too Many Requests."
    response_size = response.headers.setdefault("content-length")
    total_size = int(response_size) + file_size #if response_size is not None else None
    # if total_size is None:
    #     return False, f"total_size Exception: {total_size}."
    if total_size == file_size:
        return True, f"File has download. file_size: {file_size}."
    if status_code == 206:
        try:
            with open(file_path, "ab+")as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
                    file.flush()
                    file_size += len(chunk)
                    percent = "{:.2%}".format(file_size / total_size)
                    print(f"\r{datetime.today()}: {file_size}/{total_size}-- percent:{percent}", end="")
                print()
                return True, "Download Ok"
        except RequestException:
            print("download again.")
            download(file_path, url, **kwargs)


if __name__ == "__main__":
    a = {'sample_md5': '02e9055087d07e2008bbf96f86e889a5', 'sample_name': '02e9055087d07e2008bbf96f86e889a5.vir',
         'sample_url': 'http://virusign.com/file/63f963084ffabe7564bb790ceb2e1a9c25c812fbdc2f341496f6b78e52320ead.7z',
         'is_archive': True,
         'auth': ("infected", "infected")
         }
    a_ = r"G:\AutoCollect\2020-03-28\02e9055087d07e2008bbf96f86e889a5.vir"
    b_ = "http://unlimitedimportandexport.com/wp-content/plugins/all-in-one-wp-migration/lib/bread.exe"
    aa = download(a_, b_, **a)
    print(aa)
