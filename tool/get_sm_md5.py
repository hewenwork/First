import requests


url = "http://192.168.1.19/imfsmart/interface/it_md5mgr.php"
params = {
    "action": "getmd5s",
    "cpage": 0,
    "pagemaxitems": 15
}
response = requests.get(url, params=params)
print(response.text)