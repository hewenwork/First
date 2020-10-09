from urllib import parse
from shutil import rmtree
from bs4 import BeautifulSoup
from re import findall, match
from subprocess import check_output
from requests_html import HTMLSession
from datetime import datetime, timedelta
from os import path, remove, listdir, makedirs, popen

log_dir = path.join(path.dirname(__file__), "Log")
makedirs(log_dir) if path.exists(log_dir) is False else None
log_path = path.join(log_dir, datetime.today().strftime("%Y-%m-%d.log"))


def log(function):
    def write_log(*args, **kwargs):
        function_name = function.__name__
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            result = "Exception:{}".format(e)
        with open(log_path, "a+", encoding="utf-8")as file:
            attr = datetime.today(), function_name, result
            line = "{}: function: {}, result:{}\n".format(*attr)
            file.write(line)
        return result

    return write_log


@log
def download(**kwargs) -> bool or str:
    url = kwargs.setdefault("url")
    session = kwargs.setdefault("session", HTMLSession())
    requests_params = ['headers', 'cookies', 'auth', 'proxies', 'hooks', 'params', 'verify',
                       'cert', 'prefetch', 'adapters', 'stream', 'trust_env',
                       'max_redirects']
    option = {key: value for key, value in kwargs.items() if key in requests_params}
    option.setdefault("stream", True)
    while True:
        response = session.head(url, **option)
        status_code = response.status_code
        headers = response.headers
        if status_code == 301 or status_code == 302:
            url = headers["location"]
        elif status_code == 200:
            break
        else:
            return "获取错误, URL:{} status_code{}".format(url, status_code)
    file_dir = kwargs.setdefault("file_dir", path.dirname(__file__))
    makedirs(file_dir) if path.exists(file_dir) is False else None
    file_name = kwargs.setdefault("file_name")
    if file_name is None:
        content_disposition = headers.setdefault("Content-Disposition")
        if content_disposition is None:
            file_name = datetime.today().strftime("%Y%m%d%H%M%S.7z")
        else:
            file_name = parse.unquote(content_disposition.split("filename=")[-1].strip("\""))
    file_path = kwargs.setdefault("file_path", path.join(file_dir, file_name))
    if path.exists(file_path):
        file_dir = path.dirname(file_path)
        file_name = "new_{}".format(path.basename(file_path))
        file_path = path.join(file_dir, file_name)
    with open(file_path, "wb") as file:
        chunk_size = 1024 * 1024
        for chunk in session.get(url, **option).iter_content(chunk_size=chunk_size):
            file.write(chunk)
    return True


class Archive:

    @staticmethod
    @log
    def archive(file_path, pwd="infected", archive_name=None, archive_path=None):
        if archive_path is None:
            base_name = path.basename(file_path).split(".")[0]
            if archive_name is None:
                archive_name = "[{}]{}.zip".format(pwd, base_name)
            archive_path = path.join(path.dirname(file_path), archive_name)
        command = "7z a \"{}\" \"{}\" -p{} -y".format(archive_path, file_path, pwd)
        output = check_output(command, shell=False)
        out = output.decode()
        return archive_path if "Ok" in out else out

    @staticmethod
    @log
    def extract(file_path, dist_path=None, pwd="infected"):
        dist_path = path.dirname(file_path) if dist_path is None else dist_path
        makedirs(dist_path) if path.isdir(dist_path) and path.exists(dist_path) is False else None
        command = "7z e \"{}\" -o\"{}\" -p{} -y -r".format(file_path, dist_path, pwd)
        print(command)
        output = check_output(command, shell=False)
        out = output.decode()
        return True if "Ok" in out else out

    @staticmethod
    @log
    def trans(file_path, dist_path):
        makedirs(dist_path) if path.exists(dist_path) is False else None
        command = "copy \"{}\" \"{}\"".format(file_path, dist_path)
        output = popen(command)  # check_output(command, shell=False)
        out = output.read()
        return True if "copied" in out else out

