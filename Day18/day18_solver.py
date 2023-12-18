import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

directions = {
     "U": (0, -1),
     "D": (0, 1),
     "R": (1, 0),
     "L": (-1, 0)
}

ground_space = "   .   "
empty_space = "       "

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
     min_x = 0
     min_y = 0
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
               min_x = min(min_x, cur_pos[0])
               min_y = min(min_y, cur_pos[1])
     
     return dig_map, (min_x, min_y), (max_x, max_y)


def flood_fill_outer(ground_map: dict, min, max):
     
     x_range = range(min[0]-1, max[0] + 2)
     y_range = range(min[1]-1, max[1] + 2)
     
     def fill(x, y, fill_char = empty_space, check_char = ground_space):
          stack = [(x, y)]

          while stack:
               cur_x, cur_y = stack.pop()
               
               if (cur_y < y_range.start) or (cur_y >= y_range.stop) or (cur_x < x_range.start) or (cur_x >= x_range.stop):
                    continue

               key = str((cur_x, cur_y))
               cur = ground_map[key]
               if cur == check_char:
                    ground_map[key] = fill_char
                    neighbors = [(cur_x - 1, cur_y), (cur_x + 1, cur_y), (cur_x, cur_y - 1), (cur_x, cur_y + 1)]
                    stack.extend(neighbors)


     # Assume 0,0 is safe to start with since we padded
     fill(x_range.start, y_range.start)

def expand_map(dig_map, min, max):
     #increase by 1 all around so we can flood fill to remove
     x_range = range(min[0]-1, max[0] + 2)
     y_range = range(min[1]-1, max[1] + 2)
     full_map = {}

     for y in y_range:
          for x in x_range:
               key = str((x, y))
               if key in dig_map:
                    str_o = dig_map[key]
               else:
                    str_o = ground_space
               full_map[key] = str_o
     
     return full_map

def count_area(full_map, min, max):
     #increase by 1 all around so we can flood fill to remove
     x_range = range(min[0]-1, max[0] + 2)
     y_range = range(min[1]-1, max[1] + 2)
     
     total_area = 0
     for y in y_range:
          for x in x_range:
               key = str((x, y))
               val = full_map[key]
               if val != empty_space:
                    total_area += 1

     return total_area

def print_map(map, min, max):
     #increase by 1 all around so we can flood fill to remove
     x_range = range(min[0]-1, max[0] + 2)
     y_range = range(min[1]-1, max[1] + 2)
     
     output_path = os.path.join(base_dir, "output.txt")
     with open(output_path, 'w') as output_file:
          for y in y_range:
               for x in x_range:
                    key = str((x, y))
                    if key in map:
                         str_o = map[key]
                    else:
                         str_o = ground_space
                    output_file.write(str_o + ",")
                    output_file.flush()
               output_file.write('\n')


dig_plans = extract_data(file_path)
dig_map, min, max = build_map(dig_plans)
full_map = expand_map(dig_map, min, max)
flood_fill_outer(full_map, min, max)
total_area = count_area(full_map, min, max)
print_map(full_map, min, max)

print(f"Part 1: {total_area}") #36679


