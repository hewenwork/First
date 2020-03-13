import os
from bs4 import BeautifulSoup


def get_list():
    dir_folder = r"C:\Users\hewen\Desktop\so"
    file_list = []
    for file_name in os.listdir(dir_folder):
        file_path = os.path.join(dir_folder, file_name)
        if os.path.isfile(file_path):
            file_list.append(file_path)
    return file_list


def tt(aaa):
    with open(r"C:\Users\hewen\Desktop\NanoCore.txt", "a+", encoding="utf-8")as file:
        file.write(aaa)
def test1(file_path):
    with open(file_path, "r", encoding="utf-8")as file:
        content = file.read()
    suop = BeautifulSoup(content, "lxml")
    a = suop.select("body > div.submissions > div.history > div.history-table > div.history-table--content-wrap > div > div > a > div.history__hash.noselect > div:nth-child(1) > div.hash__value")
    for i in a:
        result = i.getText().strip("\n")
        tt(result)

for ii in get_list():
    test1(ii)
