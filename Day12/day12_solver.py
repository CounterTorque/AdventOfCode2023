import os
import re
import itertools
import cProfile

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

class SpringRow:

     def __init__(self, row:str):
          records, specifiers = row.split(' ')
          self.records = records.strip()

          self.spec_list = [int(x) for x in re.findall(r'\d+', specifiers)]
          self.total_solutions = 0


def extract_data(file_path:str) -> []:
     spring_data = []
     with open(file_path, 'r') as file:
          for line in file:
               line = line.strip()
               spring_data.append(SpringRow(line))

     return spring_data

def unfold_records(spring_data: SpringRow):
     for spring in spring_data: 
          original_record = spring.records
          for _ in range(4):
               spring.records += "?" + original_record

          spring.spec_list = spring.spec_list * 5


def is_valid_solution(solution: str, spec_list:[int]) -> bool:
     # Remove leading dots from the solution
     solution = solution.lstrip('.')

     # Iterate over each specifier in spec_list
     for spec in spec_list:
          expected_string = "#" * spec
          # Check if the solution starts with the expected string
          if not solution.startswith(expected_string):
               return False
          
          # Remove the consumed portion from the solution
          solution = solution[spec:]

          # Check if there are remaining characters in the solution
          if solution and solution[0] != '.':
               return False
          
          solution = solution.lstrip('.')
     

     if solution:
          return False

     return True


def find_solutions(spring_data):
     options = ['#', '.']

     for row in spring_data:
          #simplify the data
          record_check = row.records
          max_spec = sum(row.spec_list)

          permutations = itertools.product(options, repeat=record_check.count('?'))

          for permutation in permutations:
               result = record_check
               for replacement in permutation:
                    result = result.replace('?', replacement, 1)
                    
               # precheck
               if result.count('#') != max_spec:
                    continue

               if is_valid_solution(result, row.spec_list):
                    row.total_solutions += 1


          print(row.total_solutions)


def total_solutions(spring_data):
     total = 0
     for row in spring_data:
          total += row.total_solutions

     return total

profiler = cProfile.Profile()
profiler.enable()

spring_data = extract_data(file_path)
#Part 2 Only
unfold_records(spring_data)

find_solutions(spring_data)
total_solutions = total_solutions(spring_data)

print(f"total solutions: {total_solutions}") #7541
profiler.disable()
profiler.print_stats()

#12303440 function calls (12303436 primitive calls) in 3.344 seconds

