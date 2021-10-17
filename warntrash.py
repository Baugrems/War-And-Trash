import sys

def shuffle(deck, file):
    try:
        c = 0
        n = len(deck)
        while(c < n - 1):
            r = float(file.readline().strip())
            p = int(r * (n-c) + c)
            t = deck[p]
            deck[p] = deck[c]
            deck[c] = t
            c += 1
    except IndexError:
        print("End of file of randoms")
        sys.exit(1)
    return deck

def war(deck, file):
    turns = 0
    last = 0
    transitions = 0
    scores = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K':13, 'A':14}
    hand1 = []
    hand2 = []
    for x in range(26):
        hand1.append(deck.pop())
    for x in range(26):
        hand2.append(deck.pop())
    winnings1 = []
    winnings2 = []
    warpile = []
    currentWinner = None

    while (len(hand1) + len(winnings1) < 52) and (len(hand2) + len(winnings2) < 52):
        if len(hand1) == 0:
            hand1.extend(winnings1)
            shuffle(hand1, file)
            del winnings1[:]
        if len(hand2) == 0:
            hand2.extend(winnings2)
            shuffle(hand2, file)
            del winnings2[:]
        card1 = hand1.pop()
        card2 = hand2.pop()

        warpile.append(card1)
        warpile.append(card2)

        if card1 == card2:
            if len(hand1) + len(winnings1) == 0:
                winnings2.extend(warpile)
                del warpile[:]
            elif len(hand2) + len(winnings2) == 0:
                winnings1.extend(warpile)
                del warpile[:]
            else:
                continue
        elif scores[card1] > scores[card2]:
            winnings1.extend(warpile)
            del warpile[:]
        elif scores[card1] < scores[card2]:
            winnings2.extend(warpile)
            del warpile[:]
        turns += 1
        if len(hand1) + len(winnings1) > len(hand2) + len(winnings2):
            if currentWinner != 1:
                transitions += 1
                currentWinner = 1
                last = turns
        elif len(hand1) + len(winnings1) < len(hand2) + len(winnings2):
            if currentWinner != 2:
                transitions += 1
                currentWinner = 2
                last = turns
    print("OUTPUT war", turns, transitions, last/turns)

### Stuff for trash, more complex, need classes

class Player:
    def __init__(self):
        self.hand = None
        self.clear = 10
        self.seen = [False]*10
        self.arr = []


    def need(self,value):
        if (False in self.seen) and value == 11:
            return True
        for x in self.seen:
            if value == x:
                return False
        return True

def getScore(p):
    c = p.clear
    count = 0
    for x in p.seen:
        if x == False:
            count += 1
    return (((c+1) * c) + (c - count))

def trash(deck, file):
    turns = 0
    transitions = 0
    last = 0
    p1 = Player()
    p2 = Player()
    for x in range(10):
        p1.arr.append(deck.pop())
        p2.arr.append(deck.pop())
    t = TrashGame(turns, transitions, last, deck, p1, p2)
    t.start()
    #break out and print results
    print("OUTPUT trash", t.turns, t.transitions, t.last/t.turns)

class TrashGame:
    def __init__(self, turns, transitions, last, deck, p1, p2):
        self.scores = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K':13}
        self.p1 = p1
        self.p2 = p2
        self.turns = turns
        self.transitions = transitions
        self.last = last
        self.deck = deck
        self.discard = []
        self.currentWinner = None

    def start(self):
        self.discard = self.deck.pop()
        while self.p1.clear > 0 and self.p2.clear > 0:
            self.turns += 1
            if not self.turn(self.p1):
                return
            self.turns += 1
            if not self.turn(self.p2):
                return

    def turn(self, p):
        self.checkWinner()
        if self.checkGame(p):
            if p.hand == None:
                if len(self.discard) > 0 and p.need(self.discard[-1]):
                    p.hand = self.discard.pop()
                else:
                    p.hand = self.deck.pop()
                    if not p.need(p.hand):
                        self.discard.append(p.hand)
                        p.hand = None
                        return True
            if p.hand != 11:
                r = p.arr[p.hand-1]
                p.arr[p.hand-1] = p.hand
                p.seen[p.hhand - 1] = True
                p.hand = r
                self.turn(p)
            else:
                spot = self.optJack(p)
                t = p.arr[spot]
                p.arr[spot] = p.hand
                p.hand = t
                self.turn(p)
        else:
            return False

    def optJack(self, p):
        least = 99
        count = [0]*p.clear
        for x in p.seen:
            if p.seen[x]:
                count[x] += 1
        for c in count:
            if c < least:
                least = c
        return least

    
    def checkGame(self, p):
        if len(self.deck) == 0:
            t = self.discard.pop()
            self.deck.append(self.discard)
            self.deck = shuffle(self.deck)
            self.discard.append(t)
        if not False in p.seen:
            self.deck.append(p.arr)
            t = self.discard.pop()
            self.deck.append(self.discard)
            self.deck = shuffle(self.deck)
            self.discard.append(t)
            p.clear -= 1
            if p.clear != 0:
                for x in range(p.clear):
                    p.arr.append(self.deck.pop())
                p.seen = [False] * p.clear
            else:
                return False
        

    def checkWinner(self):
        s1 = getScore(self.p1)
        s2 = getScore(self.p2)
        if s1 < s2 and self.currentWinner == self.p2:
            self.transitions += 1
            self.last = self.turns
            self.currentWinner = self.p1
        elif s2 < s1 and self.currentWinner == self.p1:
            self.transitions += 1
            self.last = self.turns
            self.currentWinner = self.p2

def start(name, file):
    try:
        file = open(file)
    except IOError:
        sys.exit(1)
    deck = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']*4
    shuffle(deck, file)
    if name == "war":
        war(deck, file)
    elif name == "trash":
        trash(deck, file)
    else:
        print("Please choose war or trash")
        sys.exit(1)