# encoding = utf-8
# @Author: Hewen
# @Time:  10:30
import re


class Demo:

    def __init__(self):
        dd = {}
        f = r"C:\Users\hewen\Desktop\SigN总.db"
        with open(f, "r", encoding="utf-8")as file:
            ll = file.readlines()
            for i in ll:

                dd[i] = ""
        print(len(dd))
        with open(r"C:\Users\hewen\Desktop\S.db", "w", encoding="utf-8")as ff:

            for j in dd.keys():
                if re.match(r"^\w*,\d*,.*,\d*,.*$", j)is False:
                    print(j)
                ff.write(j)

        print(len(ll))


if __name__ == "__main__":
    Demo()
