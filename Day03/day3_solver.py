import os
import re

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

class NumberEntry:
    def __init__(self, Line, NumberString, Start):
        self.Line = Line
        self.Number = int(NumberString)
        self.Start = Start
        self.End = Start + len(NumberString)-1
        self.Include = False

class SymbolEntry:
    def __init__(self, Line, Symbol, Index):
        self.Line = Line
        self.Symbol = Symbol
        self.Index = Index
        self.GearNumbers = []

number_entries_by_line = {}
symbol_entries_by_line = {}

def build(file_path):    
    with open(file_path, 'r') as file:
        for idx, line in enumerate(file):
            numbers = re.findall(r'\d+', line)
            number_locations = []
            for num in numbers:
                number_locations.append(line.index(num))
                #update line to replace num with spaces to avoid incorrect index
                line = line.replace(num, ' '*len(num), 1)

            number_entries = [NumberEntry(idx, number, loc) for number, loc in zip(numbers, number_locations)]
            number_entries_by_line[idx] = number_entries

            symbols = re.finditer(r'[&\+\-#\@\$*/%=]', line)
            symbol_entries = [SymbolEntry(idx, symbol.group(), symbol.start()) for symbol in symbols]
           
            symbol_entries_by_line[idx] = symbol_entries  
       

def find_includes(number_entries_by_line):
    for line, number_entries in number_entries_by_line.items():
        for number_entry in number_entries:
            check_above(number_entry)
            check_left_and_right(number_entry)
            check_below(number_entry)
            

def check_above(number_entry):
    if number_entry.Line > 0:
        line_above = number_entry.Line - 1
        include_overlap(number_entry, line_above)
        

def check_left_and_right(number_entry):
    for symbol_entry in symbol_entries_by_line[number_entry.Line]:
        if (symbol_entry.Index == number_entry.Start - 1) or (symbol_entry.Index == number_entry.End + 1):
            number_entry.Include = True
            symbol_entry.GearNumbers.append(number_entry.Number)
            

def check_below(number_entry):
    if number_entry.Line < len(symbol_entries_by_line) - 1:
        line_below = number_entry.Line + 1
        include_overlap(number_entry, line_below)


def include_overlap(number_entry, line_number):
    for symbol_entry in symbol_entries_by_line[line_number]:
        if (symbol_entry.Index >= number_entry.Start-1) and (symbol_entry.Index <= number_entry.End+1):
            number_entry.Include = True
            symbol_entry.GearNumbers.append(number_entry.Number)


def sum_includes(number_entries_by_line):
    total_sum = 0
    for line in number_entries_by_line:
        for number_entry in number_entries_by_line[line]:
            if number_entry.Include:
                total_sum += number_entry.Number
    print(total_sum)


def calculate_gears(symbol_entries_by_line):
   total_sum = 0
   for line in symbol_entries_by_line:
       for symbol_entry in symbol_entries_by_line[line]:
           if symbol_entry.Symbol != '*':
               continue
           
           if len(symbol_entry.GearNumbers) != 2:
               continue
           
           gear_ratio = symbol_entry.GearNumbers[0] * symbol_entry.GearNumbers[1]
           total_sum += gear_ratio
           
   print(total_sum)


build(file_path)

#Part 1
find_includes(number_entries_by_line)
sum_includes(number_entries_by_line)
#546312

#Part 2
calculate_gears(symbol_entries_by_line)
#87449461