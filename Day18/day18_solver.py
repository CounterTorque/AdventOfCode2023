import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

directions = {
     "U": (0, -1),
     "D": (0, 1),
     "R": (1, 0),
     "L": (-1, 0)
}

class DigPlan:
     def __init__(self, direction, length, color) -> None:
          self.direction = direction
          self.length = length
          self.color = color

def extract_data(file_path):
     dig_plans = []
     with open(file_path, 'r') as file:
          for line in file:
               line = line.strip()
               direction, length, color = line.split(" ")
               color = color[1:-1]
               dig_plans.append(DigPlan(direction, int(length), color))
     
     return dig_plans


def build_map(dig_plans):
     max_y = 1
     max_x = 1
     cur_pos = (0, 0)
     dig_map = {}
     # Add in the starting position   
     dig_map[str(cur_pos)] = "#FFFFFF"
     for plan in dig_plans:
          for _ in range(plan.length):
               cur_pos = (cur_pos[0] + directions[plan.direction][0], cur_pos[1] + directions[plan.direction][1])
               key = str(cur_pos)
               dig_map[key] = plan.color
               max_x = max(max_x, cur_pos[0])
               max_y = max(max_y, cur_pos[1])
     
     return dig_map, max_x, max_y


def print_map(map, max_y, max_x):
     output_path = os.path.join(base_dir, "output.txt")
     with open(output_path, 'w') as output_file:
          for y in range(max_y + 1):
               for x in range(max_x + 1):
                    key = str((x, y))
                    if key in map:
                         str_o = map[key]
                    else:
                         str_o = "   .   "
                    output_file.write(str_o + ",")
                    output_file.flush()
               output_file.write('\n')


dig_plans = extract_data(file_path)
dig_map, max_x, max_y= build_map(dig_plans)

print_map(dig_map, max_y, max_x)


