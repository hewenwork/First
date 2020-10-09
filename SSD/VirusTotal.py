# -*- coding: UTF-8 -*-
"""
@author: Hewen
@file:VirusTotal.py
@time:2020/09/09
"""
from random import choice
from contextlib import closing
from pickle import dump, load
from requests_html import HTMLSession

api_list = ["d8ac8c77f6c3b297750c0ba92484f06a8037075049ff79101b921d6d36104559",
            "a7450f5a40fccd2d761d83593ce8f918960b49de12b6ec172759ab485591fa71",
            "5926cc5a2d8ff785ba7973228aa5053183d61111d02c9a0a6a98ea76c05f8ac7",
            "de25ed07259c081b8bd873a8248022c6c138419f95339cea8eecf02313d7f6e0",
            "ee07787779550e5031d061220fd30eb504ac7bceac820736005c878acba5f15b",
            "2243746e5f13d38e8907355aa543b9eeb53a9a5df02c07f976ee03fc4f086781",
            "a5efd48f0b928a7a77ba0c20e803991d3ebe50add87a97e7a680cd802e64bc88",
            "6c78677baf1f91105bd165578eb4ed36b702ee52b5aba06a9c22d54c52d98d8d",
            "b9b4d1cf70ad6c849df565e9b4fc11dbc508d915332a42a9cbca175c76097b7c",
            "626f13733c1ab37b459fe2b362a9d9c037822be429c3a8b59ec89a6631b2a55b",
            "5dc4d2be4a434cd2b7abc651cb3e9a09ec311770cd8474310ab0d91445d466ec",
            "27ef571e4443ffc42395e69a939106a7f8740951c83aecb14d63959ea779b7ea",
            "d09dca26deddad1aadeb767f2762b80c6e0570596b5671a0e32c70afa4a853c9",
            "809886425d3c5e955849890d3ac2c235f63cebd57aff0454fd5d5fe98160c559",
            "6d3305d504ccd66c95fb23de209aabbef50793746e9bed97cb46a5ad3be3d1a9",
            "392ff7ebbfee647c2141e7b4ac4c9ee3d7242608a4ff8b56ba943daf2b40c4a6",
            "0106dfd35f87f68df9cd3a6fb5decd71de0f6dba6c954fc4d7003ed152b4279d",
            "78c0d9b5d93eec1a6118d0c27c05d2cf43ca1b1d8f85a5b64491134781b8a5c0",
            "33a9068c3937d8e17846767c8c344ff4f932140704362e2546d2c4dc5d85e436",
            "a5424fa7a0b9a81d2b11845dba0a694da2a9763e06fb9392e6d2af59469a1fd8",
            "40dde2e5940bccd39ec8a3af05c2ce46cc4aa7ad4f2599d9eab832b6fbfd5661",
            "d5a63233aa9309c2d53f15bf945e01ffccaea56727f87ed2e2779e686b3aa758",
            "ca8073c043cc387b585657e17f8c8ea9fa3dcec37679403aec98b76a77e439ae",
            "9d75fb43e225104caaf9ff567b13969850ee132dc0842158cec82cd397dca5f5",
            "c6225b29a41a9084271387b16130332efb838003fdcd6b6bb1001c1e07dbc230"]


def get_report(file_hash):
    api_key = choice(api_list)
    print(api_key)
    session = HTMLSession()
    url = "https://www.virustotal.com/vtapi/v2/file/report"
    params = {"apikey": api_key, "resource": file_hash}
    try:
        response = session.get(url, params=params)
        if response.status_code != 200:
            return False
        json = dict(response.json())
        return json
    except Exception as e:

        return e
    finally:
        session.close()


def get_positive(file_hash):
    positives = get_report(file_hash)
    print(positives)
    return positives.setdefault("positives") if isinstance(positives, dict) else False


def post_file(file_path):
    api_key = choice(api_list)
    print(api_key)
    session = HTMLSession()
    session.headers["x-apikey"] = api_key
    url = "https://www.virustotal.com/api/v3/files"
    files = {"file": open(file_path, "rb").read()}
    result = session.post(url, files=files)
    print(result.json())
    uu = "https://www.virustotal.com/api/v3/analyses/N2I0MmI1NGNmN2ZlZjM4OGE0ZmJiNWJkNDY0OTlhYzA6MTU5OTcwNjQyMw=="
    print(session.get(uu).content)


def check_api_key(api_key):
    session = HTMLSession()
    url = "https://www.virustotal.com/vtapi/v2/file/report"
    params = {"apikey": api_key, "resource": "38de5b216c33833af710e88f7f64fc98"}
    try:
        response = session.get(url, params=params)
        if response.status_code == 200:
            print(f"\"{api_key}\",")
    except Exception as e:
        return e
    finally:
        session.close()


if __name__ == "__main__":
    # print(get_positive("38de5b216c33833af710e88f7f64fc98"))
    # d = r"C:\Users\hewen\Desktop\sq.db"
    # post_file(d)
    # with open(r"C:\Users\hewen\Desktop\sq.db", "rb")as a:
    #     c =load(a)
    #     print(c)
    for i in api_list:
        check_api_key(i)
