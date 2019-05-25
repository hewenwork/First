import os
import re


def get_kms():
    aa = input("kms")
    for line in aa.split("\n"):
        result = re.findall(".*\\,.*\\,.*\\,(.*)", line)[0]
        print(result)
        with open(r"C:\Users\hewen\Desktop\aa.txt", "a+")as file:
            file.write(result + "\n")

while True:
    get_kms()