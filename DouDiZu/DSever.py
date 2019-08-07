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
        cls.player1 = cls._fapai(17)
        cls.player2 = cls._fapai(17)
        cls.player3 = cls._fapai(17)
        cls.last_card = cls._fapai(3)
        cls._server = socket(AF_INET, SOCK_STREAM)
        cls._server.bind((host, port))
        return object.__new__(cls)

    def __init__(self):
        self._server.listen(3)
        while True:
            client, addr = self._server.accept()
            re_data = client.recv(1024).decode("utf-8")
            print(re_data)
            if re_data == "玩家1发牌":
                se_data = json.dumps(self.player1)
                print(se_data)
                client.send(se_data, addr)

    @classmethod
    def _fapai(cls, get_num):
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


if __name__ == "__main__":
    _Server()
