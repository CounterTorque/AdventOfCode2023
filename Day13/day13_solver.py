import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

class MirrorMaze:
     def __init__(self, rows):
          self.rows = rows

def extract_data(file_path):
     mirror_mazes = []
     with open(file_path, 'r') as file:
          current_rows = []
          for line in file:
               line = line.strip()
               if line == '':
                   mirror_mazes.append(MirrorMaze(current_rows))
                   current_rows = []
               else:
                    current_rows.append(line)
          
          #last line
          mirror_mazes.append(MirrorMaze(current_rows))

     return mirror_mazes
         

def find_center_h(rows):
     #walk each row pair and check for equality
     for i in range(len(rows) - 1):
         if rows[i] == rows[i+1]:
             # once you find an equality, you need to walk back out from the "center" in both directions checking for equality
             above = i - 1
             below = i + 2
             while above >= 0 and below < len(rows) and rows[above] == rows[below]:
                 above -= 1
                 below += 1
             
             # if you run out of rows in either direction, you're done
             if above < 0 or below >= len(rows):
                 return i
          #if they are ever not equal, you hop back to your first walk and keep going to the end of the rows


     return -1

def calculate_patterns(mirror_mazes) -> int:
     total = 0
     idx = 0
     for mirror_maze in mirror_mazes:
          print(f"Solving {idx}")
          center = find_center_h(mirror_maze.rows)
          if (center != -1):
               total += ((center + 1) * 100)
               idx += 1
               continue

          #center was 0
          #transpose the rows and try again against the columns
          t_rows = ["".join(t) for t in (zip(*mirror_maze.rows))]
          center = find_center_h(t_rows)
          assert(center != -1)
          total += (center + 1)
          idx += 1
     
     return total


mirror_mazes = extract_data(file_path)
total = calculate_patterns(mirror_mazes)

print(f"total solutions: {total}") # Part 1 33520