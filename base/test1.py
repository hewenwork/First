import os

import requests

a = requests.get("https://raw.githubusercontent.com/hewenwork/First/master/icon/hw.ico").content
with open(r"C:\Users\hewen\Desktop\hw.ico", "wb")as file:
    file.write(a)