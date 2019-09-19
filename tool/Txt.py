# coding = utf-8
import chardet
import requests
from bs4 import BeautifulSoup


class Demo:

    def __init__(self):
        self.session = requests.session()
        url_home = r"https://www.yuanzunxs.cc/go/7755/"
        home_text = self.session.get(url_home).content
        suop = BeautifulSoup(home_text.decode(self.get_encoding(home_text)), "lxml").select("#list-chapterAll")[0]
        with open(r"C:\Users\hewen\Desktop\x.txt", "w", encoding="utf-8")as file:
            for page in suop.select("a"):
                url_page = url_home + page.get("href")
                try:
                    text = self.get_page(url_page)
                    file.write(text)
                except Exception as e:
                    print(e)

    @staticmethod
    def get_encoding(content):
        try:
            encoding = chardet.detect(content)["encoding"]
            return encoding
        except Exception as e:
            print(e)

    def get_page(self, url_page):
        page_content = self.session.get(url_page).content
        selector = "body > div.container > div.content > div.book.read > div.readcontent"
        page_next_select = "#linkNext"
        page_suop = BeautifulSoup(page_content.decode(self.get_encoding(page_content)), "lxml")
        page_text = page_suop.select(selector)[0].getText()[:-18]
        page_next_url = page_suop.select(page_next_select)[0].get("href")
        self.get_page_next(page_next_url, page_text)
        return page_text

    def get_page_next(self, url_page, page_text):
        page_content = self.session.get(url_page).content
        selector = "body > div.container > div.content > div.book.read > div.readcontent"
        page_suop = BeautifulSoup(page_content.decode(self.get_encoding(page_content)), "lxml")
        page_text += page_suop.select(selector)[0].getText()[:-18]
        return page_text


if __name__ == "__main__":
    Demo()
