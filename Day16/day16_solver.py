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
     def __init__(self, next_step:BeamStep, previous_steps = set()):
          self.previous_steps = previous_steps
          self.next_step = next_step

     def move(self, next_step):
          self.previous_steps.add((self.next_step.y, self.next_step.x, self.next_step.direction))
          self.next_step = next_step

     def is_cycle(self):
          if (self.next_step.y, self.next_step.x, self.next_step.direction) in self.previous_steps:
               return True
                    
          return False
     

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


def energize_map(mirror_map):
     beam_q = Queue()
     # Initally one beam from y = 0, x = -1 Traveling (0, +1)
     beam_q.put(Beam(BeamStep(0, -1, "E")))
     
     while not beam_q.empty():
          beam = beam_q.get()
          #print_map(mirror_map)

          while True:               
               dir_y, dir_x = directions[beam.next_step.direction]
               next_y = beam.next_step.y + dir_y
               next_x = beam.next_step.x + dir_x
               
               if beam.is_cycle():
                    break

               if (next_y < 0) or (next_y >= len(mirror_map)) or (next_x < 0) or (next_x >= len(mirror_map[0])):
                    break

               mirror_tile = mirror_map[next_y][next_x]
               mirror_tile.energized = True
               #print_map(mirror_map)
               if mirror_tile.type == '.':
                    # move the beam in the same direction
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
                         # move the beam in the same direction
                         beam.move(BeamStep(next_y, next_x, beam.next_step.direction))
                         continue
                    elif beam.next_step.direction == 'E' or beam.next_step.direction == 'W':
                         #split the beam
                         beam_q.put(Beam(BeamStep(next_y, next_x, 'N'), beam.previous_steps))
                         beam_q.put(Beam(BeamStep(next_y, next_x, 'S'), beam.previous_steps))
                         break #This should kill the current beam                    
               elif mirror_tile.type == '-':
                    if beam.next_step.direction == 'N' or beam.next_step.direction == 'S':
                          #split the beam
                         beam_q.put(Beam(BeamStep(next_y, next_x, 'E'), beam.previous_steps))
                         beam_q.put(Beam(BeamStep(next_y, next_x, 'W'), beam.previous_steps))
                         break #This should kill the current beam
                    elif beam.next_step.direction == 'E' or beam.next_step.direction == 'W':
                         # move the beam in the same direction
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

mirror_map = extract_data(file_path)
energize_map(mirror_map)
total_energy = count_energized(mirror_map)

print_map(mirror_map)

print(f"Part 1: {total_energy}") # 8249

