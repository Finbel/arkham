from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException

from pprint import pprint
import csv
import time
import json

option = webdriver.ChromeOptions()
option.add_argument(" — incognito")

def crawlDeck(url):
    browser = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=option)
    # Wait 10 seconds for page to load
    timeout = 10
    try:
        print("loading:",url)
        browser.get(url)
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(@class, 'card')]")))
        # find_elements_by_xpath returns an array of selenium objects.
        cards_outer = browser.find_elements_by_xpath("//a[contains(@class, 'card')]/..")
        cards_raw = [card.text for card in cards_outer]
        cards_inner = browser.find_elements_by_xpath("//a[contains(@class, 'card')]")
        cards_href = [card.get_attribute("href") for card in cards_inner]
        published = browser.find_elements_by_xpath("//time")[0].get_attribute("datetime")[:10]
        investigator = cards_raw[0]
        cards = []
        for i in range(len(cards_raw)):
            if len(cards_raw[i]) > 0:
                card_text = cards_raw[i][0]
                if card_text == "1" or card_text == "2":
                    card_count = int(cards_raw[i][0])
                    card_name = cards_raw[i][3:]
                    card_name = card_name.strip()
                    card_id = cards_href[i][-5:]
                    for j in range(card_count):
                        card = {
                            "name" : card_name,
                            "id" : card_id
                        }
                        cards.append(card)
        deck = {
            "investigator" : investigator,
            "published" : published,
            "cards" : cards
        }
        browser.quit()
        return deck
    except TimeoutException:
        print()
        print(url)
        print("Timed out waiting for page to load")
        print()
        browser.quit()
        return None

end = 4250

with open('decks.json','rt') as decks_read:
    decks = json.load(decks_read)
    with open('decks.csv', 'rt') as csvfile:
        urls_file = csv.DictReader(csvfile)
        i = 0
        for row in urls_file:
            if row["deckurl"][:5] == "https":
                deck_id = row["deckurl"][35:].split('/')[0]
                if not deck_id in decks:
                    deck = crawlDeck(row["deckurl"])
                    time.sleep(0.5)
                    if deck != None:
                        decks[deck_id] = deck
                    else:
                        decks[deck_id] = {
                            "investigator" : "not loaded",
                            "published" : "not loaded",
                            "cards" : "not loaded"
                            }
                    i += 1
                    print(100*"\n"+ str(round(i/end,3))+"% left"+10*"\n")
                else:
                    end -= 1
            if i > end:
                break
    with open('decks.json','wt') as decks_file:
        json.dump(decks, decks_file)