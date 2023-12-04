import os
import re

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

class ScratchCard:
    def __init__(self, card_number, winning_numbers, shown_numbers):
        self.CardNumber = card_number
        self.Copies = 1
        self.WinningNumbers = winning_numbers
        self.ShownNumbers = shown_numbers
        self.CountMatches = 0
        self.CardPoints = 0




def build(file_path): 
    scratch_cards = []

    with open(file_path, 'r') as file:
        for idx, line in enumerate(file):
            _, number_sets = line.strip().split(':')
            winning_numbers, shown_numbers = number_sets.split('|')
            winning_numbers = winning_numbers.strip()
            shown_numbers = shown_numbers.strip()

            scratch_card = ScratchCard(idx, 
                                       re.findall(r'\d+', winning_numbers), 
                                       re.findall(r'\d+', shown_numbers)
            )
           
            scratch_cards.append(scratch_card)
    
    return scratch_cards


def check_cards_for_matches(scratch_cards):
    for scratch_card in scratch_cards:
        for shown_number in scratch_card.ShownNumbers:
            if shown_number in scratch_card.WinningNumbers:
                scratch_card.CountMatches += 1


def generate_points_and_copies(scratch_cards):
    total_score = 0
    for scratch_card in scratch_cards:
        if scratch_card.CountMatches == 0:
            continue

        scratch_card.CardPoints = 2 ** (scratch_card.CountMatches-1)
        total_score += scratch_card.CardPoints

        copy_count = scratch_card.Copies
        for i in range(scratch_card.CountMatches):
            next_card_number = scratch_card.CardNumber + i + 1
            if next_card_number >= len(scratch_cards):
                break
            scratch_cards[next_card_number].Copies += copy_count

    print(total_score)
    #17803 Part 1


def count_copies(scratch_cards):
    total_copies = 0
    for scratch_card in scratch_cards:
        total_copies += scratch_card.Copies
    print(total_copies)
    #5554894 Part 2

scratch_cards = build(file_path)
check_cards_for_matches(scratch_cards)
generate_points_and_copies(scratch_cards)
count_copies(scratch_cards)

