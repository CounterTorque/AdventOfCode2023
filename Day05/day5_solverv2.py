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
    def __init__(self, seed_start, range):
        self.SeedStart = seed_start
        self.SeedEnd = seed_start + range


class LookupMap:
    def __init__(self, category, destination, source, range_length):
        self.Category = category
        self.Destination = destination
        self.DestinationEnd = destination + range_length
        self.Source = source
        self.SourceEnd = source + range_length


def init_seeds(seed_set, seed_strings):
    is_start = True
    seed_start = 0
    for seed in seed_strings:
        if is_start:
            seed_start = int(seed)
            is_start = False
            continue
        
        is_start = True
        seed_range = int(seed)
        next_seed = SeedData(seed_start, seed_range)
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


def check_seed_exists(seed_search, seed_set):
    for seed in seed_set:
        if (seed.SeedStart <= seed_search) and (seed_search < seed.SeedEnd):
            return True
    return False


def find_lowest_location(seed_set, lookup_maps):
    lowest_location = 0
    while True:   
        cur_Humidity = find_item(lowest_location, lookup_maps["humidity-to-location map:"])        
        cur_Temperature = find_item(cur_Humidity, lookup_maps["temperature-to-humidity map:"])        
        cur_Light = find_item(cur_Temperature, lookup_maps["light-to-temperature map:"])        
        cur_Water = find_item(cur_Light, lookup_maps["water-to-light map:"])        
        cur_Fertilizer = find_item(cur_Water, lookup_maps["fertilizer-to-water map:"])
        cur_Soil = find_item(cur_Fertilizer, lookup_maps["soil-to-fertilizer map:"])
        cur_Seed = find_item(cur_Soil, lookup_maps["seed-to-soil map:"])

        # find if seed exists for soil
        if check_seed_exists(cur_Seed, seed_set):
            return lowest_location
        
        lowest_location += 1
        

def sort_maps(lookup_maps):
    for item in lookup_maps:
        lookup_maps[item].sort(key=lambda x: x.Destination)
       
def find_source_from_destination(search, lookup_map):
    if (lookup_map.Destination <= search) and (search < lookup_map.DestinationEnd):
        offset = search - lookup_map.Destination
        return lookup_map.Source + offset
    
    return -1


def find_item(search_number, lookup_maps):
    for lookup_map in lookup_maps:
        index = find_source_from_destination(search_number, lookup_map)
        if (index != -1):
            return index
        
    return search_number

seed_set, lookup_maps = extract_data(file_path)
sort_maps(lookup_maps)
lowest_location = find_lowest_location(seed_set, lookup_maps)
print(lowest_location) #2254686