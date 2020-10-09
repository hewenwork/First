from sys import argv
from time import time
from urllib import parse
from base64 import b64decode
from re import match, findall
from inspect import signature
from bs4 import BeautifulSoup
from contextlib import closing
from os import makedirs, path, remove
from requests_html import HTMLSession
from datetime import datetime, timedelta


def decode_url(url: str):
    return parse.unquote(url)


def decode_base_64(url: str):
    return b64decode(url)


# @log_action
def download(kwargs: dict):
    session = HTMLSession()
    url = kwargs.setdefault("url")
    attrs = [
        'headers', 'cookies', 'auth', 'proxies', 'hooks', 'params', 'verify',
        'cert', 'prefetch', 'adapters', 'stream', 'trust_env',
        'max_redirects',
    ]
    option = {key: value for key, value in kwargs.items() if key in attrs}
    option.setdefault("stream", "True")
    if kwargs is None or isinstance(kwargs, dict) is False:
        return "参数错误"
    if url is None:
        return "Url is None"
    re_url = r"http.*://.*"
    if match(re_url, url) is None:
        return "Url {} is not match: {}".format(url, re_url)
    while True:
        head = session.head(url, **option)
        status_code = head.status_code
        if head.status_code in [301, 302]:
            url = head.headers.setdefault("Location")
        elif head.status_code == 200:
            break
        else:
            return "Url: {}, status code: {}".format(url, status_code)

    file_path = kwargs.setdefault("file_path")
    if file_path is None:
        file_dir = kwargs.setdefault("file_dir", path.dirname(argv[0]))
        makedirs(file_dir) if path.exists(file_dir) is False else None
        file_name = kwargs.setdefault("file_name")
        if file_name is None:
            url_name_list = findall(r"^http.*//.*/(.*\..{1,5})$", url)
            file_name = url_name_list[0] if len(url_name_list) != 0 else None
            if file_name is None:
                headers = head.headers
                response_name = headers.setdefault("Content-Disposition")
                if response_name is not None:
                    file_name = response_name.split("filename=")[-1].strip("\"")
                    file_name = decode_url(file_name)
                else:
                    file_name = str(time()) + ".tmp"
        file_path = path.join(file_dir, file_name)
    try:
        chunk_size = 1024 * 1024
        file = open(file_path, "wb")
        for chunk in session.get(**option, timeout=30).iter_content(chunk_size):
            file.write(chunk)
        file.close()
    except Exception as e:
        remove(file_path) if path.exists(file_path) else None
        return "download Exception: {}".format(e)
    return True


def st(**kwargs):
    option = kwargs.setdefault("option")
    session = kwargs.setdefault("session")
    file_size = kwargs.setdefault("file_size")
    total_sie = kwargs.setdefault("total_sie")
    file_path = kwargs.setdefault("file_path")
    file_mode = kwargs.setdefault("file_mode")
    session.headers["range"] = "bytes={}-{}".format(file_size, total_sie)
    try:
        file = open(file_path, file_mode)
        chunk_size = 1024 * 1024
        with closing(session.get(**option, timeout=30))as response:
            for chunk in response.iter_content(chunk_size):
                file.write(chunk)
        file.close()
    except Exception as e:
        remove(file_path) if path.exists(file_path) else None
        return "download Exception: {}".format(e)
    return True


# @log_action
def parser_lanzou_link(url: str) -> str:
    with closing(HTMLSession())as session:
        session.headers["referer"] = url
        session.headers["accept-language"] = "zh-CN"
        try:
            response_fn = session.get(url)
            soup_fn = BeautifulSoup(response_fn.text, "lxml").select("iframe[class=ifr2]")
            src = soup_fn[0].get("src")
            sign_url = "https://jirehlov.lanzous.com{}".format(src)
            sign_re = r"downprocess\',\'sign\':\'(.*)\',\'ves"
        except Exception as e:
            return "lanzou link parser error1:{}\n{}".format(e, url)
        try:
            sign_response = session.get(sign_url)
            sign = findall(sign_re, sign_response.text)[0]
            url_file = "https://jirehlov.lanzous.com/ajaxm.php"
            data = {
                "action": "downprocess",
                "sign": sign,
                "ves": "1"
            }
            response = session.post(url_file, data=data).json()
            url_parser = "{}/file/{}".format(response["dom"], response["url"])
            url_sample = session.head(url_parser).headers["Location"]
            return url_sample
        except Exception as e:
            return "lanzou link parser error2:{}\nurl:{}".format(e, url)


base_dir = r"G:\AutoSample\Kafan"
download_date = datetime.today() - timedelta(days=1)


class Kafan:

    @staticmethod
    def login():
        session = HTMLSession()
        url = "https://bbs.kafan.cn/member.php"
        params_formhash = {
            "mod": "logging",
            "action": "login",
            "infloat": "yes",
            "handlekey": "login",
            "inajax": "1",
            "ajaxtarget": "fwin_content_login"
        }
        try:
            response_formhash = session.get(url, params=params_formhash).text
            re_formhash = r"name=\"formhash\" value=\"(.*)\" />"
            formhash = findall(re_formhash, response_formhash)[0]
            params_login = {
                "mod": "logging",
                "action": "login",
                "loginsubmit": "yes",
                "handlekey": "login",
                "loginhash": "LVmod",
                "inajax": "1"
            }
            data = {
                "formhash": formhash,
                "referer": "https://bbs.kafan.cn/",
                "username": "1569010448@qq.com",
                "password": "e7008529ce2df26ccc4a060e28e66dd3",
                "questionid": "0"
            }
            login_result = session.post(url, params=params_login, data=data).text
            return session if "欢迎您回来" in login_result else "Login Failed"
        except Exception as e:
            return "Login Kafan Error: {}".format(e)

    def __init__(self):
        session = self.login()
        if isinstance(session, HTMLSession) is False:
            raise RuntimeError(session)
        print("Login Success")
        page_list = self.get_page_list(session)
        if isinstance(page_list, list) is False:
            raise RuntimeError( "get page list Failed: {}".format(page_list))
        for page_link in page_list:
            sample_list = self.parser_page(session, page_link)
            for sample in sample_list:
                download(sample)

    @staticmethod
    def get_page_list(session: HTMLSession):
        url = "https://bbs.kafan.cn/forum.php"
        params = {
            "mod": "forumdisplay",
            "fid": "31",
            "filter": "author",
            "orderby": "dateline"
        }
        try:
            response = session.get(url, params=params).text
            soup = BeautifulSoup(response, "lxml").select("tr")
            page_link_list = []
            for element in soup[7:-2]:
                element_date_soup = element.select("td > em > span > span")
                if len(element_date_soup) == 0:
                    continue
                element_date = datetime.strptime(element_date_soup[0].get("title"), "%Y-%m-%d").date()
                page_link = element.select("th > a")[0].get("href")
                page_link_list.append(page_link) if element_date == download_date.date() else None
            return page_link_list
        except Exception as e:
            return "get all page list Error:{}".format(e)

    @staticmethod
    def parser_page(session: HTMLSession, page_link: str):
        response = session.get(page_link).text
        soup = BeautifulSoup(response, "lxml").select("div[class=pct]")[0]
        content = soup.getText()
        re_lanzou = r"https://\w*?.lanzou.\.com/[a-zA-Z0-9]*"
        lanzou_list = findall(re_lanzou, content)
        file_dir = path.join(base_dir, str(download_date.month))
        lanzou_list = [{"url": parser_lanzou_link(i), "file_dir": file_dir} for i in lanzou_list]
        if len(lanzou_list) != 0:
            return lanzou_list
        re_other = r"(.*\.)zip|(.*\.)7z|(.*\.)exe|(.*\.)rar"
        url_list = [i.get("href") if match(re_other, i.getText()) is not None else None for i in soup.select("a")]
        link_list = [{"url": link, "file_dir": file_dir, "cookie": session.cookies} for link in url_list]
        return link_list


if __name__ == "__main__":
    Kafan()
