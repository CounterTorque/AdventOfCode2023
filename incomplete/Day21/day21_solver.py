import os
from collections import deque

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

directions = {
     "U": (0, -1),
     "D": (0, 1),
     "R": (1, 0),
     "L": (-1, 0)
}

PLOT = '.'
ROCK = '#'
WALKED = 'O'

def extract_data(file_path):
     garden_map = []
     start = (0, 0)
     with open(file_path, 'r') as file:
          lines = file.readlines()
          char_list = [list(line.strip()) for line in lines]

          for y in range(len(char_list)):
               garden_map.append([])
               for x in range(len(char_list[y])):
                    char = char_list[y][x]
                    if char == 'S':
                         start = (y, x)
                         #replace with ground to simplify later
                         char = PLOT
                    garden_map[y].append(char)

     return garden_map, start


def walk_map(garden_map, start, steps):

     rows = len(garden_map)
     cols = len(garden_map[0])

     walked_locations = []
     #starting with the start we need to look at the surounding tiles
     walk_q = deque()
     walk_q.append(start)

     #iterate the map the number of steps
     for i in range(steps):
          #for any walked_locations, add them to the walk_q
          for location in walked_locations:
              garden_map[location[0]][location[1]] = PLOT
              walk_q.append(location)
          
          walked_locations = []

          while bool(walk_q):
               location = walk_q.pop()
               y, x = location

               for dir in directions.keys():
                    new_y = y + directions[dir][0]
                    new_x = x + directions[dir][1]

                    if 0 <= new_y < rows and 0 <= new_x < cols:
                         if garden_map[new_y][new_x] == PLOT:
                              garden_map[new_y][new_x] = WALKED
                              walked_locations.append((new_y, new_x))
     
     return walked_locations


def sum_map(garden_map):
     total = 0
     for row in garden_map:
          for tile in row:
               if tile == WALKED:
                    total += 1

     return total


garden_map, start = extract_data(file_path)
walk_map(garden_map, start, 64)
total = sum_map(garden_map)

print(f"Part 1: {total}") # 3729

