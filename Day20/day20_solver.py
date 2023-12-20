import os
import re 

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

LOW = 0
HIGH = 1
OFF = 0
ON = 1

class BroadcastModule:
     def __init__(self, connections:[str]):
          self.connections = connections


class FlipFlopModule:
     def __init__(self, name:str, connections:[str]):
          self.state = OFF
          self.name = name
          self.connections = connections


class ConjunctionModule:
     def __init__(self, name: str, connections:[str]):
          self.name = name
          self.connections = connections
          self.stored_input_signal = {}

     def wire_input(self, input:str):
          self.stored_input_signal[input] = LOW


def split_data (line) -> Tuple(str, [str]):
     result = re.split(r'\s*->\s*', line)
     name, connections = result[0].strip(), result[1]

     conn_list = [con.strip() for con in connections.split(",")]

     return name, conn_list


def extract_data(file_path):
     broadcast_module = None
     flipflop_modules = {}
     conjunction_modules = {}

     with open(file_path, 'r') as file:
          for line in file:
               if "broadcaster" in line:
                   #pull outputs and create class
                   #broadcast -> a, b, c
                   name, conn_list = split_data(line)
                   assert(name == "broadcast")
                   broadcast_module = BroadcastModule(conn_list)
                   continue
              
               if "%" in line:
                   #pull name and connections and create class
                   name, conn_list = split_data(line)
                   name = name[1:]
                   ff_mod = FlipFlopModule(name, conn_list)
                   flipflop_modules.append(ff_mod)
                   continue
              
               if "&" in line:
                   #pull name and connections and create class
                   name, conn_list = split_data(line)
                   name = name[1:]
                   con_mod = ConjunctionModule(name, conn_list)
                   conjunction_modules.append(con_mod)
                   continue

     
     for b_out in broadcast_module.connections:
          if b_out in conjunction_modules:
               conjunction_modules[b_out].wire_input("broadcast")

     for con_module in conjunction_modules:
          for con_out in con_module.connections:
               if con_out in conjunction_modules:
                    conjunction_modules[con_out].wire_input(con_module.name)
     
     for ff_module in flipflop_modules:
          for ff_out in ff_module.connections:
               if ff_out in conjunction_modules:
                    conjunction_modules[ff_out].wire_input(ff_module.name)

     return broadcast_module, flipflop_modules, conjunction_modules


     
         
b_mods, f_mods, c_mods = extract_data(file_path)



