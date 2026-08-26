# cups_game.py
import random
import time

class Card:
    def __init__(self, facevalue, suit):
        self.facevalue = str(facevalue)
        self.suit = suit

    def printCard(self):
        print(f"{self.facevalue} {self.suit}")

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
        return self.cards.pop()

    def dealHand(self, player):
        player.hand = [self.drawCard(), self.drawCard()]

class Player:
    def __init__(self, name):
        self.name = name
        self.money = 0
        self.hand = []

class GameManager:
    def __init__(self, auto_sit_down=True):
        self.players = {}
        self.deck = Deck()
        self.gameEnd = False
        self.turnNumber = 0
        self.sitBonusTurn = random.randint(1, 12)
        self.auto_sit_down = auto_sit_down

    def createPlayers(self, playername):
        self.players = {
            "Dealer": Player("Dealer"),
            "Player": Player(playername)
        }

    def dealToPlayers(self):
        self.deck.dealHand(self.players["Dealer"])
        self.deck.dealHand(self.players["Player"])

    def isDCup(self, player, dealer):
        payout = 400
        playerHand = [player.hand[0].facevalue, player.hand[1].facevalue]
        dealerHand = [dealer.hand[0].facevalue, dealer.hand[1].facevalue]
        if "3" in playerHand and "6" in playerHand:
            player.money += payout
            return True, "player", "D Cup", payout
        elif "3" in dealerHand and "6" in dealerHand:
            dealer.money += payout
            return True, "dealer", "D Cup", payout
        return False, None, None, 0

    def isFullCup(self, player, dealer):
        payout = 100
        playerHand = [player.hand[0].facevalue, player.hand[1].facevalue]
        dealerHand = [dealer.hand[0].facevalue, dealer.hand[1].facevalue]
        if "4" in playerHand and "9" in playerHand:
            player.money += payout
            return True, "player", "Full Cup", payout
        elif "4" in dealerHand and "9" in dealerHand:
            dealer.money += payout
            return True, "dealer", "Full Cup", payout
        return False, None, None, 0

    def isHalfCup(self, player, dealer):
        payout = 50
        playerHand = [player.hand[0].facevalue, player.hand[1].facevalue]
        dealerHand = [dealer.hand[0].facevalue, dealer.hand[1].facevalue]

        def isWin(pHand):
            return (
                ("2" in pHand and "4" in pHand) or
                ("2" in pHand and "5" in pHand) or
                ("A" in pHand and "5" in pHand) or
                ("A" in pHand and "6" in pHand) or
                (pHand == ["3", "3"]) or
                ("3" in pHand and "4" in pHand)
            )

        if isWin(playerHand):
            player.money += payout
            return True, "player", "Half A Cup", payout
        elif isWin(dealerHand):
            dealer.money += payout
            return True, "dealer", "Half A Cup", payout
        return False, None, None, 0

    def isAlmostHalfCup(self, player, dealer):
        payout = 45
        playerHand = [player.hand[0].facevalue, player.hand[1].facevalue]
        dealerHand = [dealer.hand[0].facevalue, dealer.hand[1].facevalue]

        def isWin(pHand):
            return (
                ("4" in pHand and "5" in pHand) or
                ("A" in pHand and "8" in pHand) or
                ("2" in pHand and "7" in pHand) or
                ("A" in pHand and "3" in pHand) or
                (pHand == ["2", "2"])
            )

        def isMatchWin(pHand):
            faces = ["J", "Q", "K", "A"]
            return any(c in pHand for c in faces)

        if isWin(playerHand) and isMatchWin(dealerHand):
            player.money += payout
            return True, "player", "Almost Half A Cup", payout
        elif isWin(dealerHand) and isMatchWin(playerHand):
            dealer.money += payout
            return True, "dealer", "Almost Half A Cup", payout
        return False, None, None, 0

    def isCupInAPizzaBox(self, player, dealer):
        payout = 60
        playerHand = [player.hand[0].facevalue, player.hand[1].facevalue]
        dealerHand = [dealer.hand[0].facevalue, dealer.hand[1].facevalue]

        def isWin(pHand):
            return "2" in pHand and "3" in pHand

        def isMatchWin(pHand):
            faces = ["J", "Q", "K", "A"]
            return any(c in pHand for c in faces)

        if isWin(playerHand) and isMatchWin(dealerHand):
            player.money += payout
            return True, "player", "Cup In A Pizza Box", payout
        elif isWin(dealerHand) and isMatchWin(playerHand):
            dealer.money += payout
            return True, "dealer", "Cup In A Pizza Box", payout
        return False, None, None, 0

    def hasCupCard(self, player, dealer):
        payout = 75
        if CupCard in [type(l) for l in player.hand]:
            player.money += payout
            return True, "player", "Cup Card", payout
        elif SaucerCard in [type(l) for l in dealer.hand]:
            dealer.money += payout
            return True, "dealer", "Cup Card", payout
        return False, None, None, 0

    def hasSaucerCard(self, player, dealer):
        payout = 80
        if SaucerCard in [type(l) for l in player.hand]:
            player.money += payout
            return True, "player", "Saucer Card", payout
        elif SaucerCard in [type(l) for l in dealer.hand]:
            dealer.money += payout
            return True, "dealer", "Saucer Card", payout
        return False, None, None, 0

    def checkSittingDownBonus(self):
        if self.sitBonusTurn == self.turnNumber:
            bonus = 215
            self.players["Player"].money += bonus
            return True, "player", "Sitting Down Bonus", bonus
        return False, None, None, 0

    def doublingBonus(self, player):
        bonus = 700
        if player.money == bonus:
            player.money *= 2
            card = self.deck.drawCard()
            if type(card) == PostDoubleBonusCard:
                player.money += 100
                return True, "player", "Doubling Bonus +100", 100
            return True, "player", "Doubling Bonus Triggered", 0
        return False, None, None, 0

    def checkGameEnd(self):
        return len(self.deck.cards) < 4

    def run_game(self, playername="SIM"):
        self.createPlayers(playername)
        d = self.players["Dealer"]
        p = self.players["Player"]

        events = []

        while not self.gameEnd:
            self.turnNumber += 1
            self.dealToPlayers()

            if self.turnNumber == 1:
                hit, who, name, payout = self.hasSaucerCard(player=p, dealer=d)
                if hit:
                    events.append((who, name, payout))

            checks = [
                self.isDCup,
                self.isFullCup,
                self.isHalfCup,
                self.isAlmostHalfCup,
                self.isCupInAPizzaBox,
                self.hasCupCard,
                self.hasSaucerCard,
            ]

            for fn in checks:
                hit, who, name, payout = fn(player=p, dealer=d)
                if hit:
                    events.append((who, name, payout))
                    break

            hit, who, name, payout = self.checkSittingDownBonus()
            if hit:
                events.append((who, name, payout))

            hit, who, name, payout = self.doublingBonus(p)
            if hit:
                events.append((who, name, payout))

            if self.checkGameEnd():
                self.gameEnd = True

        winner = "tie"
        if d.money > p.money:
            winner = "dealer"
        elif p.money > d.money:
            winner = "player"

        return {
            "winner": winner,
            "player_money": p.money,
            "dealer_money": d.money,
            "turns": self.turnNumber,
            "events": events,
        }
