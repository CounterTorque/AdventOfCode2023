import os
import re

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

key_names = ["seeds:",
    "seed-to-soil map:",
    "soil-to-fertilizer map:",
    "fertilizer-to-water map:",
    "water-to-light map:",
    "light-to-temperature map:",
    "temperature-to-humidity map:",
    "humidity-to-location map:",]


class SeedData:
    SeedNumber = 0
    Soil = 0
    Fertilizer = 0
    Water = 0
    Light = 0
    Temperature = 0
    Humidity = 0
    Location = 0


class LookupMap:
    def __init__(self, category, destination, source, start):
        self.Category = category
        self.Destination = destination
        self.Source = source
        self.Start = start

seed_set = []
lookup_maps = {}

def init_seeds(seed_strings):
    for seed in seed_strings:
        next_seed = SeedData()
        next_seed.SeedNumber = int(seed)
        seed_set.append(next_seed)

def build(file_path): 
    with open(file_path, 'r') as file:
        cur_key = ""
        for idx, line in enumerate(file):
            line = line.strip()
            if (idx == 0):
                seed_strings = re.findall(r'\d+', line)
                init_seeds(seed_strings)
                continue

            if line in key_names:
                cur_key = line.strip()                    
                continue
            elif line == "":
                continue
            else:
                dest, source, start = line.split(" ")
                lookup_map = LookupMap(cur_key, dest, source, start)
                lookup_maps[cur_key] = lookup_map

        

build(file_path)