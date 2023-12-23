import os
import heapq

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

FOREST = '#'
PATH = '.'
directions = {
     "S": (1, 0),
     "N": (-1, 0),     
     "E": (0, 1),
     "W": (0, -1)
}

def extract_data(file_path):
     hiking_map = []
     with open(file_path, 'r') as file:
          lines = file.readlines()
          char_list = [list(line.strip()) for line in lines]

          for y in range(len(char_list)):
               hiking_map.append([])
               for x in range(len(char_list[y])):
                    char = char_list[y][x]  
                    if (char in ["^", "v", "<", ">"]):
                         char = PATH
                    hiking_map[y].append(char)

     return hiking_map
          
         
def  find_start_and_end(heat_map):
     start = (0, 0)
     end = (0, 0)
     y_max = len(heat_map)
     for x in range(len(heat_map[0])):
          if heat_map[0][x] == PATH:
               start = (0, x)
          
          if (heat_map[y_max - 1][x] == PATH):
               end = (y_max - 1, x)
     
     return start, end


def walk_map(hiking_map, start, end):
     
     longest_path = 0
     path_q = [(1, [start])]

     while path_q:
          cur_len, cur_path = heapq.heappop(path_q)

          tail_pos = cur_path[-1]
          if (tail_pos[0] == end[0]) and (tail_pos[1] == end[1]):
               if cur_len > longest_path:
                    longest_path = cur_len
                    print(f"Cur Longest: {longest_path-1}")
               continue
          
          for direction in directions:
               new_pos = (tail_pos[0] + directions[direction][0], tail_pos[1] + directions[direction][1])
               if new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0] >= len(hiking_map) or new_pos[1] >= len(hiking_map[0]):
                    continue

               #todo handle not allowing onto path we've already taken
               if new_pos in cur_path:
                    continue

               if hiking_map[new_pos[0]][new_pos[1]] == FOREST:
                    continue
                    
               new_path = cur_path[:]
               new_path.append(new_pos)
               heapq.heappush(path_q, (cur_len + 1, new_path))

   
     return longest_path - 1


def print_map(map):
     output_path = os.path.join(base_dir, "output.txt")
     with open(output_path, 'w') as output_file:
          for row in map:
               for tile in row:
                    output_file.write(tile + ",")
                    output_file.flush()
               output_file.write('\n')

hiking_map = extract_data(file_path)
start, end = find_start_and_end(hiking_map)
path_length = walk_map(hiking_map, start, end)

print(f"Part 2: {path_length}") #


