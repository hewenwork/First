import re
import telnetlib

import requests_html


def check_proxies(proxies):
    for proxies_type, details in proxies.items():
        try:
            host, port = details.split(":")
            telnetlib.Telnet(host, port, timeout=5)
            print(host, port)
        except Exception as e:
            print(e)
proxies = {"https": "185.83.186.6:58006", "http": "52.59.231.58:80"}
check_proxies(proxies)
session = requests_html.HTMLSession()
# proxies = {"http": "157.245.136.101:8080", "https": "72.35.40.34:8080"}
url = f"http://www.virusign.com/get_hashlist.php"
params = {
    "sha256": "",
    "start_date": "2019-01-02",
    "end_date": "2019-01-02"
}
try:
    response = session.get(url, params=params, proxies=proxies, verify=False)
    print(response.url)
    # aa = {
    #     sha256 + ".7z": f"http://virusign.com/file/{sha256}.7z"
    #     for sha256 in re.findall(r"\"(\w{64})\"", response)
    # }
    # print(aa)
except Exception as e:
    print(e)
