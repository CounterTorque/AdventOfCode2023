import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

class Sequence:
     def __init__(self, sequence, parent=None):
          self.sequence = sequence
          self.parent = parent
          self.child = self.build_child(sequence)

     def build_child(self, sequence):
          if all(number == 0 for number in sequence):
               return None
          
          sub_sequence = []
          for i in range(len(sequence)-1):
               left = sequence[i]
               right = sequence[i+1]
               sub_sequence.append(right-left)

          return Sequence(sub_sequence, self)
     
     def generate_next(self):
          if self.child:
               #get the next number to add
               child_next = self.child.generate_next()
               cur_last = self.sequence[-1]
               self.sequence.append(cur_last + child_next)
          else:
               #bottom children are all 0s
               self.sequence.append(0)

          #Everyone always returns the last number
          return self.sequence[-1]
     
     def generate_prev(self):
          if self.child:
               #get the previous number to add
               child_prev = self.child.generate_prev()
               cur_first = self.sequence[0]
               self.sequence.insert(0, cur_first - child_prev)
          else:
               #bottom children are all 0s
               self.sequence.insert(0, 0)

          #Everyone always returns the first number
          return self.sequence[0]
     

def extract_data(file_path):
    sequence_list = []
    with open(file_path, 'r') as file:
         for line in file:
              line = line.strip()
              numbers = [int(number) for number in line.split(" ")]
              sequence_list.append(Sequence(numbers))

    return sequence_list

def build_out_next_sequence(sequence_list):
     total_count = 0
     for sequence in sequence_list:
          next_sequence = sequence.generate_next()
          total_count += next_sequence
     
     return total_count


def build_out_prev_sequence(sequence_list):
     total_count = 0
     for sequence in sequence_list:
          prev_sequence = sequence.generate_prev()
          total_count += prev_sequence
     
     return total_count

         
sequence_list = extract_data(file_path)
total_count_next = build_out_next_sequence(sequence_list)
print("Part 1: ", total_count_next)

total_count_prev = build_out_prev_sequence(sequence_list)
print("Part 2: ", total_count_prev)

