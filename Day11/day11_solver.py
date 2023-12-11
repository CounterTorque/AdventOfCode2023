import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

def extract_data(file_path: str) -> [[]]:
     galaxy_map = []
    
     with open(file_path, 'r') as file:
          lines = file.readlines()
          char_list = [list(line.strip()) for line in lines]

          for y in range(len(char_list)):
               galaxy_map.append([])
               for x in range(len(char_list[y])):
                    char = char_list[y][x]
                    galaxy_map[y].append(char)


     return galaxy_map

def expand_map(galaxy_map: [[]]) -> [[]]:
     #todo for each line and column that is only '.' expand the map down or right
     return

def find_locations(galaxy_map: [[]]) -> [()]:
     #todo find each non '.' and return a tuple of its (y, x) location
     return

def find_distance(galaxy_locations: [()], galaxy_map: [[]]) -> int:
     return
         
galaxy_map = extract_data(file_path)
galaxy_map = expand_map(galaxy_map)
galaxy_locations = find_locations(galaxy_map)
total_distance = find_distance(galaxy_locations, galaxy_map)

print("Part 1: " + str(total_distance))


