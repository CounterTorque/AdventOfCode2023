import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

class Instruction:
     def __init__(self, action, label, val, hash):
          self.action = action
          self.label = label
          self.val = val
          self.hash = hash


def operator_extract(sequence):
     if '=' in sequence:
          eq_pos = sequence.index("=")
          return '=', sequence[:eq_pos], int(sequence[eq_pos+1:])
     
     return '-',sequence[:-1], 0    


def holiday_hash(sequence):
     h_hash = 0
     for char in sequence:
          ascii = ord(char)
          h_hash += ascii
          h_hash *= 17
          h_hash %=256

     return h_hash


def extract_data(file_path):
     instructions = []
     with open(file_path, 'r') as file:
          for line in file:
               sequences = line.split(",")
               for seq in sequences:
                    action,label, val = operator_extract(seq)
                    h_total = holiday_hash(label)
                    instructions.append(Instruction(action, label, val, h_total))                   
     
     return instructions

def slot_lenses(instructions):
     lens_boxes = {i:[] for i in range(256)}

     for instruction in instructions:
          lens_box = lens_boxes[instruction.hash]

          if instruction.action == '=':
               for lens in lens_box:
                    if lens.label == instruction.label:
                         lens.val = instruction.val
                         break
               else:
                    lens_boxes[instruction.hash].append(instruction)

          elif instruction.action == '-':
               for lens in lens_box:
                    if lens.label == instruction.label:
                         lens_box.remove(lens)
                         break


     return lens_boxes


def calculate_focus(lens_boxes: {[str, [Instruction]]}) -> int:
     focusing_power = 0
     for box, lenses in lens_boxes.items():
          box_value = int(box) + 1
          for slot, lens in enumerate(lenses):
               lens_pow = box_value * (slot + 1) * lens.val
               focusing_power += lens_pow
     
     return focusing_power
         
instructions = extract_data(file_path)
lens_boxes = slot_lenses(instructions)
focusing_power = calculate_focus(lens_boxes)

print(f"Part 2: {focusing_power}") # 260530

