import os
from queue import Queue


base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

directions = {
     "N": (-1, 0),
     "S": (1, 0),
     "E": (0, 1),
     "W": (0, -1)
}

class MirrorSpace:
     def __init__(self, y, x, type):
          self.y = y
          self.x = x
          self.type = type
          self.energized = False


class BeamStep:
     def __init__(self, y, x, direction:str):
          self.y = y
          self.x = x
          self.direction = direction


class Beam:
     def __init__(self, next_step:BeamStep):
          self.next_step = next_step

     def move(self, next_step):
          self.next_step = next_step

     

def extract_data(file_path:str):
     mirror_map = []

     with open(file_path, 'r') as file:
          lines = file.readlines()
          char_list = [list(line.strip()) for line in lines]

          for y in range(len(char_list)):
               mirror_map.append([])
               for x in range(len(char_list[y])):
                    char = char_list[y][x]  
                    mirror_map[y].append(MirrorSpace(y, x, char))


     return mirror_map


def energize_map(mirror_map, beam_start: BeamStep):
     beam_q = Queue()
     beam_q.put(Beam(beam_start))
     previous_steps = set()
     
     while not beam_q.empty():
          beam = beam_q.get()
          #print_map(mirror_map)

          while True:               
               dir_y, dir_x = directions[beam.next_step.direction]
               next_y = beam.next_step.y + dir_y
               next_x = beam.next_step.x + dir_x
               
               if (next_y < 0) or (next_y >= len(mirror_map)) or (next_x < 0) or (next_x >= len(mirror_map[0])):
                    break

               mirror_tile = mirror_map[next_y][next_x]
               mirror_tile.energized = True
               if (next_y, next_x, beam.next_step.direction) in previous_steps:
                    break

               previous_steps.add((next_y, next_x, beam.next_step.direction))
               
               if mirror_tile.type == '.':
                    beam.move(BeamStep(next_y, next_x, beam.next_step.direction))
                    continue
               elif mirror_tile.type == '\\':
                    if beam.next_step.direction == 'N':
                         beam.move(BeamStep(next_y, next_x, "W"))
                    elif beam.next_step.direction == 'S':
                         beam.move(BeamStep(next_y, next_x, "E"))
                    elif beam.next_step.direction == 'E':
                         beam.move(BeamStep(next_y, next_x, "S"))
                    elif beam.next_step.direction == 'W':
                         beam.move(BeamStep(next_y, next_x, "N"))
                    continue
               elif mirror_tile.type == '/':
                    if beam.next_step.direction == 'N':
                         beam.move(BeamStep(next_y, next_x, "E"))
                    elif beam.next_step.direction == 'S':
                         beam.move(BeamStep(next_y, next_x, "W"))
                    elif beam.next_step.direction == 'E':
                         beam.move(BeamStep(next_y, next_x, "N"))
                    elif beam.next_step.direction == 'W':
                         beam.move(BeamStep(next_y, next_x, "S"))
                    continue
               elif mirror_tile.type == '|':
                    if beam.next_step.direction == 'N' or beam.next_step.direction == 'S':
                         beam.move(BeamStep(next_y, next_x, beam.next_step.direction))
                         continue
                    elif beam.next_step.direction == 'E' or beam.next_step.direction == 'W':
                         beam_q.put(Beam(BeamStep(next_y, next_x, 'N')))
                         beam_q.put(Beam(BeamStep(next_y, next_x, 'S')))
                         break                     
               elif mirror_tile.type == '-':
                    if beam.next_step.direction == 'N' or beam.next_step.direction == 'S':
                         beam_q.put(Beam(BeamStep(next_y, next_x, 'E')))
                         beam_q.put(Beam(BeamStep(next_y, next_x, 'W')))
                         break 
                    elif beam.next_step.direction == 'E' or beam.next_step.direction == 'W':
                         beam.move(BeamStep(next_y, next_x, beam.next_step.direction))
                         continue
                        


def count_energized(mirror_map):
     count = 0
     for y in range(len(mirror_map)):
          for x in range(len(mirror_map[0])):
               if mirror_map[y][x].energized:
                    count += 1
     return count
     

def print_map(mirror_map):
     output_path = os.path.join(base_dir, "output.txt")
     with open(output_path, 'w') as output_file:
          for row in mirror_map:
               for tile in row:
                    if tile.energized:
                         output_file.write('#')
                    else:
                         output_file.write(tile.type)
                    output_file.flush()
               output_file.write('\n')


def reset_map(mirror_map):
     for y in range(len(mirror_map)):
          for x in range(len(mirror_map[0])):
               mirror_map[y][x].energized = False

def run_map(mirror_map, y, x, direction:str):
     energize_map(mirror_map, BeamStep(y, x, direction))
     total_energy = count_energized(mirror_map)
     #print_map(mirror_map)
     reset_map(mirror_map)
     return total_energy

mirror_map = extract_data(file_path)
max_energy = 0
y_max = len(mirror_map)
x_max = len(mirror_map[0])
assert(x_max == y_max)
for i in range(y_max):
     e_max = run_map(mirror_map, i, -1, "E")    
     w_max = run_map(mirror_map, i, x_max, "W")
     n_max = run_map(mirror_map, y_max, i, "N")
     s_max = run_map(mirror_map, -1, i, "S")
     
     max_energy = max(e_max, w_max, n_max, s_max, max_energy)


#print_map(mirror_map)

print(f"Part 2: {max_energy}") 

