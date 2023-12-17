import os
import heapq

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

directions = {
     "N": (-1, 0),
     "S": (1, 0),
     "E": (0, 1),
     "W": (0, -1)
}

def extract_data(file_path):
     heat_map = []
     with open(file_path, 'r') as file:
          lines = file.readlines()
          char_list = [list(line.strip()) for line in lines]

          for y in range(len(char_list)):
               heat_map.append([])
               for x in range(len(char_list[y])):
                    char = char_list[y][x]  
                    heat_map[y].append(int(char))

     return heat_map

def print_map(map):
     output_path = os.path.join(base_dir, "output.txt")
     with open(output_path, 'w') as output_file:
          for row in map:
               for tile in row:
                    str_o = str(tile).ljust(3, " ")
                    output_file.write(str_o + ",")
                    output_file.flush()
               output_file.write('\n')
         
def walk_map(heat_map):
     start = (0, 0)

     rows = len(heat_map)
     cols = len(heat_map[0])
     end = (rows - 1, cols - 1)

     #clear out the start, we should never revisit it
     heat_map[start[0]][start[1]] = 0

     queue = [(heat_map[start[0]][start[1]], start, "X", 0)]

     seen = set()
     
     while queue:
          current_dist, (cur_y, cur_x), direction, step = heapq.heappop(queue)
          
          # Check if we reached the destination
          if (cur_y, cur_x) == end and step >= 4:
               return current_dist

          #check if this node has already been visited by another step
          if (cur_y, cur_x, direction, step) in seen:
               continue

          seen.add((cur_y, cur_x, direction, step))


          #check if we can move in that direction any further
          if step < 10 and direction != "X":
               delta_y, delta_x = directions[direction]
               new_y, new_x = cur_y + delta_y, cur_x + delta_x
               if 0 <= new_y < rows and 0 <= new_x < cols:
                    new_dist = current_dist + heat_map[new_y][new_x]
                    heapq.heappush(queue, (new_dist, (new_y, new_x), direction, step + 1))

          if step < 4 and direction != "X":
               continue

          #handle the other directions
          for dir in directions.keys():
               #linear direction handled above
               if (dir == direction):
                    continue

               # don't go backwards
               if ((dir == "W" and direction == "E") or 
                    (dir == "E" and direction == "W")or 
                    (dir == "N" and direction == "S")or 
                    (dir == "S" and direction == "N")):
                    continue

               delta_y, delta_x = directions[dir]
               new_y, new_x = cur_y + delta_y, cur_x + delta_x
               
               # Check if the neighbor is within the grid boundaries
               if 0 <= new_y < rows and 0 <= new_x < cols:
                    new_dist = current_dist + heat_map[new_y][new_x]
                    heapq.heappush(queue, (new_dist, (new_y, new_x), dir, 1))
     
     # No path found
     return -1


heat_map = extract_data(file_path)
min_heat_loss = walk_map(heat_map)

print(f"Part 1: {min_heat_loss}")

