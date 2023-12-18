import os
import math

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

directions = {
     "3": (0, -1), #U
     "1": (0, 1), #D
     "0": (1, 0), #R
     "2": (-1, 0) #L
}

ground_space = "."
empty_space = " "
dig_space = "#"

class DigPlan:
     def __init__(self, direction, length) -> None:
          self.direction = direction
          self.length = length
          

def extract_data(file_path):
     dig_plans = []
     with open(file_path, 'r') as file:
          for line in file:
               line = line.strip()
               _, _, color = line.split(" ")
               color = color[1:-1]
               length_hex = color[1:-1]
               direction = color[-1]
               dig_plans.append(DigPlan(direction, int(length_hex, 16)))
     
     return dig_plans


def build_map(dig_plans):
     min_x = 0
     min_y = 0
     cur_pos = (0, 0)
     total_length = 0
     
     for plan in dig_plans:
          next_x = directions[plan.direction][0] * plan.length
          next_y = directions[plan.direction][1] * plan.length
          total_length += plan.length

          cur_pos = (cur_pos[0] + next_x, cur_pos[1] + next_y)
          min_x = min(min_x, cur_pos[0])
          min_y = min(min_y, cur_pos[1])


     #project into positive space
     cur_pos = (0 - min_x, 0 - min_y)
     dig_points = []
     dig_points.append(cur_pos)
     
     for plan in dig_plans:
          next_x = directions[plan.direction][0] * plan.length
          next_y = directions[plan.direction][1] * plan.length

          cur_pos = (cur_pos[0] + next_x, cur_pos[1] + next_y)
          dig_points.append(cur_pos)

     
     return dig_points, total_length

def area_between(point1, point2):
     avg_h = (point1[1] + point2[1]) / 2
     width = point2[0] - point1[0]
     sub_area = width * avg_h
     return sub_area

def count_area(dig_points):
     area = 0
     for point1, point2 in zip(dig_points, dig_points[1:]):
          sub_area = area_between(point1, point2)
          area += sub_area

     return area 

dig_plans = extract_data(file_path)
dig_points, total_length = build_map(dig_plans)
total_area = count_area(dig_points)
total_area += total_length

print(f"Part 2: {total_area}") 
#Test 1 should be 
#952408144115
#952398536221.0


