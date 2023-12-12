import os
import re

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

class SpringRow:

     def __init__(self, row:str):
          records, specifiers = row.split(' ')
          self.records = records.strip()
          self.specifiers = specifiers.strip()

          self.spec_list = re.findall(r'\d+', self.specifiers)
          self.solutions = []


def extract_data(file_path:str) -> []:
     spring_data = []
     with open(file_path, 'r') as file:
          for line in file:
               line = line.strip()
               spring_data.append(SpringRow(line))

     return spring_data


def find_solution(spring_row: SpringRow):
     #first check if a row has any unknowns
     if "?" not in spring_row.records:
          spring_row.solutions.append(spring_row.records)
          return

     return


def find_solutions(spring_data):
     for row in spring_data:
          find_solution(row)



def total_solutions(spring_data):
     total = 0
     for row in spring_data:
          total += len(row.solutions)

     return total

spring_data = extract_data(file_path)
find_solutions(spring_data)
total_solutions = total_solutions(spring_data)

print(f"Part 1: {total_solutions}")
