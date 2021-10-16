import random

data = 0

def getTokens(inf):
    for lt in [line.split() for line in inf]:
        if not lt:
            continue
        for t in lt:
            yield t

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def show(self):
        print(self.value, "of", self.suit)

class Deck:
    def __init__(self):
        self.cards = []
        self.build()
        self.shuffle()

    def build(self):
        for s in ["Spades", "Clubs", "Hearts", "Diamonds"]:
            for x in range(2,15):
                self.cards.append(Card(s,x))

    def show(self):
        print("Deck Length:", len(self.cards))
        for card in self.cards:
            card.show()

    def shuffle(self):
        global data
        c = 0
        while c < len(self.cards) - 1:
            r = float(next(data))
            p = int(r * (len(self.cards) -c) + c)
            t = self.cards[c]
            self.cards[c] = self.cards[p]
            self.cards[p] = t
            c += 1

    def drawCard(self):
        return self.cards.pop()

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.winnings = Deck()
        del self.winnings.cards[:]

    def draw(self, deck):
        self.hand.append(deck.drawCard())
        return self

    def showHand(self):
        print("Player", self.name, "hand:")
        for card in self.hand:
            card.show()

    def useCard(self):
        return self.hand.pop() 
    
    def checkHand(self):
        if len(self.hand) > 0:
            return True
        if len(self.winnings.cards) > 0:
            self.winnings.shuffle()
            self.hand.extend(self.winnings.cards)
            del self.winnings.cards[:]
            return True
        return False

class WarGame:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.transCount = 0
        self.currentWinner = None
        self.turns = 0
        self.lastTrans = 0
        self.data = data
    
    def checkWinner(self):
        if self.currentWinner == self.p1:
            if len(self.p2.hand) + len(self.p2.winnings.cards) > len(self.p1.hand) + len(self.p1.winnings.cards):
                self.currentWinner = self.p2
                self.transCount +=1
                self.lastTrans = self.turns
        else:
            if len(self.p2.hand) + len(self.p2.winnings.cards) < len(self.p1.hand) + len(self.p1.winnings.cards):
                self.currentWinner = self.p1
                self.transCount +=1
                self.lastTrans=self.turns
            else:
                self.currentWinner = self.p2
                self.transCount +=1
                self.lastTrans=self.turns


    def nextTurn(self):
        self.turns += 1
        a = self.p1.useCard()
        b = self.p2.useCard()
        pot = [a,b]
        while (a.value == b.value):
            if not(self.p1.checkHand()):
                return
            if not(self.p2.checkHand()):
                return
            a = self.p1.useCard()
            b = self.p2.useCard()
            pot.append(a)
            pot.append(b)
        if(a.value > b.value):
            self.p1.winnings.cards.extend(pot)
        else:
            self.p2.winnings.cards.extend(pot)
        if not(self.p1.checkHand()):
            return
        if not(self.p2.checkHand()):
            return
def start(file):
    global data
    data = open(file)
    data = iter(getTokens(data))
    d = Deck()
    p1 = Player("One")
    p2 = Player("Two")
    for x in range(1,27):
        p1.draw(d)
        p2.draw(d)
    war = WarGame(p1,p2)
    while len(p1.hand) > 0 and len(p2.hand) > 0:
        war.nextTurn()
        war.checkWinner()


    print("OUTPUT war turns", war.turns, "Transitions", war.transCount, "Last: ", war.lastTrans / war.turns)
