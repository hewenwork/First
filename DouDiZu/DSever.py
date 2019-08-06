import random


class _Server:
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

    def __init__(self):
        self.card_list = list(self.card_dict.keys())
        self.player1 = self._fapai()
        self.player2 = self._fapai()
        self.player3 = self._fapai()
        self.last_card = self._fapai()
        print(self.player1, self.player2, self.player3)
        print(self.last_card)

    def _fapai(self):
        # 随机取牌17张
        player = random.sample(self.card_list, 17)
        # 从总牌里面去除取走的牌
        for card in player:
            if card in self.card_list:
                self.card_list.remove(card)
        # 整理牌
        for x in range(len(player)):
            for num in range(len(player)-1-x):
                # for x in
                card_before, card_after = player[num],  player[num+1]
                if self.card_dict[card_before] >= self.card_dict[card_after]:
                    player[num],  player[num+1] = card_after, card_before
        return player


if __name__ == "__main__":
    _Server()
