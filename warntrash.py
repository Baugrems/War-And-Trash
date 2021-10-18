import sys
import random
random.seed("12345")

def shuffle(deck, file):
    try:
        c = 0
        n = len(deck)
        while(c < n - 1):
            r = float(file.readline().strip())
            # r = random.uniform(0,1)
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
        # print("Check need")
        if (False in self.seen) and value == 11:
            return True
        # print(value)
        if value > self.clear:
            return False
        for x in range(len(self.arr)):
            if x == value -1 and self.seen[x]:
                return False
        # print("Need a", value)
        return True

def getScore(p):
    c = p.clear
    count = 0
    for x in p.seen:
        if x == False:
            count += 1
    return (((c+1) * c) + (c - count))

def trash(file):
    turns = 0
    transitions = 0
    last = 0
    p1 = Player()
    p2 = Player()
    t = TrashGame(turns, transitions, last, p1, p2, file)
    t.start()
    #break out and # print results
    print("OUTPUT trash", t.turns, t.transitions, t.last/t.turns)

class TrashGame:
    def __init__(self, turns, transitions, last, p1, p2, file):
        self.deck = [1,2,3,4,5,6,7,8,9,10,11,12,13]*4
        self.p1 = p1
        self.p2 = p2
        self.turns = turns
        self.transitions = transitions
        self.last = last
        self.discard = []
        self.currentWinner = None
        self.file = file
        self.recurse = 0
        shuffle(self.deck, file)
        for x in range(10):
            self.p1.arr.append(self.deck.pop())
            self.p2.arr.append(self.deck.pop())

    def start(self):
        self.discard.append(self.deck.pop())
        while self.p1.clear > 0 and self.p2.clear > 0:
            self.turns += 1
            self.recuse = 0
            if not self.turn(self.p1):
                # print("p1 turn returned false")
                return
            # print("p1 turn over")
            self.turns += 1
            self.recurse = 0
            if not self.turn(self.p2):
                # print("p2 turn returned false")
                return
            # print("p2 turn over")

    def turn(self, p):
        self.recurse += 1
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
            elif not p.need(p.hand):
                # print("Discard unneeded")
                self.discard.append(p.hand)
                p.hand = None
                return True
            # print(p.hand)
            if p.hand != 11 and p.hand <= p.clear:
                r = p.arr[p.hand-1]
                p.arr[p.hand-1] = p.hand
                p.seen[p.hand - 1] = True
                p.hand = r
                # print("Picked up", p.hand)
                # print("Card placed")
                self.turn(p)
                return True
            elif p.hand != 11:
                self.discard.append(p.hand)
                # print("Face card discard, end turn: ", p.hand)
                p.hand = None
                return True
            else:
                spot = self.optJack(p)
                # print("Placing Jack at", spot)
                t = p.arr[spot]
                # print(t)
                p.arr[spot] = p.hand
                p.hand = t
                p.seen[spot] = True
                # print("In hand now:", p.hand)
                # print("Jack placed")
                self.turn(p)
                return True
        else:
            return False

    def optJack(self, p):
        count = [0]*p.clear
        most = 0
        for x in range(len(p.arr)):
            if p.seen[x]:
                continue
        if len(self.discard) > 0:
            for x in self.discard:
                if x < p.clear:
                    count[x] += 1
        for x in range(p.clear):
            if count[x] > most:
                if p.arr[x] == 11:
                    continue
                most = x
        if self.recurse > 200:
            return random.randint(0, p.clear)
        return most

    
    def checkGame(self, p):
        if len(self.deck) == 0:
            t = self.discard.pop()
            self.deck.extend(self.discard)
            self.deck = shuffle(self.deck, self.file)
            self.discard.append(t)
        if not False in p.seen:
            self.deck.extend(p.arr)
            t = self.discard.pop()
            self.deck.extend(self.discard)
            self.deck = shuffle(self.deck, self.file)
            self.discard.append(t)
            p.clear -= 1
            p.arr = []
            if p.clear != 0:
                # print("Array cleaned!")
                for x in range(p.clear):
                    p.arr.append(self.deck.pop())
                p.seen = [False] * p.clear
            else:
                # print("Game Over'")
                return False
        return True
        

    def checkWinner(self):
        s1 = getScore(self.p1)
        s2 = getScore(self.p2)
        if s1 < s2 and self.currentWinner != self.p1:
            self.transitions += 1
            self.last = self.turns
            self.currentWinner = self.p1
        elif s2 < s1 and self.currentWinner != self.p2:
            self.transitions += 1
            self.last = self.turns
            self.currentWinner = self.p2

def start(name, file):
    try:
        file = open(file)
    except IOError:
        sys.exit(1)
    if name == "war":
        deck = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']*4
        shuffle(deck, file)
        war(deck, file)
    elif name == "trash":
        trash(file)
    else:
        print("Please choose war or trash")
        sys.exit(1)