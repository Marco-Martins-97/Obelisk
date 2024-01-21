# #Obelisk v.1.9.1
import time
import village as v


class Game:
    def __init__(self, data):
        wood, clay, iron, progress1, progress2, progress_time, headquartes, timbercamp, claypit, ironmine, farm, warehouse = data
        self.wood = float(wood)
        self.clay = float(clay)
        self.iron = float(iron)

        self.progress1 = int(progress1)
        self.progress2 = int(progress2)
        self.progress_time = int(progress_time)

        self.village_level = [int(headquartes), int(timbercamp), int(claypit), int(ironmine), int(farm), int(warehouse)]

        self.wood_p = v.calculate_factor(1, self.village_level[1])
        self.clay_p = v.calculate_factor(2, self.village_level[2])
        self.iron_p = v.calculate_factor(3, self.village_level[3])
        self.farm = v.calculate_factor(4, self.village_level[4])
        self.warehouse = v.calculate_factor(5, self.village_level[5])

        print(self.warehouse)

        self.start_delay = time.time()
        self.start_autosave = time.time()
        self.start_progress = time.time()

        self.start_progress = (self.progress_time - v.calculate_time(self.progress1, self.village_level[self.progress1], self.village_level[0])) + time.time()
        

    def update(self):
        self.wood_p = v.calculate_factor(1, self.village_level[1])
        self.clay_p = v.calculate_factor(2, self.village_level[2])
        self.iron_p = v.calculate_factor(3, self.village_level[3])
        self.farm = v.calculate_factor(4, self.village_level[4])
        self.warehouse = v.calculate_factor(5, self.village_level[5])

    #Production
    def production(self):
        self.wood = min(self.wood + self.wood_p/3600, self.warehouse)        #Assigns too WOOD the WOOD+PRODUCTION if is smaller than WAREHOUSE
        self.clay = min(self.clay + self.clay_p/3600, self.warehouse)
        self.iron = min(self.iron + self.iron_p/3600, self.warehouse)
        
        print(f'WOOD:{self.wood}, CLAY:{self.clay},  IRON:{self.iron}')

    def delay(self, t):
        if time.time() > t+self.start_delay:
            self.start_delay = time.time()
            return True

    # #Autosave timer
    def autosave(self, t):
        if time.time() > t+self.start_autosave:
            self.start_autosave = time.time()
            return True
        
    #Progress1 timer
    def progress_timer(self, _time):
        if time.time() > _time+self.start_progress:
            self.start_progress = time.time()
            return True
        self.progress_time = (self.start_progress + _time) - time.time()

    def get_data(self):
        data = (self.wood, self.clay, self.iron, self.progress1, self.progress2, int(self.progress_time), self.village_level[0], self.village_level[1], self.village_level[2], self.village_level[3], self.village_level[1], self.village_level[5])
        return data

    def get_population(self):
        pop = 0
        for building in range(len(v.village)):
            pop += v.calculate_population(building, self.village_level[building])
            #print(pop)
        return pop
    
    def upgrade_avaliable(self, building_idx, level):
        population = self.farm - self.get_population()       
        if self.wood >= v.calculate_wood(building_idx, level+1) and self.clay >= v.calculate_clay(building_idx, level+1) and self.iron >= v.calculate_iron(building_idx, level+1) and population >= v.calculate_population(building_idx, level+1) and self.village_level[building_idx] < v.village[building_idx].max_lv and (self.progress1 == -1 or self.progress2 == -1):
            return True
        else:
            return False
        
    def sub_resources(self, building_idx, level):
        self.wood -= v.calculate_wood(building_idx, self.village_level[building_idx]+level)
        self.clay -= v.calculate_clay(building_idx, self.village_level[building_idx]+level)
        self.iron -= v.calculate_iron(building_idx, self.village_level[building_idx]+level)


    def add_to_progress(self, building_idx):
        if self.progress1 == -1:
            self.sub_resources(building_idx, 1)
            self.progress1 = building_idx
            self.start_progress = time.time()
        elif self.progress2 == -1:
            self.sub_resources(building_idx, 2)
            self.progress2 = building_idx
        else: print('Cant add to progress!')

    # #Process the progress
    def progress_countdown(self):
        if self.progress1 != -1:
            if self.progress_timer(v.calculate_time(self.progress1, self.village_level[self.progress1], self.village_level[0])):
                self.village_level[self.progress1] += 1
                self.update()
                self.progress1 = self.progress2
                self.progress2 = -1
