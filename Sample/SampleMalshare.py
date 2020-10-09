# -*- coding: UTF-8 -*-
"""
@author: Hewen
@file:SampleMalshare.py
@time:2020/09/02
"""
from re import findall
from chardet import detect
from urllib.parse import unquote
from urllib3 import disable_warnings
from requests_html import HTMLSession
from datetime import datetime, timedelta
from os import makedirs, path, popen, listdir
from subprocess import check_output, SubprocessError

log_dir = path.join(path.dirname(__file__), "Log")
makedirs(log_dir) if path.exists(log_dir) is False else None
log_name = "{}{}.log".format(path.basename(__file__), datetime.today().strftime("%Y%m%d"))
log_path = path.join(log_dir, log_name)


def log(function):
    def run(*args, **kwargs):
        function_name = function.__name__
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            result = "function: {}, Exception:{}".format(function_name, e)
        line = "{}: {}\n".format(datetime.today(), result)
        with open(log_path, "a+", encoding="utf-8")as file:
            file.write(line)
        return result

    return run


@log
def archive(file_path, pwd="infected", **kwargs):
    file_dir = path.dirname(file_path)
    archive_name = kwargs.setdefault("archive_name", path.basename(file_path).split(".")[0])
    archive_path = kwargs.setdefault("archive_path", path.join(file_dir, archive_name))
    command = "7z a \"{}\" \"{}\\*\" -p{} -y".format(archive_path, file_path, pwd)
    output = check_output(command, shell=False)
    encoding = detect(output)["encoding"]
    out = output.decode(encoding=encoding)
    return archive_path if "Ok" in out else out


@log
def extract(file_path, **kwargs):
    password = kwargs.setdefault("password", "infected")
    dist_dir = kwargs.setdefault("dist_dir", path.dirname(file_path))
    makedirs(dist_dir) if path.isdir(dist_dir) and path.exists(dist_dir) is False else None
    command = "7z e \"{}\" -o\"{}\" -p{} -y -r".format(file_path, dist_dir, password)
    try:
        output = check_output(command, shell=False)
        encoding = detect(output)["encoding"]
        out = output.decode(encoding=encoding)
        return True if "Ok" in out else out
    except SubprocessError as out:
        cmd_delete(file_path)
        return out


@log
def cmd_copy(file_path, dist_path):
    makedirs(dist_path) if path.exists(dist_path) is False else None
    command = "copy \"{}\" \"{}\"".format(file_path, dist_path)
    output = popen(command)
    out = output.read()
    return True if "copied" in out else out


@log
def cmd_delete(file_path):
    command = "RD /S /Q \"{}\"".format(file_path) if path.isdir(file_path) else "DEl /Q \"{}\"".format(file_path)
    output = popen(command)
    out = output.read()
    return True if out == "" else out


@log
def cmd(command, **kwargs):
    file_path = kwargs.setdefault("file_path")
    dist_dir = kwargs.setdefault("dist_dir")
    dist_path = kwargs.setdefault("dist_path")
    command_dict = {
        "copy": f"copy /y \"{file_path}\" \"{dist_dir}\"",
        "move": f"move /y \"{file_path}\" \"{dist_dir}\"",
        "rename": f"rename /y \"{file_path}\" \"{dist_path}\"",
        "delete": f"RD /S /Q \"{file_path}\"" if path.isdir(file_path) else f"DEl /Q \"{file_path}\""
    }
    command = command_dict[command]
    output = check_output(command, shell=False)
    encoding = detect(output)["encoding"]
    out = output.decode(encoding=encoding)
    return out


@log
def download(url, **kwargs):
    session = kwargs.setdefault("session", HTMLSession())
    params = ['headers', 'cookies', 'auth', 'proxies', 'hooks', 'params', 'verify',
              'cert', 'prefetch', 'adapters', 'stream', 'trust_env', 'max_redirects']
    option = {key: value for key, value in kwargs.items() if key in params}
    disable_warnings() if "verify" in option else None
    option.setdefault("stream", True)
    assert "http" in url, f"http not in url:{url}"
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
    # file_size = path.getsize(file_path) if path.exists(file_path) else 0
    # file_mode = "wb" if file_size == 0 else "ab"
    chunk_size = 1024 * 1024
    response = session.get(url, **option)
    headers = response.headers
    # total_size = int(headers.setdefault("content-length", "0"))
    # if total_size == file_size:
    #     return True
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=chunk_size):
            file.write(chunk)
    return True


class CMD:

    @staticmethod
    def archive(file_path, **kwargs):
        pass

    @staticmethod
    def extract(file_path, **kwargs):
        pass

    @staticmethod
    def execute(command):
        try:
            output = check_output(command, shell=False)
            encoding = detect(output).setdefault("encoding")
            out = output.decode(encoding=encoding)
            return out
        except SubprocessError as e:
            return e
        except LookupError as e:
            return e


class Sample:

    def __init__(self, **kwargs):
        session = HTMLSession()
        date = kwargs.setdefault("date", datetime.today() - timedelta(days=1))
        sample_link_list = map(self.get_download_url, self.get_all_md5(session, date))
        self.sample_link_list = list(sample_link_list)
        self.download_date = date

    @staticmethod
    def get_all_md5(session, date):
        data_string = date.strftime("%Y-%m-%d")
        url = f"https://malshare.com/daily/{data_string}/malshare_fileList.{data_string}.all.txt"
        md5_text = session.get(url).text
        md5_tuple = set(findall(r"\b(\w{32})\b", md5_text))
        return md5_tuple

    @staticmethod
    def get_download_url(md5):
        api = "2befc1c0b4d476b8527887f3f415648050638eff8dd400071f694e7356d5e49a"
        url = f"https://malshare.com/api.php?api_key={api}&action=getfile&hash={md5}"
        return url

    def __call__(self):
        sample_link_list = self.sample_link_list
        date = self.download_date
        return sample_link_list, date


class Run:

    def __init__(self):
        sm_dir = r"G:\Auto"
        sample_dir = r"G:\AutoSample\Malshare"
        temp_dir = r"G:\AutoSample\Malshare\Temp"
        makedirs(temp_dir) if path.exists(temp_dir) is False else None
        sample_list, download_date = Sample().__call__()
        for url in sample_list:
            download(url, file_dir=temp_dir)
        # for file_name in listdir(temp_dir):
        #     file_path = path.join(temp_dir, file_name)
        #     extract(file_path)
        #     cmd_delete(file_path)
        # file_path_list = [path.join(temp_dir, file_name) for file_name in listdir(temp_dir)]
        # for file_path in file_path_list:
        #     cmd_delete(file_path) if path.isdir(file_path) else None
        archive_name = "[infected]{}_Malshare.zip".format(download_date.strftime("%Y%m%d"))
        archive_path = path.join(sample_dir, archive_name)
        archive(temp_dir, archive_path=archive_path)
        cmd_copy(archive_path, sm_dir)
        cmd_delete(temp_dir)


if __name__ == "__main__":
    Run()
