import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

cur_instruction = 0
cur_step = 0

class Element:
    def __init__(self, name, left, right):
        self.name = name.strip()
        self.left = left.strip()
        self.right = right.strip()


def extract_data(file_path):
    elements = {}
    instructions = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if len(instructions) == 0:                
                instructions = [char for char in line]
                continue
            elif line == "":
                continue
            else:
                key, nodes = line.split(" = ")
                left, right = nodes.split(",")
                elements[key] = Element(key, left.strip("("), right.rstrip(")"))

            
    return  elements, instructions
        

def walk_instructions(first_elem, elements, instructions):
    cur_instruction = 0
    cur_step = 0
    cur_node = first_elem

    while cur_node != "ZZZ":
        if cur_instruction == len(instructions):
            cur_instruction = 0

        next_dir = instructions[cur_instruction]
        if next_dir == "R":
            cur_node = elements[cur_node].right
        elif next_dir == "L":
            cur_node = elements[cur_node].left
        cur_instruction += 1
        cur_step += 1

    return cur_step


elements, instructions = extract_data(file_path)
total_steps = walk_instructions("AAA", elements, instructions)

print(total_steps) #16343 Part 1