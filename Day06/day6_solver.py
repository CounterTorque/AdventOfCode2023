
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
    

race_data = [RaceData(55, 246),
             RaceData(82, 1441),
             RaceData(64, 1012),
             RaceData(90, 1111),]

solution_1 = (race_data[0].record_ways_count() * 
                race_data[1].record_ways_count() * 
                race_data[2].record_ways_count() *
                race_data[3].record_ways_count())

print(f"Part 1:{solution_1}") # 608902