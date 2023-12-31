import os
import numpy as np

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

X = 0
Y = 1
Z = 2
CUBE = -1

LOWEST_Z = 1
EMPTY = '    '

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
     
     def lower(self, z_offset):
          if (self.head[Z] == LOWEST_Z or self.tail[Z] == LOWEST_Z):
               return False
          
          self.head = self.head[:2] + (self.head[Z] - z_offset,)
          self.tail = self.tail[:2] + (self.tail[Z] - z_offset,)
          return True


def set_volume(volume, brick, name):
     if (brick.orientation == CUBE):
          volume[brick.head[X], brick.head[Y], brick.head[Z]] = name

     if (brick.orientation == X):
          volume[brick.head[X]:(brick.tail[X]+1), brick.head[Y], brick.head[Z]] = name

     if (brick.orientation == Y):
          volume[brick.head[X], brick.head[Y]:(brick.tail[Y]+1), brick.head[Z]] = name

     if (brick.orientation == Z):
          volume[brick.head[X], brick.head[Y], brick.head[Z]:(brick.tail[Z] +1)] = name



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
     volume = np.full((x_max, y_max, z_max), EMPTY, dtype='U4')
     for name, brick in bricks.items():
          set_volume(volume, brick, name)


     return bricks, volume, (x_max, y_max, z_max)
         

def get_below(volume, head, tail, z_below):

     below = []
     for chk_y in range(head[Y], tail[Y]+1):
          for chk_x in range(head[X], tail[X]+1):
               chk_voxel = volume[chk_x, chk_y, z_below]
               if chk_voxel != EMPTY and chk_voxel not in below:
                    below.append(chk_voxel)
                    
     return below     


def settle_bricks(bricks, volume, size):
          
     print_volume(volume, size)

     while True:
          seen = []
          sunk = False
          #start from LOWEST_Z (0 is ground, which may be important later)
          for z in range(LOWEST_Z, size[Z]):
               for y in range(size[Y]):
                    for x in range(size[X]):
                         voxel = volume[x, y, z]
                         if voxel != EMPTY:
                              if voxel in seen:
                                   continue

                              seen.append(voxel)
                              brick = bricks[voxel]
                              z_low = min(brick.head[Z], brick.tail[Z])

                              below_items = get_below(volume, brick.head, brick.tail, z_low-1)

                              if not below_items:                             
                                   #clear the current voxel space
                                   set_volume(volume, brick, EMPTY)
                                   #set the brick z's to -1
                                   did_lower = brick.lower(1)
                                   if sunk == False and did_lower:
                                        sunk = True
                                   #reset the new voxel space to name
                                   set_volume(volume, brick, brick.name)
     
     
          if sunk == False:
               break

     print_volume(volume, size)


def print_volume(volume, size):
     for k in range(size[Z]):
          for j in range(size[Y]):
               for i in range(size[X]):               
                    print(f"volume[{i}][{j}][{k}] = {volume[i, j, k]}")
     


def find_dis(bricks, volume):
     
     removable = []
     seen = []
     for z in range(LOWEST_Z, size[Z]):
               for y in range(size[Y]):
                    for x in range(size[X]):
                         voxel = volume[x, y, z]
                         if voxel == EMPTY:
                              continue

                         if voxel in seen:
                              continue

                         seen.append(voxel)
                         brick = bricks[voxel]

                         #now look directly above this brick
                         #collect all bricks that are above it
                         above = []
                         z_above = max(brick.head[Z], brick.tail[Z]) + 1 #the z of the above brick.
                         for chk_y in range(brick.head[Y], brick.tail[Y]+1):
                              for chk_x in range(brick.head[X], brick.tail[X]+1):
                                   chk_voxel = volume[chk_x, chk_y, z_above]
                                   if chk_voxel != EMPTY and chk_voxel not in above:
                                        above.append(chk_voxel)

                         #for each of those bricks then check count the number of bricks below them
                         safe = True
                         for chk_abv in above:
                              brick_above = bricks[chk_abv]
                              #if there is more than 1, for all items, then it's safe to remove the original brick
                              below_items = get_below(volume, brick_above.head, brick_above.tail, z_above-1)
                              if (len(below_items) <= 1):
                                   safe = False
                                   break

                         if safe:
                              removable.append(voxel)
                                    
     return len(removable)


bricks, volume, size = extract_data(file_path)
settle_bricks(bricks, volume, size)
total = find_dis(bricks, volume)

print(f"Part 1: {total}") #416


