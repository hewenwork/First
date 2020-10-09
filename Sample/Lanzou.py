from re import findall
from urllib.parse import urlparse
from requests_html import HTMLSession


def test(url: str):
    session = HTMLSession()
    response = session.get(url)
    re = r"ifr2\" name=\"\d*?\" src=\"(.*?)\" frameborder"
    parameters = findall(re, response.text)[1]
    # session.headers["Accept-language"] = "zh-CN"
    # session.headers["Host"] = urlparse(url).netloc
    # session.headers["Referer"] = url
    # session.headers["Origin"] = "https://{}".format(session.headers["Host"])
    url = "https://{}{}".format(urlparse(url).netloc, parameters)
    response = session.get(url)
    re = "var ajaxdata = '(.*)';"
    sign = findall(re, response.text)[0]
    url = "https://{}/ajaxm.php".format(urlparse(url).netloc)
    data = {"action": "downprocess", "sign": sign, "ves": "1"}
    response = session.post(url, data=data)
    json = response.json()
    link = "{}/file/{}".format(json["dom"], json["url"])

    print(link)
    print(session.headers)
    response = session.get(link)
    return response.status_code


class Lanzou:

    def __init__(self, url):
        session = self.get_session(url)
        parameters = self.get_parameters(session, url)
        sign = self.get_sign(session, url, parameters)
        link = self.get_ajaxm(session, sign)
        direct_link = self.get_direct_link(link)
        self.url = direct_link

    @staticmethod
    def get_session(url: str):
        session = HTMLSession()
        session.headers["Host"] = urlparse(url).netloc
        return session

    @staticmethod
    def get_parameters(session, url):
        response = session.get(url)
        re = r"ifr2\" name=\"\d*?\" src=\"(.*?)\" frameborder"
        parameters = findall(re, response.text)[1]
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
        return response.headers["Location"]


if __name__ == "__main__":
    a = "https://www.lanzoux.com/iSvJhh90lre"
    print(test(a))
