import requests
from bs4 import BeautifulSoup


class GetApp:

    def get_page(self, page):
        # "http://www.dayanzai.me/windows-soft/network/page/2"
        base_url = "http://www.dayanzai.me/windows-soft/system/page/%s" % page
        session = requests.session()
        session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"})
        response = session.get(base_url)
        suop_title = BeautifulSoup(response.text, "lxml").select("ul > li > div > div > p.r-top > span > a")
        suop_detail = BeautifulSoup(response.text, "lxml").select("ul > li > div > div > p.desc")
        with open(r"C:\Users\hewen\Desktop\system.txt", "a+", encoding="utf-8")as file:
            for title, detail in zip(suop_title, suop_detail):
                title_url = title.get("href")
                title_name = title.getText()
                title_detail = detail.getText()
                one = title_url + "   " + title_name + "\n" + title_detail + "\n"
                print(one)
                file.write(one)


if __name__ == "__main__":
    for i in range(0, 16):
        GetApp().get_page(i)
