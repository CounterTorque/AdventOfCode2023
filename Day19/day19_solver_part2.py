import os
from queue import Queue
import copy

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

class Instruction:
     def __init__(self, raw_instruction):
          self.variable = ""
          self.operator = ""
          self.term = 0
          self.outcome = ""
          self.has_expression = False
          self.is_lt = False

          if ":" not in raw_instruction:
               self.outcome = raw_instruction
               return
          
          self.has_expression = True
          eq, outcome = raw_instruction.split(":")
          self.outcome = outcome

          if "<" in eq:
               self.variable, str_term = eq.split("<")
               self.term = int(str_term)
               self.operator = "<"
               self.is_lt = True
          elif ">" in eq:
               self.variable, str_term = eq.split(">")
               self.term = int(str_term)
               self.operator = ">"

class Workflow:
     def __init__(self, name, raw_instructions):
          self.name = name
          self.instructions = []
          for ins in raw_instructions:
               self.instructions.append(Instruction(ins))
          

class RangePart:
     def __init__(self, x_min, x_max, m_min, m_max, a_min, a_max, s_min, s_max):
          self.x_min = x_min
          self.x_max = x_max
          self.m_min = m_min
          self.m_max = m_max
          self.a_min = a_min
          self.a_max = a_max
          self.s_min = s_min
          self.s_max = s_max

     def __repr__(self):
          return f"""X({self.x_min}, {self.x_max}) {self.x_max - self.x_min}, 
M({self.m_min}, {self.m_max}) {self.m_max - self.m_min},
A({self.a_min}, {self.a_max}) {self.a_max - self.a_min}, 
S({self.s_min}, {self.s_max}) {self.s_max - self.s_min} \n"""


def extract_data(file_path):
     workflows = {}
     parse_parts = False
     with open(file_path, 'r') as file:
          for line in file:
               line = line.strip()

               if line == "":
                    parse_parts = True
                    continue

               if not parse_parts:
                    work_key, ins = line.split("{")
                    ins = ins.replace("}", "")
                    ins = ins.split(",")
                    workflow = Workflow(work_key, ins)
                    workflows[work_key] = workflow
                    continue              

               if parse_parts:
                    continue

     return workflows

def update_part_range(current_part, instruction):
     part_left = copy.deepcopy(current_part)
     part_right = copy.deepcopy(current_part)
     
     l_mod = 1
     r_mod = 0

     if instruction.operator == "<":  
          l_mod = 0
          r_mod = 1
     
     if instruction.variable == "x":
          part_right.x_min = max(part_left.x_min, instruction.term + l_mod)
          part_left.x_max = min(part_left.x_max, instruction.term - r_mod)
     elif instruction.variable == "m":
          part_right.m_min = max(part_left.m_min, instruction.term + l_mod)
          part_left.m_max = min(part_left.m_max, instruction.term - r_mod)
     elif instruction.variable == "a":
          part_right.a_min = max(part_left.a_min, instruction.term + l_mod)
          part_left.a_max = min(part_left.a_max, instruction.term - r_mod)
     elif instruction.variable == "s":
          part_right.s_min = max(part_left.s_min, instruction.term + l_mod)
          part_left.s_max = min(part_left.s_max, instruction.term - r_mod)

     return part_left, part_right

def process_workflows(workflows):
     
     path_q = Queue()
     base_part = RangePart(1, 4000, 1, 4000, 1, 4000, 1, 4000)
     possible_parts = []

     path_q.put((base_part, "in"))
     while not path_q.empty():
          current_part, current_workflow_name = path_q.get()
          if current_workflow_name == 'A':
               print(current_part)
               possible_parts.append(current_part)
               #this is a winning case
               continue

          if current_workflow_name == 'R':
               continue # This is a loosing case
          
          current_workflow = workflows[current_workflow_name]
          for ins in current_workflow.instructions:
               if not ins.has_expression:
                    path_q.put((current_part, ins.outcome))
                    #current part has been updated by preceding instruction
                    continue

               part_left, part_right = update_part_range(current_part, ins)
               if ins.is_lt:
                    path_q.put((part_left, ins.outcome))
                    current_part = part_right
               else:
                    path_q.put((part_right, ins.outcome))
                    current_part = part_left         

    
     return possible_parts

def sum_possible(possible_parts):
     total = 0
     for part in possible_parts:
          total_x = part.x_max - part.x_min + 1
          total_m = part.m_max - part.m_min + 1
          total_a = part.a_max - part.a_min + 1
          total_s = part.s_max - part.s_min + 1
          part_sum = total_x * total_m * total_a *  total_s
          total += part_sum

     return total

         
workflows = extract_data(file_path)
possible_parts = process_workflows(workflows)
total_accepted_sum = sum_possible(possible_parts)

print(f"Part 2: {total_accepted_sum}") # 125744206494820
