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
    Symbol = ""
    Index = 0

NumberEntrys = []
SymbolEntrys = {}

def build(file_path):    
    with open(file_path, 'r') as file:
        for idx, line in enumerate(file, start=0):
            numbers = re.findall(r'\d+', line)
            locations = []
            for num in numbers:
                locations.append(line.index(num))

                #update line to replace num with spaces
                line = line.replace(num, ' '*len(num), 1)
                

            for number, loc in zip(numbers, locations):
                numberEntry = NumberEntry()
                numberEntry.Line = idx
                numberEntry.Number = int(number)
                numberEntry.NumberWord = number
                numberEntry.Start = loc
                numberEntry.End = loc + len(number)-1
                numberEntry.Include = False
                NumberEntrys.append(numberEntry)

            symbols = re.finditer(r'[&\+\-#\@\$*/%=]', line)
            symbolEntrys = []
            for symbol in symbols:
                symbolEntry = SymbolEntry()
                symbolEntry.Index = symbol.start()
                symbolEntry.Symbol = symbol.group()
                symbolEntrys.append(symbolEntry)
           
            SymbolEntrys[idx] = symbolEntrys  

        
def find_includes():
    for number in NumberEntrys:
        #Check Above
        if number.Line > 0:
            line_above = number.Line - 1
            include_overlap(number, line_above)

        if(number.Include):
            continue
        
        #Check Left and Right
        for symbolEntry in SymbolEntrys[number.Line]:
            if (symbolEntry.Index == number.Start-1) or (symbolEntry.Index == number.End+1):
                number.Include = True
                break
        
        if(number.Include):
            continue      

        #Check Below
        if number.Line < len(SymbolEntrys) - 1:
            line_below = number.Line + 1
            include_overlap(number, line_below)


def include_overlap(number, line_number):
    for symbol in SymbolEntrys[line_number]:
        #if symbol is in the range of number.start-1 to number.end+1 then include
        if (symbol.Index >= number.Start-1) and (symbol.Index <= number.End+1):
            number.Include = True
            break


def sum_includes():
    sum = 0
    for number in NumberEntrys:
        if number.Include:
            sum += number.Number
    print(sum)

build(file_path)
find_includes()
sum_includes()