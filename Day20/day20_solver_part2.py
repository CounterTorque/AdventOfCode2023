import os
import re 
from collections import deque
from abc import abstractmethod
import cProfile

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

LOW = 0
HIGH = 1
OFF = 0
ON = 1

class BaseModule:
     def __init__(self, name:str, connections:[str]):
          self.name = name
          self.connections = connections
     
     @abstractmethod
     def InPulse(self, src_name, pulse) -> int:
          pass

class BroadcastModule(BaseModule):
     def __init__(self, name:str, connections:[str]):
          super().__init__(name, connections)

     def InPulse(self, src_name, pulse) -> int:
          assert(pulse == LOW)
          return LOW


class FlipFlopModule(BaseModule):
     def __init__(self, name:str, connections:[str]):
          super().__init__(name, connections)
          self.state = OFF

     def InPulse(self, src_name, pulse) -> int:
          if pulse == HIGH:
               #ignore
               return None
          
          if self.state == OFF:
               self.state = ON
               return HIGH
          
          if self.state == ON:
               self.state = OFF
               return LOW         


class ConjunctionModule(BaseModule):
     def __init__(self, name: str, connections:[str]):
          super().__init__(name, connections)
          self.stored_input_signal = {}

     def wire_input(self, input:str):
          self.stored_input_signal[input] = LOW
     
     def InPulse(self, src_name, pulse) -> int:
          #assert(src_name in self.stored_input_signal)
          self.stored_input_signal[src_name] = pulse

          if all([x == HIGH for x in self.stored_input_signal.values()]):
               return LOW
          
          return HIGH


def split_data (line):
     result = re.split(r'\s*->\s*', line)
     name, connections = result[0].strip(), result[1]

     conn_list = [con.strip() for con in connections.split(",")]

     return name, conn_list


def extract_data(file_path):
     modules = {}
     
     with open(file_path, 'r') as file:
          for line in file:
               if "broadcaster" in line:
                   name, conn_list = split_data(line)
                   modules["broadcaster"] = BroadcastModule(name, conn_list)
                   continue
              
               if "%" in line:
                   name, conn_list = split_data(line)
                   name = name[1:]
                   ff_mod = FlipFlopModule(name, conn_list)
                   modules[name] = ff_mod
                   continue
              
               if "&" in line:
                   name, conn_list = split_data(line)
                   name = name[1:]
                   con_mod = ConjunctionModule(name, conn_list)
                   modules[name] = con_mod
                   continue
     
  
     for _, module in modules.items():
          for dst in module.connections:
                    if dst not in modules:
                         continue
                    mod = modules[dst]
                    if isinstance(mod, ConjunctionModule): 
                         mod.wire_input(module.name)

     return modules


def push_button(modules):
     #button sends single low to b_mod
     rx_low = 0
     
     pulse_q = deque()
     
     b_mod = modules["broadcaster"]
     for out in b_mod.connections:
          pulse_q.append(("broadcaster", out, LOW))

     while bool(pulse_q):
          src_name, dst_name, pulse = pulse_q.pop()
               
          #todo handle when the output doesn't exist in the modules
          if dst_name not in modules:
               if dst_name == 'rx' and pulse == LOW:
                    rx_low += 1
               continue

          dst_mod = modules[dst_name]
          next_pulse = dst_mod.InPulse(src_name, pulse)
          if next_pulse is not None:
               for out in dst_mod.connections:
                    pulse_q.append((dst_name, out, next_pulse))
          

     return rx_low


def cycle_button(modules, num_cycles):
     
     for i in range(num_cycles):
          if i % 10000 == 0:
               print(f"Cycle {i}")
          rx_low = push_button(modules)
          if rx_low == 1:
               return i
     
     return -1
     
         
modules = extract_data(file_path)
profiler = cProfile.Profile()
profiler.enable()
total_presses = cycle_button(modules, 10000000)
profiler.disable()
profiler.print_stats()


print(f"Part 2: {total_presses}") 
#1,000,000,000 to low
#10,000,000,000 not it


