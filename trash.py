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
        c = 0
        while c < len(self.cards) - 1:
            r = random.uniform(0,1)
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



def start(file):
	pass
