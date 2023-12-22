import os
from collections import deque
import copy


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

def expand_map(garden_map, start):
     rows = len(garden_map)
     cols = len(garden_map[0])

     start = (start[0] + rows + rows, start[1] + cols + cols)

     #expand the map
     for i in range(rows):
          row = garden_map[i]
          row = row + row + row + row + row
          garden_map[i] = row

     for i in range(rows):
          new_row = copy.deepcopy(garden_map[i])
          garden_map.append(new_row)

     for i in range(rows):
          new_row = copy.deepcopy(garden_map[i])
          garden_map.append(new_row)

     for i in range(rows):
          new_row = copy.deepcopy(garden_map[i])
          garden_map.append(new_row)

     for i in range(rows):
          new_row = copy.deepcopy(garden_map[i])
          garden_map.append(new_row)
          
     return start


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


def print_map(map):
     output_path = os.path.join(base_dir, "output.txt")
     with open(output_path, 'w') as output_file:
          for row in map:
               for tile in row:
                    output_file.write(tile)
                    output_file.flush()
               output_file.write('\n')

garden_map, start = extract_data(file_path)
start = expand_map(garden_map, start)
walk_map(garden_map, start, 10)
total = sum_map(garden_map)
print_map(garden_map)

print(f"Part 2: {total}")
#10 = 101
#20 = 379
#30 = 826
#40 = 1441
#50 = 2243
#100 = 9067
#150 = 20103
#200 = 35837
#250 = 55788
#300 = 79934

#a=1053/1250
#a=17327/20000
a=.885
#b=253/25
#b=1559/200
b=10
#c=-369
c=0

t_50 = a*(50**2) + b*50 + c

print(t_50)

t_26501365 = a*(26501365**2) + b*26501365 + c
print(t_26501365)

#591636613191026 #to low
#621289922886149 Answer