import os
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "input.txt")

#Line width excluding new line
LINE_WIDTH = 140
SYMBOLS = "&+-#@$*/%="

# run through each line in the input
#create a list of NumberEntry of nummbers found
class NumberEntry:
    Line = 0
    Number = 0
    NumberWord = ""
    Start = 0
    End = 0
    Include = False

class SymbolEntry:
    Line = 0
    Symbol = ""
    Index = 0
    GearNumbers = []

NumberEntrysByLine = {}
SymbolEntrysByLine = {}

def build(file_path):    
    with open(file_path, 'r') as file:
        for idx, line in enumerate(file, start=0):
            numbers = re.findall(r'\d+', line)
            locations = []
            for num in numbers:
                locations.append(line.index(num))
                #update line to replace num with spaces
                line = line.replace(num, ' '*len(num), 1)

            numberEntrys = []
            for number, loc in zip(numbers, locations):
                numberEntry = NumberEntry()
                numberEntry.Line = idx
                numberEntry.Number = int(number)
                numberEntry.NumberWord = number
                numberEntry.Start = loc
                numberEntry.End = loc + len(number)-1
                numberEntry.Include = False
                numberEntrys.append(numberEntry)

            NumberEntrysByLine[idx] = numberEntrys

            symbols = re.finditer(r'[&\+\-#\@\$*/%=]', line)
            symbolEntrys = []
            for symbol in symbols:
                symbolEntry = SymbolEntry()
                symbolEntry.Line = idx
                symbolEntry.Index = symbol.start()
                symbolEntry.Symbol = symbol.group()
                symbolEntry.GearNumbers = []
                symbolEntrys.append(symbolEntry)
           
            SymbolEntrysByLine[idx] = symbolEntrys  

        
def find_includes():
    for line in NumberEntrysByLine:
        for number in NumberEntrysByLine[line]:
            #Check Above
            if number.Line > 0:
                line_above = number.Line - 1
                include_overlap(number, line_above)
            
            #Check Left and Right
            for symbolEntry in SymbolEntrysByLine[number.Line]:
                if (symbolEntry.Index == number.Start-1) or (symbolEntry.Index == number.End+1):
                    number.Include = True
                    symbolEntry.GearNumbers.append(number.Number)

            #Check Below
            if number.Line < len(SymbolEntrysByLine) - 1:
                line_below = number.Line + 1
                include_overlap(number, line_below)


def include_overlap(number, line_number):
    for symbolEntry in SymbolEntrysByLine[line_number]:
        #if symbol is in the range of number.start-1 to number.end+1 then include
        if (symbolEntry.Index >= number.Start-1) and (symbolEntry.Index <= number.End+1):
            number.Include = True
            symbolEntry.GearNumbers.append(number.Number)


def sum_includes():
    sum = 0
    for line in NumberEntrysByLine:
        for number in NumberEntrysByLine[line]:
            if number.Include:
                sum += number.Number
    print(sum)


def calculate_gears():
   sum = 0
   for line in SymbolEntrysByLine:
       for symbolEntry in SymbolEntrysByLine[line]:
           if symbolEntry.Symbol != '*':
               continue
           
           if len(symbolEntry.GearNumbers) != 2:
               continue
           
           gear_ratio = symbolEntry.GearNumbers[0] * symbolEntry.GearNumbers[1]
           sum += gear_ratio
           
   print(sum)


build(file_path)

#Part 1
find_includes()
sum_includes()

#Part 2
calculate_gears()