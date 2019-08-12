from socket import *


class _Client:

    def __new__(cls, *args, **kwargs):
        host = "192.168.2.226"
        port = 8010
        cls.client = socket(AF_INET, SOCK_STREAM)
        cls.client.connect((host, port))
        return object.__new__(cls)

    def __init__(self):
        # start
        self.client.send("发牌".encode("utf-8"))
        self.card = eval(self.client.recv(1024).decode("utf-8"))
        print(self.card)
        self.client.send("叫地主".encode("utf-8"))
        self.card_re = eval(self.client.recv(1024).decode("utf-8"))
        print(self.card_re)


if __name__ == "__main__":
    _Client()
