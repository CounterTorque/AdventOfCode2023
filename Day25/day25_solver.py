import os
from itertools import combinations
import heapq
import copy

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

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
          

def count_groups(components):

     visited = set()
     num_groups = 0
     group_sizes = []

     def dfs(component):
         visited.add(component)
         group_sizes[num_groups] += 1
         for conn in components[component]:
             if conn not in visited:
                 dfs(conn)

     for component in components:
         if component not in visited:
             group_sizes.append(0)
             dfs(component)
             num_groups += 1

     return num_groups, group_sizes


def split_components(components):
     trio_q = list(combinations(components.keys(), 6))

     max_size = 0
     while trio_q:
          conn_a1, conn_a2, conn_b1, conn_b2, conn_c1, conn_c2 = heapq.heappop(trio_q)
          if (conn_a2 not in components[conn_a1] or
               conn_b2 not in components[conn_b1] or 
               conn_c2 not in components[conn_c1]):
               continue
         
          exp_componenets = copy.deepcopy(components)
          exp_componenets[conn_a1].remove(conn_a2)
          exp_componenets[conn_a2].remove(conn_a1)
          exp_componenets[conn_b1].remove(conn_b2)
          exp_componenets[conn_b2].remove(conn_b1)
          exp_componenets[conn_c1].remove(conn_c2)
          exp_componenets[conn_c2].remove(conn_c1)

          cur_groups, group_sizes = count_groups(exp_componenets)
          if (cur_groups > 1):
               assert(cur_groups == 2)
               max_size = group_sizes[0] * group_sizes[1]

     return max_size
     
     
         
components = extract_data(file_path)
max_size = split_components(components)

print(f"Part 1: {max_size}")
