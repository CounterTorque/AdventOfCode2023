import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")



def extract_data(file_path) -> [[]]:
    mirror_map = []
    with open(file_path, 'r') as file:
          lines = file.readlines()
          char_list = [list(line.strip()) for line in lines]

          for y in range(len(char_list)):
               mirror_map.append([])
               for x in range(len(char_list[y])):
                    char = char_list[y][x]                           
                    mirror_map[y].append(char) 

    return mirror_map

def tilt_map(mirror_map, y_dir):
     had_movement = False
     for y in range(len(mirror_map)):
          for x in range(len(mirror_map[0])):
               if mirror_map[y][x] == "O":
                    if (y-1) >=0 and mirror_map[y-1][x] == ".":
                         mirror_map[y-1][x] = "O"
                         mirror_map[y][x] = "."
                         had_movement = True

     return had_movement

def tilt_map_distance(mirror_map, y_dir, y_max):
     for _ in range(y_max):
          had_movement = tilt_map(mirror_map, y_dir)
          if not had_movement:
               break

         
def calculate_load(mirror_map):
     total_load = 0
     y_max = len(mirror_map)
     for y in range(y_max):
          for x in range(len(mirror_map[0])):
               if mirror_map[y][x] == "O":
                    total_load += y_max - y

     return total_load


mirror_map = extract_data(file_path)
y_max = len(mirror_map)
tilt_map_distance(mirror_map, -1, y_max)
total_load = calculate_load(mirror_map)

print(f"Part 1: {total_load}") #108889

