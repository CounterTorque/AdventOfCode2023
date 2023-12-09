import os
import math

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

cur_instruction = 0
cur_step = 0

class Element:
    def __init__(self, name, left, right):
        self.name = name.strip()
        self.left = left.strip()
        self.right = right.strip()

class ParseStep:
    def __init__(self, cur_node):
        self.cur_node = cur_node
        self.total_steps = 0

    def isEnd(self):
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

def find_starting_nodes(elements):
    starting_nodes = []
    for key in elements:
        if key.endswith("A"):
            starting_nodes.append(key)
    return starting_nodes
        

def walk_full_instructions(first_elem, elements, instructions):
    cur_instruction = 0
    cur_step = 0
    cur_node = first_elem

    while not cur_node.endswith("Z"):
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
starting_nodes = find_starting_nodes(elements)
parse_steps = []
for node in starting_nodes:
    parse_step = ParseStep(node)
    parse_step.total_steps = walk_full_instructions(node, elements, instructions)
    parse_steps.append(parse_step) 
    
total_steps = math.lcm(*[parse_step.total_steps for parse_step in parse_steps])


print(total_steps) #day 8 part 2 15299095336639