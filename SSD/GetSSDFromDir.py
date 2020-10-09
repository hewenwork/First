# -*- coding: UTF-8 -*-
"""
@author: Hewen
@file:GetSSDFromDir.py
@time:2020/09/09
"""
from chardet import detect
from os import path, listdir
from re import match, findall


def get_file_content(file_path: str):
    with open(file_path, "rb")as file:
        encoding = detect(file.read()).setdefault("encoding", "utf-8")
    with open(file_path, "r", encoding=encoding)as file:
        content = file.read()
    return content


def get_re_match_dict(re: str, text: str):
    match_list = findall(re, text)
    match_dict = {line.split(" , ")[0]: line.split(" , ")[-1] for line in match_list}
    return match_dict


def get_file_path_list(file_dir: str):
    file_path_list = [path.join(file_dir, file_name) for file_name in listdir(file_dir)]
    for file_path in file_path_list:
        if path.isdir(file_path):
            file_path_list.remove(file_path)
    return file_path_list


def run():
    file_path_list = get_file_path_list(r"C:\Users\hewen\Desktop\ssd")
    re = r"\d{8} , \w{32}"
    match_dict = {j: k for i in file_path_list for j, k in get_re_match_dict(re, get_file_content(i)).items()}
    md5_dict = {md5: md5 for md5 in match_dict.values()}
    print(len(md5_dict))
    info_list = [f"{j}:{k}" for i in file_path_list for j, k in get_re_match_dict(re, get_file_content(i)).items()]
    info_set = set(info_list)

    with open(r"C:\Users\hewen\Desktop\ssdaaa.db", "w")as file:
        for i in info_set:
            file.write("{}\n".format(i.replace(" ", "")))


if __name__ == "__main__":
    run()
