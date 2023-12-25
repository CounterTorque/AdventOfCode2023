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
    def __init__(self, category, destination, source, range_length):
        self.Category = category
        self.Destination = destination
        self.Source = source
        self.RangeLength = range_length


def init_seeds(seed_set, seed_strings):
    for seed in seed_strings:
        next_seed = SeedData()
        next_seed.SeedNumber = int(seed)
        seed_set.append(next_seed)


def extract_data(file_path): 
    seed_set = []
    lookup_maps = {}
    with open(file_path, 'r') as file:
        cur_key = ""
        for idx, line in enumerate(file):
            line = line.strip()
            if (idx == 0):
                seed_strings = re.findall(r'\d+', line)
                init_seeds(seed_set, seed_strings)
                continue

            if line in key_names:
                cur_key = line.strip()    
                lookup_maps[cur_key] = []                
                continue
            elif line == "":
                continue
            else:
                dest, source, range_length = line.split(" ")
                lookup_map = LookupMap(cur_key, int(dest), int(source), int(range_length))
                lookup_maps[cur_key].append(lookup_map)
    
    return seed_set, lookup_maps

        
def build_full_seed(seed_set, lookup_maps):
    for seed in seed_set:
        seed.Soil = find_item(seed.SeedNumber, lookup_maps["seed-to-soil map:"])
        seed.Fertilizer = find_item(seed.Soil, lookup_maps["soil-to-fertilizer map:"])
        seed.Water = find_item(seed.Fertilizer, lookup_maps["fertilizer-to-water map:"])
        seed.Light = find_item(seed.Water, lookup_maps["water-to-light map:"])
        seed.Temperature = find_item(seed.Light, lookup_maps["light-to-temperature map:"])
        seed.Humidity = find_item(seed.Temperature, lookup_maps["temperature-to-humidity map:"])
        seed.Location = find_item(seed.Humidity, lookup_maps["humidity-to-location map:"])
       

def find_map_index(search, lookup_map):
    if (lookup_map.Source <= search) and (search < lookup_map.Source + lookup_map.RangeLength):
        offset = search - lookup_map.Source
        return lookup_map.Destination + offset
    
    return -1


def find_item(search_number, lookup_maps):
    for lookup_map in lookup_maps:
        index = find_map_index(search_number, lookup_map)
        if (index != -1):
            return index
        
    return search_number


seed_set, lookup_maps = extract_data(file_path)
build_full_seed(seed_set, lookup_maps)
lowest_location = min(seed.Location for seed in seed_set)
print(f"Part 1: {lowest_location}") # 199602917