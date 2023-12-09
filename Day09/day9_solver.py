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
          
          sub_sequence = [sequence[i+1] - sequence[i] for i in range(len(sequence)-1)]
   
          return Sequence(sub_sequence, self)
     
     def generate_next(self):
          if self.child:
               child_next = self.child.generate_next()
               last_element = self.sequence[-1]
               self.sequence.append(last_element + child_next)
          else:
               self.sequence.append(0)

          return self.sequence[-1]
     
     def generate_prev(self):
          if self.child:
               child_prev = self.child.generate_prev()
               first_element = self.sequence[0]
               self.sequence.insert(0, first_element - child_prev)
          else:
               self.sequence.insert(0, 0)

          return self.sequence[0]
     

def extract_data(file_path):
    sequences = []
    with open(file_path, 'r') as file:
         for line in file:
              line = line.strip()
              numbers = [int(number) for number in line.split(" ")]
              sequences.append(Sequence(numbers))

    return sequences

def build_out_sequence(sequence_list):
     total_next = 0
     total_prev = 0
     for sequence in sequence_list:
          total_next += sequence.generate_next()
          total_prev += sequence.generate_prev()

     return total_next, total_prev

         
sequence_list = extract_data(file_path)
total_count_next, total_count_prev = build_out_sequence(sequence_list)
print("Part 1: ", total_count_next) #1969958987
print("Part 2: ", total_count_prev) #1068

