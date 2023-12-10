import os
import sys
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

EMPTY = "((.)) "
OUTSIDE = "      "

class PipeSegment:
     def __init__(self, y, x, type):
          self.y = y
          self.x = x
          self.type = type
          self.step_number = EMPTY

     def connections(self):
          type_mapping = {
               "|": ((self.y + 1, self.x), (self.y - 1, self.x)),
               "-": ((self.y, self.x + 1), (self.y, self.x - 1)),
               "L": ((self.y, self.x + 1), (self.y - 1, self.x)),
               "J": ((self.y, self.x - 1), (self.y - 1, self.x)),
               "7": ((self.y + 1, self.x), (self.y, self.x - 1)),
               "F": ((self.y, self.x + 1), (self.y + 1, self.x)),
               ".": (None, None),
               "S": (None, None)
          }
          
          return type_mapping.get(self.type)
 
     
     def exit_connection(self, input_y, input_x):
          conn_a, conn_b = self.connections()
          assert(conn_a != None and conn_b != None)

          if conn_a[0] == input_y and conn_a[1] == input_x:
               return conn_b
          
          return conn_a
           


def start_connections(pipe_segment: PipeSegment, pipe_map:[[]]):
          assert(pipe_segment.type == "S")

          up = pipe_segment.y - 1
          down = pipe_segment.y + 1
          left = pipe_segment.x - 1
          right = pipe_segment.x + 1

          connections = []

          if up >= 0:
               pipe_check = pipe_map[up][pipe_segment.x]
               if pipe_check.type in ["|", "7", "F"]:
                    connections.append((up, pipe_segment.x))
          
          if down < len(pipe_map):
               pipe_check = pipe_map[down][pipe_segment.x]
               if pipe_check.type in ["|", "L", "J"]:
                    connections.append((down, pipe_segment.x))

          if left >= 0:
               pipe_check = pipe_map[pipe_segment.y][left]
               if pipe_check.type in ["-", "L", "F"]:
                    connections.append((pipe_segment.y, left))

          if right < len(pipe_map[0]):
               pipe_check = pipe_map[pipe_segment.y][right]
               if pipe_check.type in ["-", "J", "7"]:
                    connections.append((pipe_segment.y, right))

          assert(len(connections) == 2)
          return connections[0], connections[1]

               
          
def extract_data(file_path: str):
     pipe_map = []
     start_x = 0
     start_y = 0
     with open(file_path, 'r') as file:
          lines = file.readlines()
          char_list = [list(line.strip()) for line in lines]

          for y in range(len(char_list)):
               pipe_map.append([])
               for x in range(len(char_list[y])):
                    char = char_list[y][x]                           
                    pipe_map[y].append(PipeSegment(y, x, char)) 

                    if (char == "S"):
                         pipe_map[y][x].step_number = "SSSSS "
                         start_y = y
                         start_x = x


     return pipe_map, start_y, start_x 


def walk_pipes(pipe_map:[[]], start_y:int , start_x:int ) -> int:
     pipe_segement = pipe_map[start_y][start_x]
     
     cur_a = (start_y, start_x)
     cur_b = (start_y, start_x)
     next_a, next_b = start_connections(pipe_segement, pipe_map)     
     steps = 1

     while(next_a != next_b):
          pipe_a = pipe_map[next_a[0]][next_a[1]]
          pipe_b = pipe_map[next_b[0]][next_b[1]]
          pipe_a.step_number = "A" + str(steps).rjust(4, "0") + " "
          pipe_b.step_number = "B" + str(steps).rjust(4, "0") + " "
          steps += 1

          next_a = pipe_a.exit_connection(cur_a[0], cur_a[1])
          next_b = pipe_b.exit_connection(cur_b[0], cur_b[1])
          cur_a = (pipe_a.y, pipe_a.x)
          cur_b = (pipe_b.y, pipe_b.x)
     
     pipe_map[next_a[0]][next_a[1]].step_number = "AB.AB "
     
     return steps


def flood_fill_outer(pipe_map = [[]]):
     sys.setrecursionlimit(6000)
     height = len(pipe_map)
     width = len(pipe_map[0])
     def fill(y, x):
          if (y < 0) or (y >= height) or (x < 0) or (x >= width):
               return
          if pipe_map[y][x].step_number == EMPTY:
               pipe_map[y][x].step_number = OUTSIDE
               neighbors =  [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]
               for n in neighbors:
                    fill(n[0],n[1])
     
     # Assume 0,0 is safe to start with
     fill(0, 0)

     #known outside
     fill(66,0)
     fill(73,0)


pipe_map, start_y, start_x = extract_data(file_path)
farthest_step = walk_pipes(pipe_map, start_y, start_x )
print("Part 1: ",farthest_step) #6820

flood_fill_outer(pipe_map)
#debug print map

def print_output_map(base_dir, pipe_map):
     output_path = os.path.join(base_dir, "output.txt")
     with open(output_path, 'w') as output_file:
          for row in pipe_map:
               for pipe_segment in row:
                    output_file.write(pipe_segment.step_number)
                    output_file.flush()
               output_file.write('\n')

print_output_map(base_dir, pipe_map)

#part 2 
# 201 is too low
# 248 is too low
# 586 is too high