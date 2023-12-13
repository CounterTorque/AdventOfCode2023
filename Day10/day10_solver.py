import os
import sys
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

EMPTY = "((.)) "
OUTSIDE = "      "

matrix_map = {
     "|":[[' ','X',' '],
          [' ','X',' '],
          [' ','X',' ']],
     "-":[[' ',' ',' '],
          ['X','X','X'],
          [' ',' ',' ']],
     "L":[[' ','X',' '],
          [' ','X','X'],
          [' ',' ',' ']],
     "J":[[' ','X',' '],
          ['X','X',' '],
          [' ',' ',' ']],
     "7":[[' ',' ',' '],
          ['X','X',' '],
          [' ','X',' ']],
     "F":[[' ',' ',' '],
          [' ','X','X'],
          [' ','X',' ']],
     ".":[['O','O','O'],
          ['O','O','O'],
          ['O','O','O']],
     "S":[[' ',' ',' '],
          [' ','X',' '],
          [' ',' ',' ']],
}

class PipeSegment:
     def __init__(self, y, x, type):
          self.y = y
          self.x = x
          self.type = type
          self.step_number = EMPTY
          self.matrix = matrix_map[type]

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
                    pipe_segment.matrix[0][1] = "X"
          
          if down < len(pipe_map):
               pipe_check = pipe_map[down][pipe_segment.x]
               if pipe_check.type in ["|", "L", "J"]:
                    connections.append((down, pipe_segment.x))
                    pipe_segment.matrix[2][1] = "X"

          if left >= 0:
               pipe_check = pipe_map[pipe_segment.y][left]
               if pipe_check.type in ["-", "L", "F"]:
                    connections.append((pipe_segment.y, left))
                    pipe_segment.matrix[1][0] = "X"

          if right < len(pipe_map[0]):
               pipe_check = pipe_map[pipe_segment.y][right]
               if pipe_check.type in ["-", "J", "7"]:
                    connections.append((pipe_segment.y, right))
                    pipe_segment.matrix[1][2] = "X"


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


def flood_fill_outer(output_map = [[]]):
     
     height = len(output_map)
     width = len(output_map[0])
     
     def fill(y, x, fill_char = " ", check_char = "O"):
          stack = [(y, x)]

          while stack:
               curr_y, curr_x = stack.pop()
               
               if (curr_y < 0) or (curr_y >= height) or (curr_x < 0) or (curr_x >= width):
                    continue

               cur = output_map[curr_y][curr_x]
               if cur == check_char:
                    output_map[curr_y][curr_x] = fill_char
                    neighbors = [(curr_y - 1, curr_x), (curr_y + 1, curr_x), (curr_y, curr_x - 1), (curr_y, curr_x + 1)]
                    stack.extend(neighbors)


     # Assume 0,0 is safe to start with
     fill(0, 0)
     fill(0, 0, "O", " ")
     fill(0, 0)


def clean_matrix(pipe_map = [[]]):
     for row in pipe_map:
          for pipe_segment in row:
               if (pipe_segment.step_number == EMPTY): 
                    pipe_segment.matrix = matrix_map["."]



def construct_output_map(pipe_map = [[]]):
     output_map = []
     y_max = len(pipe_map) * 3
     x_max = len(pipe_map[0])
     for y in range(y_max):
          output_map.append([])
          for x in range(x_max):
               y_item = y // 3
               y_step = y % 3
               pipe_segement = pipe_map[y_item][x]
               matrix_cur = pipe_segement.matrix[y_step]
               for item in matrix_cur:
                    output_map[y].append(item)
               
          
     return output_map

pipe_map, start_y, start_x = extract_data(file_path)
farthest_step = walk_pipes(pipe_map, start_y, start_x )
clean_matrix(pipe_map)
print("Part 1: ",farthest_step) #6820

output_map = construct_output_map(pipe_map)
flood_fill_outer(output_map)
#debug print map

def print_output_map(base_dir, pipe_map):
     count_o = 0
     output_path = os.path.join(base_dir, "output.txt")
     with open(output_path, 'w') as output_file:
          for row in output_map:
               for output_item in row:
                    output_file.write(output_item)
                    count_o += output_item.count('O')
                    output_file.flush()
               output_file.write('\n')

     print("Part 2: ", count_o // 9) # 337

print_output_map(base_dir, pipe_map)



#part 2 
# 201 is too low
# 248 is too low
# 586 is too high