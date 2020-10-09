from re import match
from urllib import parse
from bs4 import BeautifulSoup
from shutil import rmtree, move
from subprocess import check_output
from requests_html import HTMLSession
from datetime import datetime, timedelta
from os import path, remove, listdir, makedirs, popen

# todo 未完成, 转移有问题, 下载未完成
smart_dir = r"G:\Auto"
error_dir = r"G:\Error"
sample_dir = r"G:\AutoSample\Hybird"
log_dir = path.join(sample_dir, "Log")
log_name = "{}.log".format(datetime.today().strftime("%Y-%m-%d"))
log_path = path.join(log_dir, log_name)
makedirs(log_dir) if path.exists(log_dir) is False else None


def log(function):
    def write_log(*args, **kwargs):
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            result = "Exception:{}".format(e)
        with open(log_path, "a+", encoding="utf-8")as file:
            function_name = function.__name__
            attr = datetime.today(), function_name, result
            line = "{}: function: {}, result:{}\n".format(*attr)
            file.write(line)
        return result

    return write_log


@log
def archive(file_path, archive_name=None, archive_path=None, pwd="infected"):
    if archive_path is None:
        if archive_name is None:
            base_name = path.basename(file_path).split(".")[0]
            archive_name = "[{}]{}.zip".format(pwd, base_name)
        archive_path = path.join(path.dirname(file_path), archive_name)
    command = "7z a \"{}\" \"{}\" -p{} -y".format(archive_path, file_path, pwd)
    output = check_output(command, shell=False)
    out = output.decode()
    return archive_path if "Ok" in out else out


@log
def extract(file_path, dist_path=None, pwd="infected"):
    dist_path = path.dirname(file_path) if dist_path is None else dist_path
    makedirs(dist_path) if path.isdir(dist_path) and path.exists(dist_path) is False else None
    command = "7z e \"{}\" -o\"{}\" -p{} -y -r".format(file_path, dist_path, pwd)
    output = check_output(command, shell=False)
    out = output.decode()
    return True if "Ok" in out else out


@log
def copy(file_path, dist_path):
    makedirs(dist_path) if path.exists(dist_path) is False else None
    command = "copy \"{}\" \"{}\"".format(file_path, dist_path)
    output = popen(command)
    out = output.read()
    return True if "copied" in out else out


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


@log
def move2smartccl(file_dir, archive_name=None):
    re = r".*\.zip|.*\.rar|.*\.gz|.*\.7z"
    file_path_list = [path.join(file_dir, file_name) for file_name in listdir(file_dir)]
    if len(file_path_list) == 0:
        return "今天没有任何数据"
    for file_path in file_path_list:
        if match(re, file_path) and len(file_path_list) == 1:
            copy(file_path, smart_dir)
            move(path.dirname(file_path), smart_dir)
            break
        elif match(re, file_path) and len(file_path_list) > 1:
            remove(file_path) if extract(file_path) else move(file_path, error_dir)
    else:
        # archive_name = archive_name if archive_name else
        archive_path = archive(file_dir, archive_name=archive_name)
        copy(archive_path, smart_dir)
    rmtree(file_dir)


class Hybird:
    date = datetime.today() - timedelta(days=1)
    file_dir = path.join(sample_dir, date.strftime("%Y-%m-%d"))
    makedirs(file_dir) if path.exists(file_dir) is False else None

    def __init__(self):
        self.run()
        archive_name = "[infected]{}_Hybird".format(self.date.strftime("%Y-%m-%d"))
        move2smartccl(self.file_dir, archive_name)

    def run(self):
        session = self.login()
        sha256_list = self.feed(session) + self.latest(session)

        print(sha256_list)

    @staticmethod
    @log
    def login():
        session = HTMLSession()
        url = "https://www.hybrid-analysis.com/login"
        data = {"login[email]": "cicely@iobit.com",
                "login[password]": "IObit>20191213"}
        response = session.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        token = soup.select("input#login__token")[0].get("value")
        data.setdefault("login[_token]", token)
        result = session.post(url, data=data)
        return session if "Logout" in result.text else "login failed."

    @staticmethod
    @log
    def feed(session):
        # get download dict
        url = "https://www.hybrid-analysis.com/feed?json"
        json = session.get(url).json()
        sha256_list = [detail["sha256"] for detail in json["data"]]
        return sha256_list

    @staticmethod
    @log
    def latest(session):
        url = "https://www.hybrid-analysis.com/submissions/sandbox/files"
        params = {"sort": "timestamp",
                  "sort_order": "desc",
                  "page": 1}
        selector = "a.analysis-overview-link.convert-link"

        @log
        def parser_page(page_num):
            params.update({"page": page_num})
            response = session.get(url, params=params).text
            soup = BeautifulSoup(response, "lxml").select(selector)
            return [detail.get("href").split("/")[-1] for detail in soup]

        link_list = [sah256 for page in range(1, 11) for sah256 in parser_page(page)]
        return link_list

    @staticmethod
    def parser_sah256(sha256):
        file_name = "{}.bin.gz".format(sha256)
        url = "https://www.hybrid-analysis.com/download-sample/{}".format(sha256)


if __name__ == "__main__":
    Hybird()
