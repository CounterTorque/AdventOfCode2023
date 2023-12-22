import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

X = 0
Y = 1
Z = 2
CUBE = -1

class Brick():
     def __init__(self, head, tail):
          self.head = head
          self.tail = tail
          self.orientation = calc_orientation(head, tail)

     def calc_orientation(head, tail):
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
     bricks = []
     with open(file_path, 'r') as file:
          for line in file:
               #1,0,1~1,2,1
               #x, y, z
               head_str, tail_str = line.split('~')
               head = tuple(map(int, head_str.split(',')))
               tail = tuple(map(int, tail_str.split(',')))
               brick = Brick(head, tail)
               bricks.append(brick)
               
     return bricks
         

def settle_bricks(bricks):
     #sort by lowest z first
     #then for each set of bricks at a given z
     #lower the brick as far as it can go
     #repeat until no bricks move
     pass


def find_dis(bricks):
     #for each brick
     #find any bricks that are above it
     #for each of those bricks find any bricks that are bellow it.
     #if there is more than 1, then it's safe to remove the original brick
     for brick_bottom in bricks:
          for brick_other in bricks:
               if brick_bottom == brick_other:
                    continue
               
               
     pass


bricks = extract_data(file_path)
settle_bricks(bricks)
total = find_dis(bricks)

print(f"Part 1: {total}")


