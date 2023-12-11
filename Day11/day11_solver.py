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
     
     y = 0
     while True:
          has_y_space = all(item == "." for item in galaxy_map[y])
          if has_y_space:
               galaxy_map.insert(y + 1, ["."] * len(galaxy_map[0]))
               y += 1
          
          y += 1
          if (y >= len(galaxy_map)):
               break


     x = 0
     while True:
          has_x_space = all(item == "." for item in [row[x] for row in galaxy_map])
          if has_x_space:
               for row in galaxy_map:
                    row.insert(x + 1, ".")
               x += 1
          
          x += 1
          if (x >= len(galaxy_map[0])):
               break
               
     return galaxy_map

def find_locations(galaxy_map: [[]]) -> [()]:
     locations = []
     for y in range(len(galaxy_map)):
          for x in range(len(galaxy_map[y])):
               if galaxy_map[y][x] != ".":
                    locations.append((y, x))

     return locations

def find_distance(galaxy_locations: [()], galaxy_map: [[]]) -> int:
     distance_total = 0
     for index_location in range(len(galaxy_locations)):
          source_location = galaxy_locations[index_location]
          for dest_location in galaxy_locations[index_location + 1:]:
               distance = abs(source_location[0] - dest_location[0]) + abs(source_location[1] - dest_location[1])
               distance_total += distance
          

     return distance_total
         
galaxy_map = extract_data(file_path)
galaxy_map = expand_map(galaxy_map)
galaxy_locations = find_locations(galaxy_map)
total_distance = find_distance(galaxy_locations, galaxy_map)

print("Part 1: " + str(total_distance)) # 10231178


