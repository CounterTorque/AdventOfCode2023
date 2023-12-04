import os
import re

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

class ScratchCard:
    CardNumber = 0
    WinningNumbers = []
    ShownNumbers = []
    CountMatches = 0

scratch_cards = []

def build(file_path):    
    with open(file_path, 'r') as file:
        for idx, line in enumerate(file):
            _, number_sets = line.strip().split(':')
            winning_numbers, shown_numbers = number_sets.split('|')
            winning_numbers = winning_numbers.strip()
            shown_numbers = shown_numbers.strip()

            scratch_card = ScratchCard()
            scratch_card.CardNumber = idx
            scratch_card.WinningNumbers = re.findall(r'\d+', winning_numbers)
            scratch_card.ShownNumbers = re.findall(r'\d+', shown_numbers)

            scratch_cards.append(scratch_card)


def check_cards_for_matches(scractch_cards):
    for scratch_card in scratch_cards:
        for shown_number in scratch_card.ShownNumbers:
            if shown_number in scratch_card.WinningNumbers:
                scratch_card.CountMatches += 1


def generate_scores(scratch_cards):
    total_score = 0
    for scratch_card in scratch_cards:
        if (scratch_card.CountMatches == 0):
            continue

        card_score = 2**(scratch_card.CountMatches-1)
        total_score += card_score

    print(total_score)


build(file_path)
check_cards_for_matches(scratch_cards)
generate_scores(scratch_cards)


