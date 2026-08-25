from app.game.models import Deck, Player, Card
from app.game import rules
import random

class GameManager:
    def __init__(self):
        self.reset()

    def reset(self):
        self.deck = Deck()
        self.players = {}
        self.turn_number = 0
        self.game_end = False
        self.sit_bonus_turn = random.randint(1, 12)
        self.last_events = []

    def start_game(self, player_name: str):
        self.reset()
        self.players = {
            "Dealer": Player("Dealer"),
            "Player": Player(player_name),
        }
        self.last_events = [{"type": "game_started"}]
        return self.serialize_state()

    def serialize_card(self, c: Card):
        return {"facevalue": c.facevalue, "suit": c.suit}

    def serialize_player(self, p: Player):
        return {
            "name": p.name,
            "money": p.money,
            "hand": [self.serialize_card(c) for c in p.hand],
        }

    def serialize_state(self):
        return {
            "turn_number": self.turn_number,
            "game_end": self.game_end,
            "deck_count": len(self.deck.cards),
            "sit_bonus_turn": self.sit_bonus_turn,
            "players": {k: self.serialize_player(v) for k, v in self.players.items()},
            "last_events": self.last_events,
        }

    def deal_to(self, who: str):
        card = self.deck.draw_card()
        self.players[who].hand.append(card)
        return {"type": "deal", "who": who, "card": self.serialize_card(card)}

    def discard_hand(self, who: str):
        self.players[who].hand = []
        return {"type": "discard", "who": who}

    def apply_payout(self, who: str, amount: int, reason: str):
        self.players[who].money += amount
        return {"type": "payout", "who": who, "amount": amount, "reason": reason}

    def resolve_turn(self):
        self.turn_number += 1
        self.last_events = []

        self.last_events.append(self.discard_hand("Dealer"))
        self.last_events.append(self.discard_hand("Player"))

        self.last_events.append(self.deal_to("Dealer"))
        self.last_events.append(self.deal_to("Player"))
        self.last_events.append(self.deal_to("Dealer"))
        self.last_events.append(self.deal_to("Player"))

        p = self.players["Player"]
        d = self.players["Dealer"]

        if rules.is_d_cup(p):
            self.last_events.append(self.apply_payout("Player", 400, "D Cup"))
        elif rules.is_d_cup(d):
            self.last_events.append(self.apply_payout("Dealer", 400, "D Cup"))
        elif rules.is_full_cup(p):
            self.last_events.append(self.apply_payout("Player", 100, "Full Cup"))
        elif rules.is_full_cup(d):
            self.last_events.append(self.apply_payout("Dealer", 100, "Full Cup"))
        elif rules.is_half_cup(p):
            self.last_events.append(self.apply_payout("Player", 50, "Half A Cup"))
        elif rules.is_half_cup(d):
            self.last_events.append(self.apply_payout("Dealer", 50, "Half A Cup"))
        elif rules.is_almost_half_cup(p):
            self.last_events.append(self.apply_payout("Player", 45, "Almost Half A Cup"))
        elif rules.is_almost_half_cup(d):
            self.last_events.append(self.apply_payout("Dealer", 45, "Almost Half A Cup"))
        elif rules.is_cup_in_a_pizza_box(p):
            self.last_events.append(self.apply_payout("Player", 60, "Cup In A Pizza Box"))
        elif rules.is_cup_in_a_pizza_box(d):
            self.last_events.append(self.apply_payout("Dealer", 60, "Cup In A Pizza Box"))
        elif rules.has_cup_card(p):
            self.last_events.append(self.apply_payout("Player", 75, "Cup Card"))
        elif rules.has_cup_card(d):
            self.last_events.append(self.apply_payout("Dealer", 75, "Cup Card"))
        elif rules.has_saucer_card(p):
            self.last_events.append(self.apply_payout("Player", 80, "Saucer Card"))
        elif rules.has_saucer_card(d):
            self.last_events.append(self.apply_payout("Dealer", 80, "Saucer Card"))

        if self.players["Player"].money == 700:
            self.players["Player"].money *= 2
            self.last_events.append({"type": "double_bonus", "who": "Player", "new_money": self.players["Player"].money})

            if len(self.deck.cards) > 0:
                card = self.deck.draw_card()
                self.last_events.append({"type": "bonus_draw", "card": self.serialize_card(card)})
                if card.suit == "C" and card.facevalue == "2":
                    self.players["Player"].money += 100
                    self.last_events.append({"type": "payout", "who": "Player", "amount": 100, "reason": "Post Double Bonus Card"})

        if self.turn_number == self.sit_bonus_turn:
            self.players["Player"].money += 700
            self.last_events.append({"type": "sit_bonus", "who": "Player", "amount": 700})

        if len(self.deck.cards) < 4:
            self.game_end = True

        return self.serialize_state()



# from app.game.models import Deck, Player, Card
# from app.game import rules
# import random

# class GameManager:
#     def __init__(self):
#         self.reset()

#     def reset(self):
#         self.deck = Deck()
#         self.players = {}
#         self.turn_number = 0
#         self.game_end = False
#         self.sit_bonus_turn = random.randint(1, 12)
#         self.last_events = []

#     def start_game(self, player_name: str):
#         self.reset()
#         self.players = {
#             "Dealer": Player("Dealer"),
#             "Player": Player(player_name),
#         }
#         self.last_events = [{"type": "game_started"}]
#         return self.serialize_state()

#     def serialize_card(self, c: Card):
#         return {"facevalue": c.facevalue, "suit": c.suit}

#     def serialize_player(self, p: Player):
#         return {
#             "name": p.name,
#             "money": p.money,
#             "hand": [self.serialize_card(c) for c in p.hand],
#         }

#     def serialize_state(self):
#         return {
#             "turn_number": self.turn_number,
#             "game_end": self.game_end,
#             "deck_count": len(self.deck.cards),
#             "sit_bonus_turn": self.sit_bonus_turn,
#             "players": {k: self.serialize_player(v) for k, v in self.players.items()},
#             "last_events": self.last_events,
#         }

#     def deal_round(self):
#         dealer = self.players["Dealer"]
#         player = self.players["Player"]

#         self.deck.deal_hand(dealer)
#         self.deck.deal_hand(player)

#         return [
#             {"type": "deal", "who": "Dealer", "hand": [self.serialize_card(c) for c in dealer.hand]},
#             {"type": "deal", "who": "Player", "hand": [self.serialize_card(c) for c in player.hand]},
#         ]

#     def draw_one(self, who: str):
#         card = self.deck.draw_card()
#         self.players[who].hand = [card]
#         return {"type": "draw", "who": who, "card": self.serialize_card(card)}

#     def discard_hand(self, who: str):
#         self.players[who].hand = []
#         return {"type": "discard", "who": who}

#     def apply_payout(self, who: str, amount: int, reason: str):
#         self.players[who].money += amount
#         return {"type": "payout", "who": who, "amount": amount, "reason": reason}

#     def resolve_turn(self):
#         self.turn_number += 1
#         self.last_events = []

#         self.last_events.extend(self.deal_round())

#         p = self.players["Player"]
#         d = self.players["Dealer"]

#         if self.turn_number == 1:
#             if any(c.suit == "D" and c.facevalue == "10" for c in [*p.hand, *d.hand]):
#                 self.last_events.append(self.apply_payout("Player", 80, "Saucer Card"))

#         if rules.is_d_cup(p):
#             self.last_events.append(self.apply_payout("Player", 400, "D Cup"))
#         elif rules.is_d_cup(d):
#             self.last_events.append(self.apply_payout("Dealer", 400, "D Cup"))
#         elif rules.is_full_cup(p):
#             self.last_events.append(self.apply_payout("Player", 100, "Full Cup"))
#         elif rules.is_full_cup(d):
#             self.last_events.append(self.apply_payout("Dealer", 100, "Full Cup"))
#         elif rules.is_half_cup(p):
#             self.last_events.append(self.apply_payout("Player", 50, "Half A Cup"))
#         elif rules.is_half_cup(d):
#             self.last_events.append(self.apply_payout("Dealer", 50, "Half A Cup"))
#         elif rules.is_almost_half_cup(p):
#             self.last_events.append(self.apply_payout("Player", 45, "Almost Half A Cup"))
#         elif rules.is_almost_half_cup(d):
#             self.last_events.append(self.apply_payout("Dealer", 45, "Almost Half A Cup"))
#         elif rules.is_cup_in_a_pizza_box(p):
#             self.last_events.append(self.apply_payout("Player", 60, "Cup In A Pizza Box"))
#         elif rules.is_cup_in_a_pizza_box(d):
#             self.last_events.append(self.apply_payout("Dealer", 60, "Cup In A Pizza Box"))
#         elif rules.has_cup_card(p):
#             self.last_events.append(self.apply_payout("Player", 75, "Cup Card"))
#         elif rules.has_cup_card(d):
#             self.last_events.append(self.apply_payout("Dealer", 75, "Cup Card"))
#         elif rules.has_saucer_card(p):
#             self.last_events.append(self.apply_payout("Player", 80, "Saucer Card"))
#         elif rules.has_saucer_card(d):
#             self.last_events.append(self.apply_payout("Dealer", 80, "Saucer Card"))

#         if self.players["Player"].money == 700:
#             self.players["Player"].money *= 2
#             self.last_events.append({"type": "double_bonus", "who": "Player", "new_money": self.players["Player"].money})

#             if len(self.deck.cards) > 0:
#                 card = self.deck.draw_card()
#                 self.last_events.append({"type": "bonus_draw", "card": self.serialize_card(card)})
#                 if card.suit == "C" and card.facevalue == "2":
#                     self.players["Player"].money += 100
#                     self.last_events.append({"type": "payout", "who": "Player", "amount": 100, "reason": "Post Double Bonus Card"})

#         if self.turn_number == self.sit_bonus_turn:
#             self.players["Player"].money += 700
#             self.last_events.append({"type": "sit_bonus", "who": "Player", "amount": 700})

#         if len(self.deck.cards) < 4:
#             self.game_end = True

#         return self.serialize_state()

#     def get_winner(self):
#         p = self.players["Player"].money
#         d = self.players["Dealer"].money
#         if p > d:
#             return {"winner": "Player", "money": p}
#         elif d > p:
#             return {"winner": "Dealer", "money": d}
#         return {"winner": "Tie", "money": p}
