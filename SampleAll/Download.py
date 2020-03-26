import os
from contextlib import closing
from requests_html import HTMLSession


def download(file_path, link, sessions=None, **option):
    session = HTMLSession() if sessions is None else sessions
    session.keep_alive = False
    if os.path.exists(file_path):
        return False, f"file exists:{file_path}."
    try:
        with closing(session.get(link, **option))as response:
            if response.status_code == 200:
                response = response.content
                with open(file_path, "wb")as file:
                    file.write(response)
                return True, file_path
            else:
                return False, f"file download failed. code: {response.status_code}, link: {link}."
    except Exception as e:
        return False, f"file download failed error: {e}.  link:{link}."


def download_iter(file_path, link, sessions=None, **kwargs):
    session = HTMLSession() if sessions is None else sessions
    try:
        response = sessions.get(url=link, stream=True)
        if response.status_code != 200:
            return False
        with open(file_path, "wb")as file:
            for chunk in response.iter_content():
                file.write(chunk)
        return True, file_path
    except Exception as e:
        return False, e


if __name__ == "__main__":
    # _f = r"C:\Users\hewen\Desktop\A00.gz"
    # a = "https://www.hybrid-analysis.com/download-sample/6a4610e5f3ebb3f603592a1e624bd89dd9626c77f8b90d2945586c0c631a21ff"
    print(session.get(
        "https://www.hybrid-analysis.com/download-sample/57a0b85c775c8808d016dd89207dce3e481f9160a57f947504317510369719f8"))
