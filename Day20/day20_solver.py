import os

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

     def setup_inputs(self, inputs:[str]):
          assert(self.stored_input_signal.empty())
          for input in inputs:
               self.stored_input_signal[input] = LOW


def extract_data(file_path):
     broadcast_module = None
     flipflop_modules = {}
     conjunction_modules = {}

     with open(file_path, 'r') as file:
          for line in file:
               if "broadcaster" in line:
                   #pull outputs and create class
                   pass
              
               if "%" in line:
                   #pull name and connections and create class
                   pass
              
               if "&" in line:
                   #pull name and connections and create class
              
                   pass

     
     for con_module in conjunction_modules:
          
          #have to afterwords wire up inputs
          # could be broadcast, conjuction, or flipflop
          pass

     
         
extract_data(file_path)


