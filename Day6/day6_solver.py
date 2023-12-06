import os
import re

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")

class RaceData:
    def __init__(self, time, distance):
        self.Time = time
        self.Distance = distance
        self.Better_Starts = []
        self.calc_better_starts()

    def calc_better_starts(self):
        for time_start in range(0, self.Time):
            if self.distance_if(time_start) > self.Distance:
                self.Better_Starts.append(time_start)
        return
    
    def distance_if(self, time_start):
        dist_per_second = time_start
        time_left = self.Time - time_start
        return dist_per_second * time_left

    
    def record_ways_count(self):
        return len(self.Better_Starts)

#Part 2 46173809
race_data = [RaceData(55826490, 246144110121111)]
solution_1 = (race_data[0].record_ways_count())

#Part 1 608902
"""
race_data = [RaceData(55, 246),
             RaceData(82, 1441),
             RaceData(64, 1012),
             RaceData(90, 1111),]

solution_1 = (race_data[0].record_ways_count() * 
                race_data[1].record_ways_count() * 
                race_data[2].record_ways_count() *
                race_data[3].record_ways_count())

"""

#Example
"""
race_data = [RaceData(7, 9),
             RaceData(15, 40),
             RaceData(30, 200),
             ]
"""

print(solution_1)