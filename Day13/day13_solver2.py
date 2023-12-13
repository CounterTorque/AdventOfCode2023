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
         

def find_center_h(rows, ignore):
     #walk each row pair and check for equality
     for i in range(len(rows) - 1):
         if rows[i] == rows[i+1]:
             if (i == ignore):
                 continue
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

def find_pattern(rows, org_h = -1, org_v = -1):
     center = find_center_h(rows, org_h)
     if (center != -1):
          return center, -1

     #center was not found
     #transpose the rows and try again against the columns
     t_rows = ["".join(t) for t in (zip(*rows))]
     center = find_center_h(t_rows, org_v)
     
     return -1, center
     

def smudge(rows, step):
     s_row = step // len(rows[0])
     s_col = step % len(rows[0])

     smudge_rows = rows[:]
     char = smudge_rows[s_row][s_col]
     if (char == '.'):
          char = '#'
     else:
          char = '.'

     smudge_rows[s_row] = smudge_rows[s_row][:s_col] + char + smudge_rows[s_row][s_col+1:]

     return smudge_rows

def calculate_patterns(mirror_mazes) -> int:
     total = 0
     idx = 0
     for mirror_maze in mirror_mazes:
          print(f"Solving {idx}")
          
          smudge_step = 0
          smudge_max = len(mirror_maze.rows[0]) * len(mirror_maze.rows)
          org_h, org_v = find_pattern(mirror_maze.rows)

          while True:
               rows_next = smudge(mirror_maze.rows, smudge_step)
               h, v = find_pattern(rows_next, org_h, org_v)
               

               if (h != -1 and h != org_h):
                    total += ((h + 1) * 100)
                    break

               if (v != -1 and v != org_v):
                    total += (v + 1)
                    break

               smudge_step += 1
               assert(smudge_step < smudge_max)

          idx += 1
     
     return total


mirror_mazes = extract_data(file_path)
total = calculate_patterns(mirror_mazes)

print(f"total solutions: {total}") # Part 2 34824