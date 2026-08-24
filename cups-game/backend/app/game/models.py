from dataclasses import dataclass, field
import random

@dataclass
class Card:
    facevalue: str
    suit: str

@dataclass
class Player:
    name: str
    money: int = 0
    hand: list[Card] = field(default_factory=list)

class Deck:
    suits = ["D", "C", "H", "S"]
    vals = [str(i) for i in range(2, 11)] + ["J", "Q", "K", "A"]

    def __init__(self):
        self.cards = self.initialize_cards()
        random.shuffle(self.cards)

    def initialize_cards(self):
        cards = []
        for s in self.suits:
            for v in self.vals:
                cards.append(Card(facevalue=v, suit=s))
        return cards

    def draw_card(self):
        return self.cards.pop()

    def deal_hand(self, player: Player):
        player.hand = [self.draw_card(), self.draw_card()]
