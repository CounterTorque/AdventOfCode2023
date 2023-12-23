import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

FOREST = '#'
PATH = '.'
directions = {
     "N": (-1, 0),
     "S": (1, 0),
     "E": (0, 1),
     "W": (0, -1)
}
slopes = {
     "^": "N",
     "v": "S",
     ">": "E",
     "<": "W"
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
                    hiking_map[y].append(int(char))

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
     #for each possible direction, check if we can move in that direction
     #keep a list of the locations we have visited (so start with the start location)
     #if we can move in more than one direction, make a duplicate branch. 
     #if we ever deadend, kill the branch
     #once we reach the end, return the distance
     #take the highest distance
     pass


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

print(f"Part 1: {path_length}")


