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
         
def walk_map(heat_map):
     start = (0, 0)
     
     rows = len(heat_map)
     cols = len(heat_map[0])
     end = (rows - 1, cols - 1)

     distance = [[float('inf')] * cols for _ in range(rows)]
     distance[start[0]][start[1]] = heat_map[start[0]][start[1]]
     queue = [(heat_map[start[0]][start[1]], start, "S")]
     heapq.heappush(queue, (heat_map[start[0]][start[1]], start, "E"))

     # each x,y indicates how much heat loss would occur if you enter that block
     # we can only move in the same NESW direction for a total of 3 blocks in a line
     # Otherwise we can move left or right, but not backwards
     # We start at 0, 0 and end at y_max-1, x_max-1

     #start with just dijkstras
     while queue:
          current_dist, (cur_y, cur_x), direction = heapq.heappop(queue)
          
          # Check if we reached the destination
          if (cur_y, cur_x) == end:
               return distance[cur_y][cur_x]
          
          # Check neighbors
          for dir in directions.keys():
               delta_y, delta_x = directions[dir]
               new_y, new_x = cur_y + delta_y, cur_x + delta_x
               
               # Check if the neighbor is within the grid boundaries
               if 0 <= new_y < rows and 0 <= new_x < cols:
                    new_dist = current_dist + heat_map[new_y][new_x]
                    
                    # Update the distance if it's shorter
                    if new_dist < distance[new_y][new_x]:
                         distance[new_y][new_x] = new_dist
                         heapq.heappush(queue, (new_dist, (new_y, new_x), dir))
     
     # No path found
     return -1


heat_map = extract_data(file_path)
min_heat_loss = walk_map(heat_map)

print(f"Part 1: {min_heat_loss}")

