import os
import re
import math
import itertools

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

class SpringRow:

     def __init__(self, row:str):
          records, specifiers = row.split(' ')
          self.records = records.strip()
          self.specifiers = specifiers.strip()

          self.spec_list = [int(x) for x in re.findall(r'\d+', self.specifiers)]
          self.solutions = []


def extract_data(file_path:str) -> []:
     spring_data = []
     with open(file_path, 'r') as file:
          for line in file:
               line = line.strip()
               spring_data.append(SpringRow(line))

     return spring_data


def generate_permutations(spring_data: SpringRow)-> [str]:
     #for every ? in the row, generate a version with it replaced with "#" or "."
     built_permutations = []
     options = ['#', '.']
     permutations = itertools.product(options, repeat=spring_data.records.count('?'))

     for permutation in permutations:
          result = spring_data.records
          for replacement in permutation:
               result = result.replace('?', replacement, 1)
          built_permutations.append(result)
          
     return built_permutations

def is_valid_solution(solution: str, spec_list:[int]) -> bool:
     # go ahead and move the solution forward by the '.'s at the head
     solution = solution.lstrip('.')
     for spec in spec_list:
          expected_string = "#" * spec
          if not solution.startswith(expected_string):
               return False
          
          solution = solution[spec:]
          if len(solution) > 0:
               if (solution[0] != '.'):
                    return False
          
          solution = solution.lstrip('.')
     
     #at this point we have consumed all the specifiers. The rest of the solution must be all '.'
     if len(solution) > 0:        
          return False

     return True


def find_solutions(spring_data):
     for row in spring_data:
          permutations = generate_permutations(row)
          for solution in permutations:
               if is_valid_solution(solution, row.spec_list):
                    row.solutions.append(solution)



def total_solutions(spring_data):
     total = 0
     for row in spring_data:
          total += len(row.solutions)

     return total


spring_data = extract_data(file_path)
find_solutions(spring_data)
total_solutions = total_solutions(spring_data)

print(f"Part 1: {total_solutions}") #7541


