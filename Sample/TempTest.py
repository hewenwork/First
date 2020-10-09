from enum import Enum
from bs4 import BeautifulSoup
from re import match, findall
from subprocess import check_output
from urllib3 import disable_warnings
from requests_html import HTMLSession
from os import makedirs, path, listdir
from datetime import datetime, timedelta
from urllib.parse import urlparse, unquote



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
    chunk_size = 1024 * 1024
    response = session.get(url, **option)
    headers = response.headers
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=chunk_size):
            file.write(chunk)
    return True


class CMD:

    @classmethod
    def delete(cls, file_path):
        command = f"RD /S /Q \"{file_path}\"" if path.isdir(file_path) else f"DEl /Q \"{file_path}\""
        try:
            check_output(command, shell=True)
            return True
        except Exception as e:
            return e

    @classmethod
    def copy(cls, file_path, dist_path):
        makedirs(dist_path) if path.exists(dist_path) is False else None
        command = f"copy \"{file_path}\" \"{dist_path}\""
        try:
            check_output(command, shell=True)
            return True
        except Exception as e:
            return e

    @classmethod
    def move(cls, file_path, dist_path):
        makedirs(dist_path) if path.exists(dist_path) is False else None
        command = f"move \"{file_path}\" \"{dist_path}\""
        try:
            check_output(command, shell=True)
            return True
        except Exception as e:
            return e

    @classmethod
    def archive(cls, file_path, **kwargs):
        file_dir = path.dirname(file_path)
        password = kwargs.setdefault("password", "infected")
        archive_name = kwargs.setdefault("archive_name", path.basename(file_path).split(".")[0])
        archive_path = kwargs.setdefault("archive_path", path.join(file_dir, archive_name))
        if path.isdir(file_path):
            command = f"7z a \"{archive_path}\" \"{file_path}\\*\" -p{password} -y"
        else:
            command = f"7z a \"{archive_path}\" \"{file_path}\" -p{password} -y"
        try:
            check_output(command, shell=True)
            return True
        except Exception as e:
            return e

    @classmethod
    def extract(cls, file_path, **kwargs):
        password = kwargs.setdefault("password", "infected")
        dist_path = kwargs.setdefault("dist_path", path.dirname(file_path))
        makedirs(dist_path) if path.isdir(dist_path) and path.exists(dist_path) is False else None
        command = "7z e \"{}\" -o\"{}\" -p{} -y -r".format(file_path, dist_path, password)
        try:
            check_output(command, shell=True)
            return True
        except Exception as e:
            return e


class Lanzou:

    @log
    def get_url(self, url):
        session = self.get_session(url)
        parameters = self.get_parameters(session, url)
        sign = self.get_sign(session, url, parameters)
        link = self.get_ajaxm(session, sign)
        direct_link = self.get_direct_link(link)
        return direct_link

    @staticmethod
    def get_session(url: str):
        session = HTMLSession()
        session.headers["Host"] = urlparse(url).netloc
        return session

    @staticmethod
    def get_parameters(session, url):
        response = session.get(url)
        text = response.content.decode()
        soup = BeautifulSoup(text, "lxml").select("body > div.d > div.d2 > div.ifr > iframe")
        parameters = soup[0].get("src")
        return parameters

    @staticmethod
    def get_sign(session, url, parameters: str):
        url = "https://{}{}".format(urlparse(url).netloc, parameters)
        response = session.get(url)
        re = "pdownload = \'(.*?)\';//var"
        sign = findall(re, response.text)[0]
        session.headers["Referer"] = url
        return sign

    @staticmethod
    def get_ajaxm(session, sign: str):
        session.headers["Origin"] = "https://{}".format(session.headers["Host"])
        url = "{}/ajaxm.php".format(session.headers["Origin"])
        data = {"action": "downprocess", "sign": sign, "ves": "1"}
        response = session.post(url, data=data)
        json = response.json()
        link = "{}/file/{}".format(json["dom"], json["url"])
        return link

    @staticmethod
    def get_direct_link(link):
        session = HTMLSession()
        session.headers["Accept-language"] = "zh-CN"
        response = session.head(link)
        url = response.headers["Location"]
        session.close()
        return url


@log
def login(self):
    session = HTMLSession()
    url = "https://bbs.kafan.cn/member.php"
    params = {
        "mod": "logging",
        "action": "login",
        "loginsubmit": "yes",
        "handlekey": "login",
        "loginhash": "LVmod",
        "inajax": "1"
    }
    data = {
        "formhash": self.get_formhash(session),
        "referer": "https://bbs.kafan.cn/",
        "username": "1569010448@qq.com",
        "password": "e7008529ce2df26ccc4a060e28e66dd3",
        "questionid": "0"
    }
    response = session.post(url, params=params, data=data)
    assert "欢迎您回来" in response.text, "Login failed."
    formhash = data.setdefault("formhash")
    sign_url = f"https://bbs.kafan.cn/plugin.php?id=dsu_amupper&ppersubmit=true&formhash={formhash}"
    session.get(sign_url)
    return session


def get_formhash(session):
    url = "https://bbs.kafan.cn/member.php"
    params = {
        "mod": "logging",
        "action": "login",
        "infloat": "yes",
        "handlekey": "login",
        "inajax": "1",
        "ajaxtarget": "fwin_content_login"
    }
    formhash_text = session.get(url, params=params).text
    formhash = findall(r"name=\"formhash\" value=\"(.*)\" />", formhash_text)[0]
    return formhash


class Kafan:

    def get_sample_link_list(self, session, download_date):
        assert isinstance(session, HTMLSession), "login failed"
        sample_list = [self.parser_page(session, page_link) for page_link in self.get_page_list(session, download_date)]
        sample_link_list = [link for link_list in sample_list if link_list for link in link_list]
        return sample_link_list

    def get_page_list(self, session, download_date):
        url = "https://bbs.kafan.cn/forum.php"
        params = {"mod": "forumdisplay", "fid": "31", "filter": "author", "orderby": "dateline"}
        response = session.get(url, params=params).text
        soup = BeautifulSoup(response, "lxml").select("tr")[7:]
        download_date = download_date.date()
        page_link_list = []
        for element in soup:
            element_date_soup = element.select("td[class=by] > em > span > span")
            element_date = datetime.strptime(element_date_soup[0].get("title"), "%Y-%m-%d").date()
            if element_date > download_date:
                continue
            elif element_date == download_date:
                page_link_list.append(element.select("th > a")[0].get("href"))
            elif element_date < download_date:
                break
        return page_link_list

    def parser_page(self, session, page_link: str):
        response = session.get(page_link).text
        soup = BeautifulSoup(response, "lxml").select("div[class=pct]")
        if not len(soup):
            return None
        link_list = self.parse_page_text(soup[0])
        return link_list

    @staticmethod
    def parse_page_text(soup):
        content = soup.getText()
        re_lanzou = r"https://\w*?.lanzou.\.com/[a-zA-Z0-9]*"
        lanzou_list = findall(re_lanzou, content)
        lanzou_list = [Lanzou().get_url(i) for i in lanzou_list if i]
        if len(lanzou_list) != 0:
            return lanzou_list
        re_other = r"(.*\.)zip|(.*\.)7z|(.*\.)exe|(.*\.)rar"
        url_list = [i.get("href") if match(re_other, i.getText()) is not None else None for i in soup.select("a")]
        link_list = [link for link in url_list if link]
        return link_list


def final():
    sm_dir = r"G:\Auto"
    sample_dir = r"G:\AutoSample\Kafan"
    temp_dir = r"G:\AutoSample\Kafan\Temp"
    session = login()
    download_date = datetime.today() - timedelta(days=1)
    makedirs(temp_dir) if path.exists(temp_dir) is False else None
    archive_name = "[infected]{}_Kafan.zip".format(download_date.strftime("%Y%m%d"))
    archive_path = path.join(sample_dir, archive_name)
    sample_list = Kafan().get_page_list(session, download_date)
    for url in sample_list:
        download(url, session=session, file_dir=temp_dir)
    for file_name in listdir(temp_dir):
        file_path = path.join(temp_dir, file_name)
        CMD.extract(file_path)
        CMD.delete(file_path)
    file_path_list = [path.join(temp_dir, file_name) for file_name in listdir(temp_dir)]
    for file_path in file_path_list:
        CMD.delete(file_path) if path.isdir(file_path) else None
    CMD.archive(temp_dir, archive_path=archive_path)
    CMD.copy(archive_path, sm_dir)
    CMD.delete(temp_dir)


class Login:

    @log
    def __call__(self):
        session = HTMLSession()
        url = "https://bbs.kafan.cn/member.php"
        params = {
            "mod": "logging",
            "action": "login",
            "loginsubmit": "yes",
            "handlekey": "login",
            "loginhash": "LVmod",
            "inajax": "1"
        }
        data = {
            "formhash": self.get_formhash(session),
            "referer": "https://bbs.kafan.cn/",
            "username": "1569010448@qq.com",
            "password": "e7008529ce2df26ccc4a060e28e66dd3",
            "questionid": "0"
        }
        response = session.post(url, params=params, data=data)
        assert "欢迎您回来" in response.text, "Login failed."
        formhash = data.setdefault("formhash")
        sign_url = f"https://bbs.kafan.cn/plugin.php?id=dsu_amupper&ppersubmit=true&formhash={formhash}"
        session.get(sign_url)
        return session

    @staticmethod
    def get_formhash(session):
        url = "https://bbs.kafan.cn/member.php"
        params = {
            "mod": "logging",
            "action": "login",
            "infloat": "yes",
            "handlekey": "login",
            "inajax": "1",
            "ajaxtarget": "fwin_content_login"
        }
        formhash_text = session.get(url, params=params).text
        formhash = findall(r"name=\"formhash\" value=\"(.*)\" />", formhash_text)[0]
        return formhash


class Info(Enum):
    DATE = datetime.today() - timedelta(days=1)
    SM_DIR = r"G:\Auto"
    SAMPLE_DIR = r"G:\AutoSample\Kafan"
    TEMP_DIR = r"G:\AutoSample\Kafan\Temp"
    ARCHIVE_NAME = "[infected]{}_Kafan.zip".format(DATE.strftime("%Y%m%d"))

    class Kafan:

        def __init__(self):
            self.session = Info.Login()
            self.date = Info.DATE.value

        def __call__(self):
            assert isinstance(self.session, HTMLSession), "login failed"
            sample_list = [self.parser_page(page_link) for page_link in self.get_page_list()]
            sample_link_list = [link for link_list in sample_list if link_list for link in link_list]
            return sample_link_list

        def get_page_list(self):
            url = "https://bbs.kafan.cn/forum.php"
            params = {"mod": "forumdisplay", "fid": "31", "filter": "author", "orderby": "dateline"}
            response = self.session.get(url, params=params).text
            soup = BeautifulSoup(response, "lxml").select("tr")[7:]
            download_date = self.date.date()
            page_link_list = []
            for element in soup:
                element_date_soup = element.select("td[class=by] > em > span > span")
                element_date = datetime.strptime(element_date_soup[0].get("title"), "%Y-%m-%d").date()
                if element_date > download_date:
                    continue
                elif element_date == download_date:
                    page_link_list.append(element.select("th > a")[0].get("href"))
                elif element_date < download_date:
                    break
            return page_link_list

        def parser_page(self, page_link):
            response = self.session.get(page_link).text
            soup = BeautifulSoup(response, "lxml").select("div[class=pct]")
            if not len(soup):
                return None
            link_list = self.parse_page_text(soup[0])
            return link_list

        @staticmethod
        def parse_page_text(soup):
            content = soup.getText()
            re_lanzou = r"https://\w*?.lanzou.\.com/[a-zA-Z0-9]*"
            lanzou_list = findall(re_lanzou, content)
            lanzou_list = [Lanzou().get_url(i) for i in lanzou_list if i]
            if len(lanzou_list) != 0:
                return lanzou_list
            re_other = r"(.*\.)zip|(.*\.)7z|(.*\.)exe|(.*\.)rar"
            url_list = [i.get("href") if match(re_other, i.getText()) is not None else None for i in soup.select("a")]
            link_list = [link for link in url_list if link]
            return link_list

    def __call__(self, *args):
        return self.value(*args)() if callable(self.value(*args)) else self.value(*args)


if __name__ == "__main__":
    pass
