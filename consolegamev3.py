# cups_game.py
import random
import uuid
from datetime import datetime

class Card:
    def __init__(self, facevalue, suit):
        self.facevalue = str(facevalue)
        self.suit = suit

    def __str__(self):
        return f"{self.facevalue}{self.suit}"

class CupCard(Card):
    def __init__(self, facevalue=10, suit="C"):
        super().__init__(facevalue, suit)

class SaucerCard(Card):
    def __init__(self, facevalue=10, suit="D"):
        super().__init__(facevalue, suit)

class PostDoubleBonusCard(Card):
    def __init__(self, facevalue=2, suit="C"):
        super().__init__(facevalue, suit)

class Deck:
    suits = ["D", "C", "H", "S"]
    vals = [str(i) for i in range(2, 11)] + ["J", "Q", "K", "A"]

    def __init__(self):
        self.cards = self.initializeCards()
        self.shuffleDeck()

    def initializeCards(self):
        cards = []
        for s in Deck.suits:
            for v in Deck.vals:
                if v == "2" and s == "C":
                    newcard = PostDoubleBonusCard(facevalue=v, suit=s)
                elif v == "10" and s == "C":
                    newcard = CupCard(facevalue=v, suit=s)
                elif v == "10" and s == "D":
                    newcard = SaucerCard(facevalue=v, suit=s)
                else:
                    newcard = Card(facevalue=v, suit=s)
                cards.append(newcard)
        return cards

    def shuffleDeck(self):
        random.shuffle(self.cards)

    def drawCard(self):
        if not self.cards:
            return None
        return self.cards.pop()

    def dealHand(self, player):
        if len(self.cards) < 2:
            player.hand = []
            return False
        player.hand = [self.drawCard(), self.drawCard()]
        return True

class Player:
    def __init__(self, name):
        self.name = name
        self.money = 0
        self.hand = []

class GameManager:
    def __init__(self):
        self.players = {}
        self.deck = Deck()
        self.gameEnd = False
        self.turnNumber = 0
        self.sitBonusTurn = random.randint(1, 12)

    def createPlayers(self, playername):
        self.players = {
            "Dealer": Player("Dealer"),
            "Player": Player(playername)
        }

    def dealToPlayers(self):
        return self.deck.dealHand(self.players["Dealer"]) and self.deck.dealHand(self.players["Player"])

    def _hand_cards(self, hand):
        cards = [str(c) for c in hand] if hand else []
        return cards if len(cards) == 2 else ["N/A", "N/A"]

    def _event(self, event_type, payout, who, turn_number, card1_player="N/A", card2_player="N/A", card1_dealer="N/A", card2_dealer="N/A"):
        return {
            "turn_number": turn_number,
            "event_id": f"evt_{turn_number:06d}_{uuid.uuid4().hex[:8]}",
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "event_type": event_type,
            "winner_of_event": who,
            "card1_player": card1_player,
            "card2_player": card2_player,
            "card1_dealer": card1_dealer,
            "card2_dealer": card2_dealer,
            # "event_payout_total_in_game": payout,
            "player_money": self.players["Player"].money,
            "dealer_money": self.players["Dealer"].money,
        }

    def isDCup(self):
        payout = 400
        p = self.players["Player"]
        d = self.players["Dealer"]
        ph = self._hand_cards(p.hand)
        dh = self._hand_cards(d.hand)

        if "3" in ph and "6" in ph:
            p.money += payout
            return True, self._event("D Cup", payout, "player", self.turnNumber, ph[0], ph[1], dh[0], dh[1])
        if "3" in dh and "6" in dh:
            d.money += payout
            return True, self._event("D Cup", payout, "dealer", self.turnNumber, ph[0], ph[1], dh[0], dh[1])
        return False, None

    def isFullCup(self):
        payout = 100
        p = self.players["Player"]
        d = self.players["Dealer"]
        ph = self._hand_cards(p.hand)
        dh = self._hand_cards(d.hand)

        if "4" in ph and "9" in ph:
            p.money += payout
            return True, self._event("Full Cup", payout, "player", self.turnNumber, ph[0], ph[1], dh[0], dh[1])
        if "4" in dh and "9" in dh:
            d.money += payout
            return True, self._event("Full Cup", payout, "dealer", self.turnNumber, ph[0], ph[1], dh[0], dh[1])
        return False, None

    def isHalfCup(self):
        payout = 50
        p = self.players["Player"]
        d = self.players["Dealer"]
        ph = self._hand_cards(p.hand)
        dh = self._hand_cards(d.hand)

        def isWin(hand):
            return (
                ("2" in hand and "4" in hand) or
                ("2" in hand and "5" in hand) or
                ("A" in hand and "5" in hand) or
                ("A" in hand and "6" in hand) or
                (hand[0] == "3" and hand[1] == "3") or
                ("3" in hand and "4" in hand)
            )

        if isWin(ph):
            p.money += payout
            return True, self._event("Half A Cup", payout, "player", self.turnNumber, ph[0], ph[1], dh[0], dh[1])
        if isWin(dh):
            d.money += payout
            return True, self._event("Half A Cup", payout, "dealer", self.turnNumber, ph[0], ph[1], dh[0], dh[1])
        return False, None

    def isAlmostHalfCup(self):
        payout = 45
        p = self.players["Player"]
        d = self.players["Dealer"]
        ph = self._hand_cards(p.hand)
        dh = self._hand_cards(d.hand)

        def isWin(hand):
            return (
                ("4" in hand and "5" in hand) or
                ("A" in hand and "8" in hand) or
                ("2" in hand and "7" in hand) or
                ("A" in hand and "3" in hand) or
                (hand[0] == "2" and hand[1] == "2")
            )

        def hasFace(hand):
            return any(c[0] in ["J", "Q", "K", "A"] for c in hand)

        if isWin(ph) and hasFace(dh):
            p.money += payout
            return True, self._event("Almost Half A Cup", payout, "player", self.turnNumber, ph[0], ph[1], dh[0], dh[1])
        if isWin(dh) and hasFace(ph):
            d.money += payout
            return True, self._event("Almost Half A Cup", payout, "dealer", self.turnNumber, ph[0], ph[1], dh[0], dh[1])
        return False, None

    def isCupInAPizzaBox(self):
        payout = 60
        p = self.players["Player"]
        d = self.players["Dealer"]
        ph = self._hand_cards(p.hand)
        dh = self._hand_cards(d.hand)

        def isWin(hand):
            return "2" in hand and "3" in hand

        def hasFace(hand):
            return any(c[0] in ["J", "Q", "K", "A"] for c in hand)

        if isWin(ph) and hasFace(dh):
            p.money += payout
            return True, self._event("Cup In A Pizza Box", payout, "player", self.turnNumber, ph[0], ph[1], dh[0], dh[1])
        if isWin(dh) and hasFace(ph):
            d.money += payout
            return True, self._event("Cup In A Pizza Box", payout, "dealer", self.turnNumber, ph[0], ph[1], dh[0], dh[1])
        return False, None

    def hasCupCard(self):
        payout = 75
        p = self.players["Player"]
        d = self.players["Dealer"]
        ph = self._hand_cards(p.hand)
        dh = self._hand_cards(d.hand)

        if any(type(c) == CupCard for c in p.hand):
            p.money += payout
            return True, self._event("Cup Card", payout, "player", self.turnNumber, ph[0], ph[1], dh[0], dh[1])
        if any(type(c) == CupCard for c in d.hand):
            d.money += payout
            return True, self._event("Cup Card", payout, "dealer", self.turnNumber, ph[0], ph[1], dh[0], dh[1])
        return False, None

    def hasSaucerCard(self):
        payout = 80
        p = self.players["Player"]
        d = self.players["Dealer"]
        ph = self._hand_cards(p.hand)
        dh = self._hand_cards(d.hand)

        if any(type(c) == SaucerCard for c in p.hand):
            p.money += payout
            return True, self._event("Saucer Card", payout, "player", self.turnNumber, ph[0], ph[1], dh[0], dh[1])
        if any(type(c) == SaucerCard for c in d.hand):
            d.money += payout
            return True, self._event("Saucer Card", payout, "dealer", self.turnNumber, ph[0], ph[1], dh[0], dh[1])
        return False, None

    def checkSittingDownBonus(self):
        p = self.players["Player"]
        d = self.players["Dealer"]
        ph = self._hand_cards(p.hand)
        dh = self._hand_cards(d.hand)

        if self.sitBonusTurn == self.turnNumber:
            bonus = 215
            p.money += bonus
            return True, self._event("Sitting Down Bonus", bonus, "player", self.turnNumber, ph[0], ph[1], dh[0], dh[1])
        return False, None

    def doublingBonus(self):
        p = self.players["Player"]
        d = self.players["Dealer"]
        ph = self._hand_cards(p.hand)
        dh = self._hand_cards(d.hand)

        if p.money == 700:
            p.money *= 2
            drawn = self.deck.drawCard()
            payout = 100 if type(drawn) == PostDoubleBonusCard else 0
            if payout:
                p.money += payout
            return True, self._event("Doubling Bonus", payout, "player", self.turnNumber, ph[0], ph[1], dh[0], dh[1])
        return False, None

    def checkGameEnd(self):
        return len(self.deck.cards) < 4

    def run_game(self, playername="SIM"):
        self.createPlayers(playername)
        self.deck = Deck()
        self.gameEnd = False
        self.turnNumber = 0
        events = []

        while not self.gameEnd:
            if not self.dealToPlayers():
                break

            self.turnNumber += 1

            turn_checks = [
                self.isDCup,
                self.isFullCup,
                self.isHalfCup,
                self.isAlmostHalfCup,
                self.isCupInAPizzaBox,
                self.hasCupCard,
                self.hasSaucerCard,
                self.checkSittingDownBonus,
                self.doublingBonus,
            ]

            for fn in turn_checks:
                hit, event = fn()
                if hit and event is not None:
                    events.append(event)

            if self.checkGameEnd():
                self.gameEnd = True

        winner = "tie"
        if self.players["Dealer"].money > self.players["Player"].money:
            winner = "dealer"
        elif self.players["Player"].money > self.players["Dealer"].money:
            winner = "player"

        return {
            "winner": winner,
            "player_money": self.players["Player"].money,
            "dealer_money": self.players["Dealer"].money,
            "turns": self.turnNumber,
            "events": events,
        }
