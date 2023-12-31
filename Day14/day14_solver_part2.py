import os
import hashlib

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


def tilt_map_v(mirror_map, y_dir):
     had_movement = False
     rows = len(mirror_map)
     cols = len(mirror_map[0])
     for y in range(rows):
          for x in range(cols):
               if mirror_map[y][x] == "O":
                    y_next = y+y_dir
                    if 0 <= y_next < rows and mirror_map[y_next][x] == ".":
                         mirror_map[y][x], mirror_map[y_next][x] = ".","O"
                         had_movement = True

     return had_movement

def tilt_map_h(mirror_map, x_dir):
     had_movement = False
     rows = len(mirror_map)
     cols = len(mirror_map[0])
     for y in range(rows):
          for x in range(cols):
               if mirror_map[y][x] == "O":
                    x_next = x+x_dir
                    if 0 <=x_next < cols and mirror_map[y][x_next] == ".":
                         mirror_map[y][x], mirror_map[y][x_next] = ".","O"
                         had_movement = True

     return had_movement

def tilt_map_vertical(mirror_map, y_dir, y_max):
     for _ in range(y_max):
          if not tilt_map_v(mirror_map, y_dir):
               break


def tilt_map_horizontal(mirror_map, x_dir, x_max):
     for _ in range(x_max):
          if not tilt_map_h(mirror_map, x_dir):
               break

         
def calculate_load(mirror_map):
     total_load = 0
     y_max = len(mirror_map)
     for y in range(y_max):
          for x in range(len(mirror_map[0])):
               if mirror_map[y][x] == "O":
                    total_load += y_max - y

     return total_load


def hash_mirrors(mirror_map):
     str_hash = ""
     for sub_map in mirror_map:
           str_hash += ''.join(sub_map)

     return hashlib.md5(str_hash.encode('utf-8')).hexdigest()


mirror_map = extract_data(file_path)

def spin_cycle(mirror_map, cycle_stop):

     cycle = 0
     y_max = len(mirror_map)
     x_max = len(mirror_map[0])
    
     cache = {}
     start_hash = hash_mirrors(mirror_map)
     cache[start_hash] = 0
     do_cache = True

     while cycle < cycle_stop:

          tilt_map_vertical(mirror_map, -1, y_max)         
          tilt_map_horizontal(mirror_map, -1, x_max)                   
          tilt_map_vertical(mirror_map, 1, y_max)                    
          tilt_map_horizontal(mirror_map, 1, x_max)
          
          cycle += 1    
          if do_cache:
               hash_val = hash_mirrors(mirror_map)
               if hash_val in cache:
                    cycle_head = cache[hash_val]
                    cycle_size = cycle - cycle_head
                    cycle = cycle_stop - ((cycle_stop - cycle_head) % cycle_size)
                    do_cache = False

               cache[hash_val] = cycle      
     

#part 2 104671
cycle_stop = 1000000000
spin_cycle(mirror_map, cycle_stop)

total_load = calculate_load(mirror_map)

print(f"Part 2: {total_load}")

