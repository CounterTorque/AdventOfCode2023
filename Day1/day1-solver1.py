import os
import re

# Get the path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the file you want to open
file_path = os.path.join(current_dir, "input")

total = 0
acceptable_values = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "zero",
                     "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

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
}

with open(file_path, 'r') as file:
    for line in file:
        # from line, find in order, each word in acceptable_values

       # matches = [word for word in acceptable_values if word in line]

        #matches = [word for word in word_to_number for i, char in enumerate(line) if line[i:i+len(word)] == word]
        numbers = re.findall(r'\d+?', line)
        calValue = int(numbers[0] + numbers[-1])
        total += calValue
       

print(total)