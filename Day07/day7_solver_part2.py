import os
import re
from collections import Counter

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

card_names = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

FIVE_OF_A_KIND = 6
FOUR_OF_A_KIND = 5
FULL_HOUSE = 4
THREE_OF_A_KIND = 3
TWO_PAIR = 2
ONE_PAIR = 1
HIGH_CARD = 0

def most_common_character(string):
    counter = Counter(string)
    most_common = counter.most_common(1)
    return most_common[0][0] if most_common else None


class Hand:
    def __init__(self, cards, bid):
        self.Cards = cards
        self.Hand = self.parse_cards(cards)
        self.bid = bid
        self.WildCards, self.WildHand = self.calculate_wild(cards, self.Hand)
        self.hand_type = self.calculate_hand_type()
   

    def parse_cards(self, cards):
        return [card_names.index(card) for card in cards]
    
    def calculate_wild(self, cards, hand):
        if not re.search(r'J', cards):
            return cards, hand
        
        best_card_letter = "A"
        if len(set(hand)) > 1:
            hand_sorted = sorted(hand)
            cards_sorted = [card_names[card_id] for card_id in hand_sorted if card_id != card_names.index("J")] 
            best_card_letter = most_common_character(cards_sorted)
        best_card_num = card_names.index(best_card_letter)

        card_adj = ""
        hand_adj = []
        for card_id in hand:
            if card_id == card_names.index("J"):
                card_adj += best_card_letter
                hand_adj.append(best_card_num)
            else:
                card_adj += card_names[card_id]
                hand_adj.append(card_id)


        return card_adj, hand_adj
   
    def calculate_hand_type(self):
        distinct_cards = set(self.WildHand)

        if len(distinct_cards) == 1: 
            return FIVE_OF_A_KIND
       
        if len(distinct_cards) == 2:
            count_card1 = len(re.findall(re.escape(self.WildCards[0]), self.WildCards))
            if count_card1 == 4 or count_card1 == 1:
                return FOUR_OF_A_KIND
                        
            return FULL_HOUSE

        if len(distinct_cards) == 3:
            count_card1 = len(re.findall(re.escape(self.WildCards[0]), self.WildCards))
            count_card2 = len(re.findall(re.escape(self.WildCards[1]), self.WildCards))
            count_card3 = len(re.findall(re.escape(self.WildCards[3]), self.WildCards))
            if count_card1 == 3 or count_card2 == 3 or count_card3 == 3:
                return THREE_OF_A_KIND

            return TWO_PAIR
        
        if len(distinct_cards) == 4:
            return ONE_PAIR
        
        return HIGH_CARD
    
    
    def __lt__(self, other):
        if(self.hand_type < other.hand_type):
            return True
        elif(self.hand_type > other.hand_type):
            return False
        else:
            for(card1, card2) in zip(self.Hand, other.Hand):
                if(card1 < card2):
                    return False
                elif(card1 > card2):
                    return True
                
    
    def __gt__(self, other):
        if(self.hand_type > other.hand_type):
            return True
        elif(self.hand_type < other.hand_type):
            return False
        else:
            for(card1, card2) in zip(self.Hand, other.Hand):
                if(card1 > card2):
                    return False
                elif(card1 < card2):
                    return True
    

def extract_data(file_path):
    hand_set = [] 
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            cards, bid = line.split(" ")
            hand = Hand(cards, bid)
            hand_set.append(hand)
            
    return hand_set
        
hand_set = extract_data(file_path)
# sort handset by rank and order
hand_set.sort()

winnings = 0
for idx, hand in enumerate(hand_set):
    if hand.Cards != hand.WildCards:
        print(str(idx) + ": " + hand.WildCards + " (" + hand.Cards + ")")
    else:
        print(str(idx) + ": " + hand.Cards)
    winnings += ((idx + 1) * int(hand.bid))

print(f"Part 2: {winnings}")
#part two: 251003917