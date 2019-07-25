# encoding = utf-8
import time
import sys
import os


def run_path(file_path):
    file_name = os.path.split(file_path)[-1]
    if getattr(sys, 'frozen', False):
        # we are running in a bundle
        frozen = 'ever so'
        bundle_dir = sys._MEIPASS
    else:
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(bundle_dir, file_name)


f = r"C:\Users\hewen\Desktop\Error.log"
with open(run_path(f), "r+", encoding="utf-8")as file:
    aa = file.read()
    print(aa)
print(os.path.dirname(os.path.abspath(__file__)))
input("aa")

