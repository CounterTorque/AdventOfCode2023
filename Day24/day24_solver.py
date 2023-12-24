import os
import math

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

class Hailstone:
     def __init__(self, position, vector):
          self.position = position
          self.vector = vector

def extract_data(file_path):
     hailstones = []
     with open(file_path, 'r') as file:
          for line in file:
               pos, vec = line.split('@')
               pos_num = tuple(int(num) for num in pos.split(","))
               vec_num = tuple(int(num) for num in vec.split(","))
               hailstone = Hailstone(pos_num, vec_num)
               hailstones.append(hailstone)
     
     print(f"Combinations: {math.comb(len(hailstones), 2)}")
     return hailstones


def find_line_intersection(pos1, vec1, pos2, vec2):
     x1, y1, _ = pos1
     x2, y2 = pos1[0] + vec1[0], pos1[1] + vec1[1]
     x3, y3, _ = pos2
     x4, y4 = pos2[0] + vec2[0], pos2[1] + vec2[1]

     # Calculate the denominator of the intersection formula
     denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

     # Check if the lines are parallel (denominator is 0)
     if denominator == 0:
          return None

     # Calculate the intersection point
     x_intersect = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
     y_intersect = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator

     # Check if the intersection point falls within the future of both line segments
     if (
          min(x1, x2) <= x_intersect <= max(x1, x2) and
          min(y1, y2) <= y_intersect <= max(y1, y2) and
          min(x3, x4) <= x_intersect <= max(x3, x4) and
          min(y3, y4) <= y_intersect <= max(y3, y4)
     ):
          return x_intersect, y_intersect

     return None
          
def check_intersections(hailstones):
     total_intersections = 0
     bounds = (200000000000000, 400000000000000, 200000000000000, 400000000000000)
     max_bounds = max(bounds[1] - bounds[0], bounds[3] - bounds[2])
     #for each hailstone, compare it against all the others hailstones
     for i in range(len(hailstones)):
          for j in range(i+1, len(hailstones)):
               #scale the vectors to the max of the bounds
               vec_1 = (hailstones[i].vector[0] * max_bounds, hailstones[i].vector[1] * max_bounds)
               vec_2 = (hailstones[j].vector[0] * max_bounds, hailstones[j].vector[1] * max_bounds)
               intersection = find_line_intersection(hailstones[i].position, vec_1, hailstones[j].position, vec_2)
               if intersection:
                    if bounds[0] <= intersection[0] <= bounds[1] and bounds[2] <= intersection[1] <= bounds[3]:
                         total_intersections += 1


     return total_intersections
         
hailstones = extract_data(file_path)
total_intersections = check_intersections(hailstones)

print(f"Part 1: {total_intersections}") #25261

