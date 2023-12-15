import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

def holiday_hash(line):
     h_hash = 0
     for char in line:
          ascii = ord(char)
          h_hash += ascii
          h_hash *= 17
          h_hash %=256

     return h_hash

def extract_data(file_path):
     hash_total = 0
     with open(file_path, 'r') as file:
          for line in file:
               sequences = line.split(",")
               for seq in sequences:
                    h_total = holiday_hash(seq.strip())
                    hash_total += h_total
     
     return hash_total
         
hash_total = extract_data(file_path)

print(f"Part 1: {hash_total}")

