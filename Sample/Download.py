from os import makedirs, path
from urllib.parse import unquote
from urllib3 import disable_warnings
from requests_html import HTMLSession


def download(url, **kwargs):
    session = kwargs.setdefault("session", HTMLSession())
    params = ['headers', 'cookies', 'auth', 'proxies', 'hooks', 'params', 'verify',
              'cert', 'prefetch', 'adapters', 'stream', 'trust_env', 'max_redirects']
    option = {key: value for key, value in kwargs.items() if key in params}
    disable_warnings() if "verify" in option else None
    option.setdefault("stream", True)
    assert "http" in url, "http not in url"
    head = session.head(url, **option)
    status_code = head.status_code
    headers = head.headers
    assert status_code not in [301, 302], download(headers.setdefault("location"), **kwargs)
    assert status_code == 200, f"status_code: {status_code}"

    def get_file_name():
        disposition = headers.setdefault("Content-Disposition")
        if disposition is None:
            file_name_from_url = unquote(path.basename(url).split("?")[0])
        else:
            file_name_from_url = unquote(disposition.split("=")[-1].strip("\""))
        return file_name_from_url

    file_path = kwargs.setdefault("file_path")
    if file_path is None:
        file_name = kwargs.setdefault("file_name", get_file_name())
        file_dir = kwargs.setdefault("file_dir", path.dirname(__file__))
        file_path = path.join(file_dir, file_name)
    else:
        file_dir = path.dirname(file_path)
    makedirs(file_dir) if path.exists(file_dir) is False else None
    chunk_size = 1024 * 1024
    response = session.get(url, **option)
    headers = response.headers
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=chunk_size):
            file.write(chunk)
    return True
