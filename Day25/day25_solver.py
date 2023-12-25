import os
import sys
import networkx as nx

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

sys.setrecursionlimit(5000)

def extract_data(file_path):
     components = {}
     with open(file_path, 'r') as file:
          for line in file:
               line = line.strip()
               core_componenet, connections = line.split(":")
               connection_items = connections.strip().split(" ")
               if (core_componenet not in components):
                    components[core_componenet] = []
               components[core_componenet].extend(connection_items)

               for conn in connection_items:
                    if conn not in components:
                         components[conn] = []
                    components[conn].append(core_componenet)
     
     return components


def split_components(components):
     graph = nx.DiGraph()
     for key, value in components.items():
          for item in value:
               graph.add_edge(key, item, capacity=1)
               graph.add_edge(item, key, capacity=1)
               
     for x in components.keys():
          for y in components.keys():
               if x == y:
                    continue
               cuts, (L,R) = nx.minimum_cut(graph, x, y)
               if (cuts == 3):
                    return (len(L) * len(R))
     
         
components = extract_data(file_path)
max_size = split_components(components)

print(f"Part 1: {max_size}") # 598120
