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
    hand1 = deck[0:26]
    hand2 = deck[26:]
    winnings1 = []
    winnings2 = []
    warpile = []
    currentWinner = None

    while (len(hand1) + len(winnings1) < 52) and (len(hand2) + len(winnings2) < 52):
        if len(hand1) == 0:
            hand1 = shuffle(winnings1, file)
            del winnings1[:]
        if len(hand2) == 0:
            hand2 = shuffle(winnings2, file)
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

    def trash(deck, file):
        turns = 0
        transitions = 0
        last = 0
        scores = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K':13}
        currentWinner = None
        arr1 = []
        arr2 = []
        discard = []

        discard.append(deck.pop())

        for x in range(10):
            arr1.append(deck.pop())
            arr2.append(deck.pop())
        seen1 = [False]*10
        seen2 = [False]*10

        hand = None

        print("OUTPUT trash", turns, transitions, last/turns)


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