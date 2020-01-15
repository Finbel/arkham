import json
from collections import defaultdict
from pprint import pprint

cards = ["Unexpected Courage","Perception","Guts","Manual Dexterity","Overpower"]

with open('decks.json','rt') as decks_read:
    decks = json.load(decks_read)
    allcards = []
    for row in decks:
        allcards += decks[row]["cards"]
    print(len(allcards))
    allcards = list(filter(lambda x : not isinstance(x, str),allcards))
    print(len(allcards))

    filtered = []
    for card in allcards:
        if card['name'] in cards:
            filtered.append(card['name'])
    card_frequency = defaultdict( int )
    for card in filtered:
        card_frequency[card] += 1
    pprint(card_frequency)