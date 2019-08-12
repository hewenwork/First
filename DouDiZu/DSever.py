import json
import random
from socket import *


class _Server(object):
    card_dict = {
        "♣2": 15,
        "♣3": 3,
        "♣4": 4,
        "♣5": 5,
        "♣6": 6,
        "♣7": 7,
        "♣8": 8,
        "♣9": 9,
        "♣10": 10,
        "♣J": 11,
        "♣Q": 12,
        "♣K": 13,
        "♣A": 14,
        "♥2": 15,
        "♥3": 3,
        "♥4": 4,
        "♥5": 5,
        "♥6": 6,
        "♥7": 7,
        "♥8": 8,
        "♥9": 9,
        "♥10": 10,
        "♥J": 11,
        "♥Q": 12,
        "♥K": 13,
        "♥A": 14,
        "♦2": 15,
        "♦3": 3,
        "♦4": 4,
        "♦5": 5,
        "♦6": 6,
        "♦7": 7,
        "♦8": 8,
        "♦9": 9,
        "♦10": 10,
        "♦J": 11,
        "♦Q": 12,
        "♦K": 13,
        "♦A": 14,
        "♠2": 15,
        "♠3": 3,
        "♠4": 4,
        "♠5": 5,
        "♠6": 6,
        "♠7": 7,
        "♠8": 8,
        "♠9": 9,
        "♠10": 10,
        "♠J": 11,
        "♠Q": 12,
        "♠K": 13,
        "♠A": 14,
        "小🥁": 16,
        "大🥁": 17
    }
    card_list = list(card_dict.keys())

    def __new__(cls, *args, **kwargs):
        host = gethostbyname(gethostname())
        port = 8010
        cls.player_num = 0
        cls.call_dizhu = False
        cls.player1 = cls.get_card(17)
        cls.player2 = cls.get_card(17)
        cls.player3 = cls.get_card(17)
        cls.last_card = cls.get_card(3)
        cls.player_card = [cls.player1, cls.player2, cls.player3]
        cls._server = socket(AF_INET, SOCK_STREAM)
        cls._server.bind((host, port))
        return object.__new__(cls)

    @classmethod
    def get_card(cls, get_num):
        # 随机取牌17张
        player = random.sample(cls.card_list, get_num)
        # 从总牌里面去除取走的牌
        for card in player:
            if card in cls.card_list:
                cls.card_list.remove(card)
        # 整理牌
        for x in range(len(player)):
            for num in range(len(player) - 1 - x):
                card_before, card_after = player[num], player[num + 1]
                if cls.card_dict[card_before] >= cls.card_dict[card_after]:
                    player[num], player[num + 1] = card_after, card_before
        return player

    def __init__(self):
        self._server.listen(3)
        while True:
            client, addr = self._server.accept()
            re_command = client.recv(1024).decode("utf-8")
            self.send_card(client, re_command, addr)

    def send_card(self, client, re_command, addr):
        if re_command == "发牌" and self.player_num < 3:
            self.send_data(client, self.player_card.pop(), addr)
            self.player_num += 1
        elif re_command == "叫地主":
            if self.call_dizhu == True:
                self.send_data(client, "nn", addr)
            else:
                self.send_data(client, self.last_card, addr)
                self.call_dizhu = True

    def send_data(self, client, data, addr):
        se_data = bytes(str(data), encoding="utf-8")
        client.sendto(se_data, addr)


if __name__ == "__main__":
    _Server()
