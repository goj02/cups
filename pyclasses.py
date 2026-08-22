import random
import time 

#first version, use console input

class Card:
    def __init__(self, facevalue, suit):
        self.facevalue = facevalue
        self.suit = suit

    def printCard(self):
        print(f"{self.facevalue} {self.suit}")

class CupCard(Card):
    def __init__(self):
        super().__init__(10, "C")

class SaucerCard(Card):
    def __init__(self):
        super().__init__(10, "D")

class PostDoubleBonusCard(Card):
    def __init__(self):
        super().__init__(2, "C")


class Deck:
    suits = ["D", "C", "H", "S"]
    vals = [str(i) for i in range(2,11)] + ["J", "Q", "K", "A"]

    def __init__(self):
        self.cards = self.initializeCards()
        self.shuffleDeck()

    def initializeCards(self):
        cardcount = 52
        cards = []
        # CupCard = 10 Clubs
        # SaucerCard = 10 Diamonds 
        # PostDoubleBonusCard = 2 Clubs
        for s in Deck.suits:
            for v in Deck.vals:
                if v==2 and s=="C":
                    newcard = PostDoubleBonusCard(facevalue=v, suit=s)
                elif v==10 and s=="C":
                    newcard = CupCard(facevalue=v, suit=s)
                elif v==10 and s=="D":
                    newcard = SaucerCard(facevalue=v, suit=s)
                else:
                    newcard = Card(facevalue=v, suit=s)
                cards.append(newcard)
        print(f"Created {len(cards)} cards")
        return cards 
    
    def shuffleDeck(self):
        random.shuffle(self.cards)
        print(f"Shuffled deck")

    def drawCard(self):
        return self.cards.pop()

    def dealHand(self, player):
        #using pop will remove from right side, 
        #so right side is top of deck
        player.hand = [self.drawCard(), self.drawCard()]
        print(f"Dealt hand to {player.name}")



class Player:
    def __init__(self, name):
        self.name = name
        self.money = 0
        self.hand = []

    def printHand(self):
        print(f"{self.name} : {self.hand[0].facevalue} {self.hand[0].suit} | {self.hand[1].facevalue} {self.hand[1].suit}")

    def discardHand(self):
        #release objects from memory
        self.hand.pop()
        self.hand.pop()

class GameManager:
    def __init__(self):
        self.players = {}
        self.deck = Deck()
        self.gameEnd = False
        self.turnNumber = 0
        self.sitBonusTurn = random.randint(1,12)

    def createPlayers(self, playername):
        self.players = {
            "Dealer":Player("Dealer"),
            "Player":Player(playername)
        }

    def dealToPlayers(self):
        self.deck.dealHand(self.players["Dealer"])
        self.deck.dealHand(self.players["Player"])
        

    '''
    These functions check the winning hands
    If there is a winner, increment their score and return True to trigger 
                the next step in the round
            otherwise return False
    '''
    # def isWinningHand(self, player: Player, dealer: Player, winningHand: bool, payout: int, handname: str) -> bool:
    #     '''
    #     generalized function checking both users' hands
    #     return True if there is a winner for the hand being checked
    #         and increment the player's money
    #     example winningHand: 3 in dealerHand and 6 in dealerHand

    #     '''
    #     if winningHand:
    #         player.money+=payout
    #         print(f"{player.name} won ${payout} with a {hname}!")
    #         return True
    #     elif 3 in dealerHand and 6 in dealerHand:
    #         dealer.money+=payout
    #         print(f"{dealer.name} won ${payout} with a {hname}!")
    #         return True
    #     else:
    #         #the dealer and the player dont have the winning hand 
    #         return False
    def isDCup(self, player: Player, dealer: Player):
        '''
        Run first
        Check for a 3 and a 6, reward $400
        '''
        payout = 400
        hname = "D Cup"
        playerHand = [player.hand[0].facevalue, player.hand[1].facevalue]
        dealerHand = [dealer.hand[0].facevalue, dealer.hand[1].facevalue] 
        if '3' in playerHand and '6' in playerHand:
            player.money+=payout
            print(f"{player.name} won ${payout} with a {hname}!")
            return True
        elif '3' in dealerHand and '6' in dealerHand:
            dealer.money+=payout
            print(f"{dealer.name} won ${payout} with a {hname}!")
            return True
        else:
            #the dealer and the player dont have the winning hand 
            return False

    def isFullCup(self, player: Player, dealer: Player):
        '''
        DCup is run first
        
        '''
        payout = 100
        hname = "Full Cup"
        playerHand = [player.hand[0].facevalue, player.hand[1].facevalue]
        dealerHand = [dealer.hand[0].facevalue, dealer.hand[1].facevalue] 
        if '4' in playerHand and '9' in playerHand:
            player.money+=payout
            print(f"{player.name} won ${payout} with a {hname}!")
            return True
        elif '4' in dealerHand and '9' in dealerHand:
            dealer.money+=payout
            print(f"{dealer.name} won ${payout} with a {hname}!")
            return True
        else:
            #the dealer and the player dont have the winning hand 
            return False

    def isHalfCup(self, player: Player, dealer: Player):
        '''
            • [2/4]
            • 2/5
            • [A/5]
            • [A/6]
            • [3/3]
            • [3/4]

        '''
        payout = 50
        hname = "Half A Cup"
        playerHand = [player.hand[0].facevalue, player.hand[1].facevalue]
        dealerHand = [dealer.hand[0].facevalue, dealer.hand[1].facevalue]  
        def isWin(pHand):
            w1 = '2' in pHand and '4' in pHand
            w2 = '2' in pHand and '5' in pHand
            w3 = 'A' in pHand and '5' in pHand
            w4 = 'A' in pHand and '6' in pHand
            w5 = pHand==['3', '3']
            w6 = '3' in pHand and '4' in pHand
            return w1 or w2 or w3 or w4 or w5 or w6 


        if isWin(playerHand):
            player.money+=payout
            print(f"{player.name} won ${payout} with a {hname}!")
            return True
        elif isWin(dealerHand):
            dealer.money+=payout
            print(f"{dealer.name} won ${payout} with a {hname}!")
            return True
        else:
            #the dealer and the player dont have the winning hand 
            return False

    def isAlmostHalfCup(self, player: Player, dealer: Player):
        '''
        • 4/5
        • [A/8]
        • [2/7]
        • [A/3]
        • [2/2]

        '''
        payout = 45
        hname = "Almost Half A Cup"
        playerHand = [player.hand[0].facevalue, player.hand[1].facevalue]
        dealerHand = [dealer.hand[0].facevalue, dealer.hand[1].facevalue]  
        def isWin(pHand):
            '''
            One player should have the defined pairs
            '''
            w1 = '4' in pHand and '5' in pHand
            w2 = 'A' in pHand and '8' in pHand
            w3 = '2' in pHand and '7' in pHand
            w4 = 'A' in pHand and '3' in pHand
            w5 = pHand==['2', '2']
            return w1 or w2 or w3 or w4 or w5 
        
        def isMatchWin(pHand):
            '''
            the other player should have at least one face card if win1 is True
            '''
            faces = ["J", "Q", "K", "A"]
            return any(c in pHand for c in faces)


        if isWin(playerHand) and isMatchWin(dealerHand):
            player.money+=payout
            print(f"{player.name} won ${payout} with a {hname}!")
            return True
        elif isWin(dealerHand) and isMatchWin(playerHand):
            dealer.money+=payout
            print(f"{dealer.name} won ${payout} with a {hname}!")
            return True
        else:
            #the dealer and the player dont have the winning hand 
            return False

    def isCupInAPizzaBox(self, player: Player, dealer: Player):
        payout = 60
        hname = "Cup In A Pizza Box"
        playerHand = [player.hand[0].facevalue, player.hand[1].facevalue]
        dealerHand = [dealer.hand[0].facevalue, dealer.hand[1].facevalue]  
        def isWin(pHand):
            '''
            One player should have the defined pairs
            '''
            return '2' in pHand and '3' in pHand
            
        
        def isMatchWin(pHand):
            '''
            the other player should have at least one face card if win1 is True
            '''
            faces = ["J", "Q", "K", "A"]
            return any(c in pHand for c in faces)


        if isWin(playerHand) and isMatchWin(dealerHand):
            player.money+=payout
            print(f"{player.name} won ${payout} with a {hname}!")
            return True
        elif isWin(dealerHand) and isMatchWin(playerHand):
            dealer.money+=payout
            print(f"{dealer.name} won ${payout} with a {hname}!")
            return True
        else:
            #the dealer and the player dont have the winning hand 
            return False

    def hasCupCard(self, player: Player, dealer: Player):
        '''
        DCup check already runs before this
        '''
        payout = 75
        hname = "Cup Card"
        
        if CupCard in [type(l) for l in player.hand]:
            player.money+=payout
            print(f"{player.name} won ${payout} with a {hname}!")
            return True
        elif CupCard in [type(l) for l in dealer.hand]:
            dealer.money+=payout
            print(f"{dealer.name} won ${payout} with a {hname}!")
            return True
        else:
            return False
        

    def hasSaucerCard(self, player: Player, dealer: Player):
        '''
        add another check in the turn loop for turn 1
        DCup check already runs before this
        '''
        payout = 80
        hname = "Saucer Card"
        if SaucerCard in [type(l) for l in player.hand]:
            player.money+=payout
            print(f"{player.name} won ${payout} with a {hname}!")
            return True
        elif SaucerCard in [type(l) for l in dealer.hand]:
            dealer.money+=payout
            print(f"{dealer.name} won ${payout} with a {hname}!")
            return True
        else:
            return False

    def doublingBonus(self, player: Player):
        bonus = 700
        if player.money == bonus:
            userinput = input(f"How much money have you won so far?\n")
            userinput = input(f"Not ${player.money} exactly?!\n")
            print(f"DOUBLE IT")
            player.money*=2
            time.sleep(2)
            print(f"You see in Cups once you get ${bonus}, you have to double it!")
            time.sleep(1)
            print("Hey, i didnt make up the rules")
            time.sleep(3)
            print(f"Now after you receive the doubling bonus, you get one card. That card can be worth 100 dollars, which brings your total to $1500. Dont get too excited bc thats not going to happen unless you get the…\n")
            time.sleep(5)
            print("(Dealer draws card)")
            time.sleep(1)
            card = self.deck.drawCard()
            if type(card)==PostDoubleBonusCard:
                print("NO WAY\n")
                player.money+=100
            else:
                print(f"Nothin'!\n")
            card.printCard()
        return
    
    def checkSittingDownBonus(self):
        if self.sitBonusTurn==self.turnNumber:
            bonus = 700     #215
            answer = input("Are you sitting down? (y/n)\n")
            if "yes" in answer.lower()  or answer.lower().strip() == "y":
                self.players["Player"].money+=bonus
                print(F"{self.players['Player'].name} got an extra ${bonus} for sitting down!")
            else:
                print(f"Aw too bad")

    def checkGameEnd(self):
        return len(self.deck.cards) < 4

    def awaitPlayer(self, message):
        #just for mvp version
        command = input(f"{message}: ")
        return command
    
    def checkWinner(self):
        #only runs when the endgame condition is hit
        #trigger Player checks
        if self.players["Dealer"].money > self.players["Player"].money:
            print(f"Dealer wins with ${self.players['Dealer'].money}!")
        elif self.players["Dealer"].money < self.players["Player"].money:
            print(f"{self.players['Player'].name} wins with ${self.players['Player'].money}!")
        elif self.players["Dealer"].money == self.players["Player"].money:
            print(f"It's a tie at ${self.players['Dealer'].money}")
        else:
            print("I can't tell who won")                
        return

    def gameLoop(self):
        #start the game
        t1 = time.perf_counter()
        name = input("Let's Play Cups\n\n\n...\n\nBeginner's luck, very important in Cups\n\nWhat's your name?\n")
        self.createPlayers(playername=name)

        d = self.players["Dealer"]
        p = self.players["Player"]

        while not self.gameEnd:
            #start the round
            self.turnNumber+=1
            print(f"----------Turn #{self.turnNumber}----------")
            print(f"---Player: ${p.money}------Dealer: ${d.money}---")
            #deal hands
            self.dealToPlayers()


            d.printHand()
            p.printHand()
            
            command = input("Press any key to continue")

            #saucer card special condition
            if self.turnNumber==1:
                self.hasSaucerCard(player=p, dealer=d)

            #check hand to see if the hands meet any of the payout hands
            #first the special hands

            if not self.isDCup(player=p, dealer=d):
                if not self.isFullCup(player=p, dealer=d):
                    if not self.isHalfCup(player=p, dealer=d):
                        if self.isAlmostHalfCup(player=p, dealer=d):
                            if self.isCupInAPizzaBox(player=p, dealer=d):
                                if self.hasCupCard(player=p, dealer=d):
                                    if self.hasSaucerCard(player=p, dealer=d):
                                        print("Finished checking hands")
                                    else:
                                        print(f"Moving on")
                                else:
                                    print(f"Moving on")
                            else:
                                print(f"Moving on")
                        else:
                            print(f"Moving on")
                    else:
                        print(f"Moving on")
                else:
                    print(f"Moving on")
            else:
                print(f"Moving on")

            #check special events
            self.checkSittingDownBonus()
            self.doublingBonus(p)       #should be last since it should be triggered the same turn $700 is reached
            
            #finaly check if theres any cards left to continue the game
            if self.checkGameEnd():
                self.gameEnd = True
        self.checkWinner()
        t2 = time.perf_counter()
        mins, secs = divmod(t2-t1, 60)
        print(f"{int(mins)}:{int(secs):02d} of Cups")

# cc = CupCard()
# print(cc.facevalue)
g = GameManager()
g.gameLoop()