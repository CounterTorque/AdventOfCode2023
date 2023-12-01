import os
import re

# Get the path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "input")

word_to_number = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "zero": 0,
    "1": 1,
    "2": 2,
    "3": 3, 
    "4": 4, 
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8, 
    "9": 9, 
    "0": 0
}

def find_all_occurrences(word, string):
    indices = [match.start() for match in re.finditer(word, string)]
    return indices

def find_matching_values(inputline, search_values):
    colatedValues = []  

    colatedValues = [(curSearchValue, index)
                    for curSearchValue in search_values
                    for index in find_all_occurrences(curSearchValue, inputline)]
                     
                     
    return colatedValues

def join_first_last_numeric(line):
    matching_values = find_matching_values(line, word_to_number.keys())
    if(len(matching_values) == 0):
        return 0
    
    sorted_values = sorted(matching_values, key=lambda x: x[1])
    numeric_values = [word_to_number[value[0]] for value in sorted_values]
            
    joined_two_digit = str(numeric_values[0]) + str(numeric_values[-1])
    calValue = int(joined_two_digit)
    return calValue

def solve():
    total = 0
    with open(file_path, 'r') as file:
        for line in file:
            calValue = join_first_last_numeric(line)
            total += calValue
    
    return total
      

print(solve())