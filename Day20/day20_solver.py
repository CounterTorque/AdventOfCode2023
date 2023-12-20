import os
import re 
from queue import Queue
from abc import abstractmethod

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
          assert(src_name in self.stored_input_signal)
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
     low_pulses = 1
     high_pulses = 0
     pulse_q = Queue()
     
     b_mod = modules["broadcaster"]
     for out in b_mod.connections:
          pulse_q.put(("broadcaster", out, LOW))

     while not pulse_q.empty():
          src_name, dst_name, pulse = pulse_q.get()

          if pulse == LOW:
               low_pulses += 1
          else:
               high_pulses += 1
          
          #todo handle when the output doesn't exist in the modules
          if dst_name not in modules:
               continue

          dst_mod = modules[dst_name]
          next_pulse = dst_mod.InPulse(src_name, pulse)
          if next_pulse is not None:
               for out in dst_mod.connections:
                    pulse_q.put((dst_name, out, next_pulse))
          

     return low_pulses, high_pulses


def cycle_button(modules, num_cycles):
     low_pulses = 0
     high_pulses = 0
     for _ in range(num_cycles):
          run_low, run_high = push_button(modules)
          low_pulses += run_low
          high_pulses += run_high
     
     return low_pulses * high_pulses
     
         
modules = extract_data(file_path)
total_pulses = cycle_button(modules, 1000)


print(f"Part 1: {total_pulses}") #812721756



