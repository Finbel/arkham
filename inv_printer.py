import json
from pprint import pprint
from collections import defaultdict
from datetime import datetime
import operator

# investigator = "Lola Hayes"
top_x = 15

start_date = datetime.strptime("2017-01-31","%Y-%m-%d")

with open('decks.json','rt') as decks_read:
    decks = json.load(decks_read)
    investigators = []
    for row in decks:
        investigators.append(decks[row]["investigator"])
    investigators = list(filter(lambda x : x!="not loaded",list(set(investigators))))

    inv_dict = {}
    s = 0 
    for investigator in investigators:
        i = 0
        for row in decks:
            right_name = decks[row]["investigator"] == investigator
            if right_name:
                date = datetime.strptime(decks[row]["published"],"%Y-%m-%d")
                right_time = date < start_date
                if right_time:
                    i += 1
        if i > s:
            s = i
        inv_dict[investigator] = i
    inv_dict = sorted(inv_dict.items(), key=lambda kv: -kv[1])        
    
    for investigator in inv_dict:
        if(len(investigator[0])>13):
            tabs = "\t"
        else:
            tabs = "\t\t"
        print(investigator[0],":"+tabs,investigator[1],",\t",str(round(investigator[1]/s*100)) +"%")
    
