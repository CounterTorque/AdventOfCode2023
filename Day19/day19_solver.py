import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

Part_Index = {
     "x": 0,
     "m": 1,
     "a": 2,
     "s": 3
}

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
          

class Part:
     def __init__(self, x, m, a, s):
          self.x = x
          self.m = m
          self.a = a
          self.s = s


def extract_data(file_path):
     workflows = {}
     parts = []
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
                    line = line.replace("{", "").replace("}", "")
                    part_items = line.split(",")
                    x = int(part_items[0].split("=")[1])
                    m = int(part_items[1].split("=")[1])
                    a = int(part_items[2].split("=")[1])
                    s = int(part_items[3].split("=")[1])
                    
                    parts.append(Part(x, m, a, s))
                    continue

     return workflows, parts

def compare_part_value(is_lt, work_term, part_val):
     if is_lt:
          return part_val < work_term
     else:
          return part_val > work_term

def execute_workflow(workflow, part):
     for ins in workflow.instructions:
          if not ins.has_expression:
               return ins.outcome
          
          part_val = 0
          if ins.variable == "x":
               part_val = part.x

          if ins.variable == "m":
               part_val = part.m

          if ins.variable == "a":
               part_val = part.a

          if ins.variable == "s":
               part_val = part.s

          result = compare_part_value(ins.is_lt, ins.term, part_val)
          if result:
               return ins.outcome
          

     #should never hit this
     return "-1"

def sum_parts(parts):
     total = 0
     for part in parts:
          total += part.x + part.m + part.a + part.s
     return total


def process_parts(workflows, parts):
     accepted_parts = []
     
     for part in parts:
          next_workflow = workflows["in"]
          while True:
               outcome = execute_workflow(next_workflow, part)
               if (outcome == "A"):
                    accepted_parts.append(part)
                    break

               if (outcome == "R"):
                    break

               next_workflow = workflows[outcome]


     total = sum_parts(accepted_parts)
     return total
         
workflows, parts = extract_data(file_path)
total_accepted_sum = process_parts(workflows, parts)

print(f"Part 1: {total_accepted_sum}") # 325952

