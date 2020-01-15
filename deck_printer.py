import json
from pprint import pprint
from collections import defaultdict
import operator

# investigator = "Lola Hayes"
top_x = 30

with open('decks.json','rt') as decks_read:
    decks = json.load(decks_read)
    investigators = []
    for row in decks:
        investigators.append(decks[row]["investigator"])
    
    investigators = list(set(investigators))

    print(len(investigators))
    investigators = list(filter(lambda x : x!="not loaded",investigators))
    print(len(investigators))

    for investigator in investigators:
        l = 0
        i = 0
        cards = []
        for row in decks:
            l += 1
            if decks[row]["investigator"] == investigator:
                i += 1
                cards += decks[row]["cards"]
        cards = [c["name"] for c in cards]
        card_frequency = defaultdict( int )
        for card in cards:
            card_frequency[card] += 1

        card_frequency = sorted(card_frequency.items(), key=lambda kv: -kv[1])
        j = 0
        print("out of",l,"decks")
        print()
        print("There are",i,"decks for",investigator)
        print("Their top",top_x,"cards are:")
        for card in card_frequency:
            print(card[0],":",card[1])
            j += 1
            if j > top_x:
                break
        
    # pprint(decks)