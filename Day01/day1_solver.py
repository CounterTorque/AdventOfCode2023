import os
import re

# Get the path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the file you want to open
file_path = os.path.join(current_dir, "input.txt")

total = 0

with open(file_path, 'r') as file:
    for line in file:
        # Parse each line here
        numbers = re.findall(r'\d+?', line)
        calValue = int(numbers[0] + numbers[-1])
        total += calValue


print(total) #54990