import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

class PipeSegment:
     def __init__(self, y, x, type):
          self.y = y
          self.x = x
          self.type = type
          self.step_number = " (()) "

     def connections(self):
          if self.type == "|":
              return (self.y + 1, self.x), (self.y - 1, self.x)
          elif self.type == "-":
               return (self.y, self.x + 1), (self.y, self.x - 1)
          elif self.type == "L":
               return (self.y, self.x + 1), (self.y - 1, self.x)
          elif self.type == "J":
               return (self.y, self.x - 1), (self.y - 1, self.x)
          elif self.type == "7":
               return (self.y + 1, self.x), (self.y, self.x - 1)
          elif self.type == "F":
               return (self.y, self.x + 1), (self.y + 1, self.x)
          elif self.type == ".":
               return None, None
          elif self.type == "S":
               return None, None
     
     def exit_connection(self, input_y, input_x):
          conn_a, conn_b = self.connections()
          assert(conn_a != None and conn_b != None)

          if conn_a[0] == input_y and conn_a[1] == input_x:
               return conn_b
          
          return conn_a
           


def start_connections(pipe_segement: PipeSegment, pipe_map:[[]]):
          assert(pipe_segement.type == "S")

          up = pipe_segement.y - 1
          down = pipe_segement.y + 1
          left = pipe_segement.x - 1
          right = pipe_segement.x + 1

          connections = []

          if up >= 0:
               pipe_check = pipe_map[up][pipe_segement.x]
               if pipe_check.type == "|" or pipe_check.type == "7" or pipe_check.type == "F":
                    connections.append((up, pipe_segement.x))
          
          if down < len(pipe_map[0]):
               pipe_check = pipe_map[down][pipe_segement.x]
               if pipe_check.type == "|" or pipe_check.type == "L" or pipe_check.type == "J":
                    connections.append((down, pipe_segement.x))

          if left >= 0:
               pipe_check = pipe_map[pipe_segement.y][left]
               if pipe_check.type == "-" or pipe_check.type == "L" or pipe_check.type == "F":
                    connections.append((pipe_segement.y, left))

          if right < len(pipe_map):
               pipe_check = pipe_map[pipe_segement.y][right]
               if pipe_check.type == "-" or pipe_check.type == "J" or pipe_check.type == "7":
                    connections.append((pipe_segement.y, right))

          assert(len(connections) == 2)
          return connections[0], connections[1]

               
          
def extract_data(file_path: str):
     x = 0
     y = 0
     pipe_map = []
     start_x = 0
     start_y = 0
     with open(file_path, 'r') as file:
          #I don't know the right way to work with a 2d list in python, so we are doing this
          lines = file.readlines()
          char_list = [list(line.strip()) for line in lines]

          for y in range(len(char_list)):
               pipe_map.append([])
               for x in range(len(char_list[y])):
                    char = char_list[y][x]                           
                    pipe_map[y].append(PipeSegment(y, x, char)) 

                    if (char == "S"):
                         start_y = y
                         start_x = x


     return pipe_map, start_y, start_x 


def walk_pipes(pipe_map:[[]], start_y, start_x):
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
          #print(pipe_b.type + " ", end="")
          steps += 1

          next_a = pipe_a.exit_connection(cur_a[0], cur_a[1])
          next_b = pipe_b.exit_connection(cur_b[0], cur_b[1])
          cur_a = (pipe_a.y, pipe_a.x)
          cur_b = (pipe_b.y, pipe_b.x)
     
     return steps


         
pipe_map, start_y, start_x = extract_data(file_path)
farthest_step = walk_pipes(pipe_map, start_y, start_x )
print("Part 1: ",farthest_step)

#debug print map

output_path = os.path.join(base_dir, "output.txt")
output_file = open(output_path, 'w')
output_file.truncate(0)

for y in range(len(pipe_map)):
     for x in range(len(pipe_map[0])):
          pipe_segement = pipe_map[y][x]
          output_file.write(pipe_segement.step_number)
          output_file.flush()
          #print(pipe_segement.step_number, end='')
     #print('\n')
     output_file.write('\n')

output_file.close()
