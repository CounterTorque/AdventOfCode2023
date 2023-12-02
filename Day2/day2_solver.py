import os
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "input")

max_red = 12
max_green = 13
max_blue = 14

#for each line in input
#parse the line into a dictionary of game ids and its list of sets of colors

# Create an empty dictionary to store game ids and their sets of colors
game_dict = {}

def parse_color_group(group):
    # Split the group into values without regard to order delimited by comma
    values = group.split(',')

    # Then split them into number and name delimited by space
    color_dict = {}
    for value in values:
        value = value.strip()
        count, color_name = value.split(' ')
        color_dict[color_name] = count

    #now find which color_name is red, green, and blue, if any
    r = color_dict.get('red', 0)
    g = color_dict.get('green', 0)
    b = color_dict.get('blue', 0)

    return int(r), int(g), int(b)

# Open the input file and iterate over each line
def parse_line(color_groups):
    color_sets = []

    # Split the color_groups into a list of sets
    for group in color_groups.split(';'):
        group = group.strip()

        r, g, b = parse_color_group(group)
        color_set = [r, g, b]
        color_sets.append(color_set)

    return color_sets

def validate(color_sets):
    for color_set in color_sets:
        if ((color_set[0] > max_red) or
            (color_set[1] > max_green) or
            (color_set[2] > max_blue)):
            return False
    
    return True

def build(file_path):
    with open(file_path, 'r') as file:
        for idx, line in enumerate(file, start=1):
            # Parse the line into game id and colors
            game_id, color_groups = line.strip().split(':')
            # Add the game id and color sets to the dictionary
            game_dict[idx] = parse_line(color_groups)



def solve_part1(game_dict):
    sum_possible = 0
    for idx, __ in enumerate(game_dict, start=1):
        line_possible = validate(game_dict[idx])

        if line_possible:
            sum_possible += idx

    print(f"Total valid games: {sum_possible}")
    return sum_possible
    
def solve_part2(game_dict):

    sum_of_powers = 0
    for color_sets in game_dict.values():
        cur_max_red = 0
        cur_max_green = 0
        cur_max_blue = 0
        for color_set in color_sets:
            if color_set[0] > cur_max_red:
                cur_max_red = color_set[0]
            if color_set[1] > cur_max_green:
                cur_max_green = color_set[1]
            if color_set[2] > cur_max_blue:
                cur_max_blue = color_set[2]

        #assuming no 0s in the game sets
        sum_of_powers += (cur_max_red * cur_max_green * cur_max_blue)
    
    print(f"Total sum of powers: {sum_of_powers}")
    return sum_of_powers


build(file_path)
solve_part1(game_dict)
solve_part2(game_dict)


