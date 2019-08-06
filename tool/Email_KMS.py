import hashlib
import os
import re


def get_kms():
    aa = input("\nkms\n")
    for line in aa.split("\n"):
        result = re.findall(".*\\,.*\\,.*\\, (.*)", line)[0]
        print(f"\r{result}", "ss",  end="")
        with open(r"C:\Users\hewen\Desktop\aa.txt", "a+")as file:
            file.write(result + "\n")


while True:
    get_kms()
# with open(r"C:\Users\hewen\Desktop\new.txt", "r")as file:
#     lines = file.readlines()
# for line in lines:
#     line = line.strip("\n")
#     print(line)
# for i in range(ord("0"), ord("9")+1):
#     print(chr(i))
# c = [chr(i) for i in range(ord("0"), ord("9")+1)]
# c += (chr(j) for j in range(ord("a"), ord("z")+1))
# print(c)
# import poplib
#
# mail_address = "1580233773@qq.com"
# mail_password = "heyang"
# mail_host = "pop.qq.com"
# mail_port = 995
# my_mail = poplib.POP3_SSL(host=mail_host, port=mail_port)
# my_mail.user(user=mail_address)
# my_mail.pass_(pswd=mail_password)
# print(my_mail.stat())

# mm = hashlib.sha256()
# mm.update("isu2_2019".encode("utf-8"))
# mm.update("aa".encode("utf-8"))
# print(mm.hexdigest())