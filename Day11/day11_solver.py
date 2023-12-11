import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")
# Part 1 = 1
#expansion_size = 1

# Part 2 = 1000000
expansion_size = 1000000 - 1

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


def count_expansions(dim_expansions: [], start: int, end: int) -> int:
     if (start > end):
          start, end = end, start

     count = len([i for i in dim_expansions if start < i < end])
     return count


def get_x_expansions(galaxy_map: [[]]) -> []:
     x_expansions = []
     for x in range(len(galaxy_map[0])):
          if all(row[x] == "." for row in galaxy_map):
               x_expansions.append(x) 

     return x_expansions


def get_y_expansions(galaxy_map: [[]]) -> []:
     y_expansions = []
     for y in range(len(galaxy_map)):
          if all(item == "." for item in galaxy_map[y]):
               y_expansions.append(y) 

     return y_expansions


def find_locations(galaxy_map: [[]]) -> [()]:
     locations = []
     for y in range(len(galaxy_map)):
          for x in range(len(galaxy_map[y])):
               if galaxy_map[y][x] != ".":
                    locations.append((y, x))

     return locations

def find_distance(galaxy_locations: [()], galaxy_map: [[]]) -> int:
     distance_total = 0
     x_expansions = get_x_expansions(galaxy_map)
     y_expansions = get_y_expansions(galaxy_map)

     for index_location in range(len(galaxy_locations)):
          source_location = galaxy_locations[index_location]
          for dest_location in galaxy_locations[index_location + 1:]:
               expand_x = count_expansions(x_expansions, source_location[1], dest_location[1])
               expand_y = count_expansions(y_expansions, source_location[0], dest_location[0])
               source_x = source_location[1] 
               source_y = source_location[0]
               dest_x = dest_location[1]
               dest_y = dest_location[0] 
               distance = abs(source_y - dest_y) + abs(source_x - dest_x) + (expand_x * expansion_size)+ (expand_y * expansion_size)
               distance_total += distance
          

     return distance_total
         
galaxy_map = extract_data(file_path)
galaxy_locations = find_locations(galaxy_map)
total_distance = find_distance(galaxy_locations, galaxy_map)

print("Part: " + str(total_distance)) 
# Part 1 10231178
# Part 2 622120986954

