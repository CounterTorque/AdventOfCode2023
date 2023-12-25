import os
import math

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

class Element:
    def __init__(self, name, left, right):
        self.name = name.strip()
        self.left = left.strip()
        self.right = right.strip()

class ParseStep:
    def __init__(self, cur_node):
        self.cur_node = cur_node
        self.total_steps = 0

    def is_end(self):
        return self.cur_node.endswith("Z")

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

def find_starting_nodes(keys):
    starting_nodes = [key for key in keys if key.endswith("A")]
    return starting_nodes
        

def walk_full_instructions(first_elem, elements, instructions):
    current_instruction = 0
    current_step = 0
    current_node = first_elem

    while not current_node.endswith("Z"):
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
starting_nodes = find_starting_nodes(elements)
parse_steps = []
for node in starting_nodes:
    parse_step = ParseStep(node)
    parse_step.total_steps = walk_full_instructions(node, elements, instructions)
    parse_steps.append(parse_step) 
    
total_steps = math.lcm(*[parse_step.total_steps for parse_step in parse_steps])


print(total_steps) #day 8 part 2 15299095336639