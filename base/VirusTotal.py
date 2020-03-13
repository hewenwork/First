# encoding = utf-8
# @Author: Hewen
# @Time: 11/6/2019 3:59 PM
# @File: VirusTotal.py
import json
import random

import requests

session = requests.session()
agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 " \
        "Safari/537.36 "
session.headers["User-Agent"] = agent
api_keys = '''bf33b55b49c2b8fe06dca09e114e2226cffcac2d214f8c8cd92a976e7f0fe696
fb007f45821a070fe8c60fbab00e38f43e27d218b63b281eceeebfa24b682b40
ebb69c2b5fc6bd3f67ff36f28c66cd489e025a321fb0f4e40c985c34e97c9b09s
e63fff6ec2f1d351b56e263e6903cf7199ecba26bd01046c69f4f92b3d79d09e
6172001af0588434c0ff9d7d78da7b1556939a252709f663987fa3bcbc7009ce
ae52dc0bf7fb17444515f9911e243d03442ac4bf9448aa44dc6f3cf6f88a1fad
6e58eb435d8eb9e137ce7cb9c63ffce33081e9dababd094c2fcdfc4647139086
010696052677d9f1962e8a1de5cb22e1ddeed5ed854ab6eae6836de2d1a6498e
cdd061806b4cc5264b8fde9cb61c9093d3396a6bafb7b77bda27a208d8cc1804
9bfb9694197e0812e6fc735fc90eb21b4e3e6dd1f058ad452b5b48df4ea70dd9
6fcd7437a39b77c405601a83c02a16d882b7c258a82b24499cd1660cc428df3a
92bb1fdbb853890322be3291b2955135d9479e1307f3fe1af8aba403843e8cc8
286087a0e2c1d52e66126467807d9ec33d0a1ba15148e2280252ad060e50f501
b847e5bc4203cdb8245f5d6c8ab5e8606b31a73ef268f3ab474da288a419b8aa
3f8ef86651609fb3fda4134d6433762efa5bbc30ca1cd1b491c584e410a1d384
d8ac8c77f6c3b297750c0ba92484f06a8037075049ff79101b921d6d36104559
a7450f5a40fccd2d761d83593ce8f918960b49de12b6ec172759ab485591fa71
5926cc5a2d8ff785ba7973228aa5053183d61111d02c9a0a6a98ea76c05f8ac7
de25ed07259c081b8bd873a8248022c6c138419f95339cea8eecf02313d7f6e0
ee07787779550e5031d061220fd30eb504ac7bceac820736005c878acba5f15b
2243746e5f13d38e8907355aa543b9eeb53a9a5df02c07f976ee03fc4f086781
a5efd48f0b928a7a77ba0c20e803991d3ebe50add87a97e7a680cd802e64bc88
6c78677baf1f91105bd165578eb4ed36b702ee52b5aba06a9c22d54c52d98d8d
b9b4d1cf70ad6c849df565e9b4fc11dbc508d915332a42a9cbca175c76097b7c
626f13733c1ab37b459fe2b362a9d9c037822be429c3a8b59ec89a6631b2a55b
5dc4d2be4a434cd2b7abc651cb3e9a09ec311770cd8474310ab0d91445d466ec
27ef571e4443ffc42395e69a939106a7f8740951c83aecb14d63959ea779b7ea
d09dca26deddad1aadeb767f2762b80c6e0570596b5671a0e32c70afa4a853c9
809886425d3c5e955849890d3ac2c235f63cebd57aff0454fd5d5fe98160c559
6d3305d504ccd66c95fb23de209aabbef50793746e9bed97cb46a5ad3be3d1a9
392ff7ebbfee647c2141e7b4ac4c9ee3d7242608a4ff8b56ba943daf2b40c4a6
0106dfd35f87f68df9cd3a6fb5decd71de0f6dba6c954fc4d7003ed152b4279d
78c0d9b5d93eec1a6118d0c27c05d2cf43ca1b1d8f85a5b64491134781b8a5c0
33a9068c3937d8e17846767c8c344ff4f932140704362e2546d2c4dc5d85e436
a5424fa7a0b9a81d2b11845dba0a694da2a9763e06fb9392e6d2af59469a1fd8
40dde2e5940bccd39ec8a3af05c2ce46cc4aa7ad4f2599d9eab832b6fbfd5661
d5a63233aa9309c2d53f15bf945e01ffccaea56727f87ed2e2779e686b3aa758
ca8073c043cc387b585657e17f8c8ea9fa3dcec37679403aec98b76a77e439ae
9d75fb43e225104caaf9ff567b13969850ee132dc0842158cec82cd397dca5f5
c6225b29a41a9084271387b16130332efb838003fdcd6b6bb1001c1e07dbc230
c8dfa1603a030e1dfed7c1466f18c93f0ddcdca9d8df6ef323fb1482df496d10'''
api_key_list = [line for line in api_keys.split("\n")]


class VirusTotal:

    # def __init__(self):
    #     self.detail("38de5b216c33833af710e88f7f64fc98")

    def detail(self, md5):
        # result_dict = {
        #     0: "Invalid resource, check what you are submitting",
        #     1: "Scan finished, information embedded"
        # }
        response = self.report(md5)  # if self.report(md5) is not False else 0
        if response is False:
            return False
        try:
            if response["response_code"] == 1:
                # positives = response["positives"]
                # permalink = response["permalink"]
                detected = {}
                for av_name, values in response["scans"].items():
                    if response["scans"][av_name]["detected"] is True:
                        detected[av_name] = values
                # detected = [{av_name: values} for av_name, values in response["scans"].items() if
                #             response["scans"][av_name]["detected"] is True]
                # detected_num = len(detected)
            else:
                return False
        except json.decoder.JSONDecodeError:
            return False

    def report(self, md5, retry=0):
        if retry >= 2:
            return False
        api_key = random.choice(api_key_list)
        url = "https://www.virustotal.com/vtapi/v2/file/report"
        params = {"apikey": api_key, "resource": md5}
        try:
            response = requests.get(url, params=params).json()
        except json.decoder.JSONDecodeError and requests.exceptions.ConnectionError:
            self.report(md5, retry + 1)
        else:
            return response


def get_ssd(permalink):
    try:
        content = session.get(permalink).json()
        # content = json.loads(content)
        print(content["data"]["attributes"]["ssdeep"])
    except Exception as e:
        print(e)


def test():
    file_path = r"C:\Users\hewen\Desktop\Azorult.txt"
    list_1 = {}
    with open(file_path, "r", encoding="utf-8")as file:
        for line in file.readlines():
            result = VirusTotal().report(line)
            if result is dict:
                positives = result["positives"]
                if positives >= 15:
                    sha256 = result["sha256"]
                    list_1.update({line: sha256})
                    permalink = f"https://www.virustotal.com/ui/files/{line}"
                    get_ssd(permalink)
            break


if __name__ == "__main__":
    test()
