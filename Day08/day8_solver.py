import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

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
                instructions = list(line)
                continue

            if line == "":
                continue
            
            key, nodes = line.split(" = ")
            left, right = nodes.split(",")
            elements[key] = Element(key, left.strip("("), right.rstrip(")"))

            
    return  elements, instructions
        

def walk_instructions(first_elem, elements, instructions):
    current_instruction = 0
    current_step = 0
    current_node = first_elem

    while current_node != "ZZZ":
        if current_instruction == len(instructions):
            current_instruction = 0

        next_dir = instructions[current_instruction]
        if next_dir == "R":
            current_node = elements[current_node].right
        elif next_dir == "L":
            current_node = elements[current_node].left
        current_instruction += 1
        current_step += 1

    return current_step


elements, instructions = extract_data(file_path)
total_steps = walk_instructions("AAA", elements, instructions)

print(total_steps) #16343 Part 1