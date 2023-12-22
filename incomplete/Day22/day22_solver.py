import os
import numpy as np

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

X = 0
Y = 1
Z = 2
CUBE = -1

def number_to_string(num):
     # Initialize an empty string
     result = ""

     # Convert the number to alphabetical representation
     while num >= 0:
          # Append the current letter to the result string
          result = chr(ord('A') + num % 26) + result

          # Update the number for the next iteration
          num //= 26

          # Check if we need to continue with the next set of letters 
          if num == 0:
               break

     result = result.ljust(4)
     return result

class Brick():
     def __init__(self, name, head, tail):
          self.name = name
          self.head = head
          self.tail = tail
          self.orientation = self.calc_orientation(head, tail)

     def calc_orientation(self, head, tail):
          x_same = head[X] == tail[X]
          y_same = head[Y] == tail[Y]
          z_same = head[Z] == tail[Z]

          if not x_same:
               return X

          if not y_same:
               return Y

          if not z_same:
               return Z

          return CUBE         


def extract_data(file_path):
     bricks = {}
     x_max = 0
     y_max = 0
     z_max = 0     

     with open(file_path, 'r') as file:
          for i, line in enumerate(file):
               name = number_to_string(i)
               #1,0,1~1,2,1
               head_str, tail_str = line.split('~')
               head = tuple(map(int, head_str.split(',')))
               tail = tuple(map(int, tail_str.split(',')))
               brick = Brick(name, head, tail)
               bricks[name] = brick

               x_max = max(x_max, head[X], tail[X])
               y_max = max(y_max, head[Y], tail[Y])
               z_max = max(z_max, head[Z], tail[Z])


     x_max += 1
     y_max += 1
     z_max += 1

     #create 3d array
     volume = np.full((x_max, y_max, z_max),'    ', dtype='U4')
     for name, brick in bricks.items():
          if (brick.orientation == CUBE):
               volume[brick.head[X], brick.head[Y], brick.head[Z]] = name
               continue

          if (brick.orientation == X):
               volume[brick.head[X]:brick.tail[X], brick.head[Y], brick.head[Z]] = name
               continue

          if (brick.orientation == Y):
               volume[brick.head[X], brick.head[Y]:brick.tail[Y], brick.head[Z]] = name
               continue

          if (brick.orientation == Z):
               volume[brick.head[X], brick.head[Y], brick.head[Z]:brick.tail[Z]] = name
               continue

          
     """
     for i in range(x_max):
          for j in range(y_max):
               for k in range(z_max):
                    print(f"volume[{i}][{j}][{k}] = {volume[i, j, k]}")
     """            

     return bricks, volume
         

def settle_bricks(bricks, volume):
     #for each z from 0 to max in the volume
     #check each X, Y to see if it contains a brick (which is not empty)
     #if it does, see if there are all empty spaces 1 z lower.
     #if so then move it down
     #repeat until no bricks move

     


     pass


def find_dis(bricks, volume):
     #for each brick
     #find any bricks that are above it
     #for each of those bricks find any bricks that are bellow it.
     #if there is more than 1, then it's safe to remove the original brick
     for brick_bottom in bricks:
          for brick_other in bricks:
               if brick_bottom == brick_other:
                    continue
               
               
     pass


bricks, volume = extract_data(file_path)
settle_bricks(bricks, volume)
total = find_dis(bricks, volume)

print(f"Part 1: {total}")


