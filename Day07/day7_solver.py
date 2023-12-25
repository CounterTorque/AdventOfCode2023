import os
import re

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

card_names = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
FIVE_OF_A_KIND = 6
FOUR_OF_A_KIND = 5
FULL_HOUSE = 4
THREE_OF_A_KIND = 3
TWO_PAIR = 2
ONE_PAIR = 1
HIGH_CARD = 0


class Hand:
    def __init__(self, cards, bid):
        self.Cards = cards
        self.Hand = self.parse_cards(cards)
        self.bid = bid
        self.rank = self.calculate_rank()


    def parse_cards(self, cards):
        return [card_names.index(card) for card in cards]
    
   
    def calculate_rank(self):
        distinct_cards = set(self.Hand)
        if (len(distinct_cards) == 1): 
            return FIVE_OF_A_KIND
       
        if (len(distinct_cards) == 2):
            count_card1 = len(re.findall(re.escape(self.Cards[0]), self.Cards))
            if (count_card1 == 4 or count_card1 == 1):
                return FOUR_OF_A_KIND
                        
            return FULL_HOUSE

        if (len(distinct_cards) == 3):
            count_card1 = len(re.findall(re.escape(self.Cards[0]), self.Cards))
            count_card2 = len(re.findall(re.escape(self.Cards[1]), self.Cards))
            count_card3 = len(re.findall(re.escape(self.Cards[3]), self.Cards))
            if (count_card1 == 3 or count_card2 == 3 or count_card3 == 3):
                return THREE_OF_A_KIND

            return TWO_PAIR
        
        if (len(distinct_cards) == 4):
            return ONE_PAIR
        
        return HIGH_CARD
    
    
    def __lt__(self, other):
        if(self.rank < other.rank):
            return True
        elif(self.rank > other.rank):
            return False
        else:
            for(card1, card2) in zip(self.Hand, other.Hand):
                if(card1 < card2):
                    return False
                elif(card1 > card2):
                    return True
                
    
    def __gt__(self, other):
        if(self.rank > other.rank):
            return True
        elif(self.rank < other.rank):
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
    winnings += ((idx + 1) * int(hand.bid))

print(f"Part 1: {winnings}")