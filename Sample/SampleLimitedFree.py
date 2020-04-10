import os
import requests_html
from contextlib import closing
from datetime import datetime, timedelta


def sample_LimitedFree(download_date):
    download_dir = r"G:\LimitedFree"
    sample_date = download_date.strftime("%Y%m%d")
    sample_name = f"virussign.com_{sample_date}_LimitedFree.zip"
    sample_url = f"http://samples.virussign.com/samples/{sample_name}"
    sample_info = {
        "sample_path": os.path.join(download_dir, sample_name),
        "sample_name": sample_name,
        "sample_url": sample_url,
        "auth": ("f_yunwing1", "9kkSkk3dSd"),
        "stream": True,
        "is_archive": True
    }
    return True, {f"{sample_name}": sample_info}


def get_path_link():
    download_dir = r"G:\LimitedFree"
    init_date = datetime(2020, 3, 3)
    download_date = init_date.strftime("%Y%m%d")
    file_name = f"virussign.com_{download_date}_LimitedFree.zip"
    file_path = os.path.join(download_dir, file_name)
    download_link = f"http://samples.virussign.com/samples/{file_name}"
    if os.path.exists(file_path) is False:
        with open(file_path, "w")as file:
            file.write("this init file, don`t delete it.")
    while os.path.exists(file_path):
        init_date = init_date + timedelta(days=1)
        download_date = init_date.strftime("%Y%m%d")
        file_name = f"virussign.com_{download_date}_LimitedFree.zip"
        file_path = os.path.join(download_dir, file_name)
        download_link = f"http://samples.virussign.com/samples/{file_name}"
    auth = ("f_yunwing1", "9kkSkk3dSd")
    option = {
        "auth": auth,
        "stream": True
    }
    session = requests_html.HTMLSession()
    with closing(session.get(download_link, **option))as content:
        download_size = 0
        chunk_size = 1024
        content_size = content.headers["Content-Length"]
        with open(file_path, "wb")as file:
            for chunk in content.iter_content(chunk_size=chunk_size):
                file.write(chunk)
                download_size += chunk_size
                print(f"\r{download_size}/ {content_size}", end="")


def run():
    while True:
        try:
            get_path_link()
        except Exception as e:
            information = f"{datetime.today()}: {e}\n"
            with open(r"LimitedFree.log", "a+")as log:
                log.write(information)
            break


if __name__ == "__main__":
    a = sample_LimitedFree(datetime.today())
    print(a)
