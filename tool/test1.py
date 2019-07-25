import json
import requests
from bs4 import BeautifulSoup
from contextlib import closing


class Fang:

    def __init__(self):
        self.session = self.get_session()

    @staticmethod
    def get_session():
        session = requests.session()
        agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
        session.headers.update({"User-Agent": agent})
        return session

    def get_page(self):
        for page in range(1, 35):
            init_url = f"http://www.fangfangfang.com/newhouse/{page}.html"
            with closing(self.session.get(init_url))as response:
                suop = BeautifulSoup(response.content, "lxml").select("li.title > a")
                for i in suop:
                    base_url = i.get("href")[:-9]
                    # self.get_view(base_url)
                    # self.get_detail(base_url)
                    self.get_photos(base_url)
                    # self.get_planintro(base_url)
                    # break
            break

    def get_view(self, url):
        url = url + "view.html"
        try:
            with closing(self.session.get(url))as response:
                suop = BeautifulSoup(response.content, "lxml").select("body > div:nth-child(6) > div")[0]
                fang_pic = suop.select("div [class=\"img\"]")[0].img.get("src").strip(" ")
                fang_name = suop.select("div [class=\"title\"]")[0].getText().strip(" ")
                fang_price = suop.select("div [class=\"num\"]")[0].getText().strip(" ")
                fang_type = suop.select("span[class=\"info\"]")[0].getText().strip(" ")
                fang_address = suop.select("span[class=\"info\"]")[1].getText().strip(" ")
                fang_new = suop.select("span[class=\"info\"]")[2].getText().strip(" ")
                fang_tel = suop.select("p[class=\"max\"]")[0].getText().strip(" ")
                print(fang_pic, fang_name, fang_price, fang_type, fang_address, fang_new, fang_tel)
        except requests.exceptions as e:
            print(e)

    def get_detail(self, url):
        url = url + "detail.html"
        try:
            with closing(self.session.get(url))as response:
                suop = BeautifulSoup(response.content, "html.parser").select("div.fl.new_list_l.new_detail_info_box.mb20")[0]
                for title in suop.select("div[class=\"center new_info_item\"]"):
                    info_title = title.select("p[class=\"item\"]")
                    for base in info_title:
                        info_base = base.select("span")
                        for info_detail in info_base:
                            print(info_detail.getText())
        except requests.exceptions as e:
            print(e)

    def get_news(self, url):
        url = url + "news.html"
        try:
            with closing(self.session.get(url))as response:
                suop = BeautifulSoup(response.content, "lxml").select("#con_one_1")
                for page in suop:
                    print(page.a.get("href"))
        except requests.exceptions as e:
            print(e)

    def get_prices(self, url):
        url = url + "prices.html"
        try:
            with closing(self.session.get(url))as response:
                suop = BeautifulSoup(response.content, "html.parser").select("#price_more")[0]
                for i in suop.select("td"):
                    print(i.getText())

        except requests.exceptions as e:
            print(e)

    def get_photos(self, url, num=1):
        init_url = url
        cid = url.split("/")[-2]
        new_url = f"http://www.fangfangfang.com/index.php?/ajax/pageload/aj_model/a%2C7/aj_check/1/aj_pagenum/{num}/aj_pagesize/18/aj_nodemode/0/aj_thumb/thumb%2C184%2C134/aj_whrfields/pid3%2C%3D%2C{cid}%3Bcaid%2C%3D%2C0/callback/?/domain/www.fangfangfang.com"
        try:
            with closing(self.session.get(new_url))as response:
                suop = response.content
                for i in json.loads(suop):
                    print(i["thumbOrg"])
                if len(json.loads(suop)) == 18:
                    num += 1
                    self.get_photos(init_url, num=num)
        except requests.exceptions as e:
            print(e)

    def get_planintro(self, url):
        cid = url.split("/")[-2]
        new_url = f"http://www.fangfangfang.com/index.php?/ajax/pageload/aj_model/a%2C11/aj_check/1/aj_pagenum/1/aj_pagesize/18/aj_deforder/status+asc%2Caid+asc/aj_nodemode/0/caid/11/aj_thumb/thumb%2C184%2C134/aj_whrfields/pid3%2C%3D%2C{cid}%3Bshi%2C%3D%2C0/callback/?/domain/www.fangfangfang.com"
        try:
            with closing(self.session.get(new_url))as response:
                suop = response.content
                for i in json.loads(suop):
                    print(i["thumbOrg"])
        except requests.exceptions as e:
            print(e)


if __name__ == "__main__":
    Fang().get_page()


