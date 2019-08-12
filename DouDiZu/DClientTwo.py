from socket import *


class _Client:

    def __new__(cls, *args, **kwargs):
        host = "192.168.2.226"
        port = 8010
        cls.client = socket(AF_INET, SOCK_STREAM)
        cls.client.connect((host, port))
        return object.__new__(cls)

    def __init__(self):
        self.client.send("玩家2发牌".encode("utf-8"))
        re_data = eval(self.client.recv(1024).decode("utf-8"))
        re_data1 = eval(self.client.recv(1024).decode("utf-8"))
        print(re_data)
        print(re_data1)
        # self.client.send()


if __name__ == "__main__":
    _Client()
    input()