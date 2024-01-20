# #Obelisk v.1.8.4
import time
import village as v


class Game:
    def __init__(self, data):
        wood, clay, iron, progress1, progress2, progress_time, headquartes, timbercamp, claypit, ironmine, farm, warehouse = data
        self.wood = int(wood)
        self.clay = int(clay)
        self.iron = int(iron)

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

        self.start_progress = (self.progress_time - self.build_speed(self.progress1)) + time.time()
        

    def update(self):
        self.wood_p = v.calculate_factor(1, self.village_level[1])
        self.clay_p = v.calculate_factor(2, self.village_level[2])
        self.iron_p = v.calculate_factor(3, self.village_level[3])
        self.farm = v.calculate_factor(4, self.village_level[4])
        self.warehouse = v.calculate_factor(5, self.village_level[5])

    #Production
    def production(self):
        self.wood = min(self.wood + self.wood_p, self.warehouse)        #Assigns too WOOD the WOOD+PRODUCTION if is smaller than WAREHOUSE
        self.clay = min(self.clay + self.clay_p, self.warehouse)
        self.iron = min(self.iron + self.iron_p, self.warehouse)
        
        #print(f'WOOD:{self.wood}, CLAY:{self.clay},  IRON:{self.iron}')

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
        if self.wood >= v.calculate_wood(building_idx, level+1) and self.clay >= v.calculate_clay(building_idx, level+1) and self.iron >= v.calculate_iron(building_idx, level+1) and population >= v.calculate_population(building_idx, level+1) and self.village_level[building_idx] < v.village[building_idx].maxlv and (self.progress1 == -1 or self.progress2 == -1):
            return True
        else:
            return False
        
    def sub_resources(self, building_idx, level):
        self.wood -= v.calculate_wood(building_idx, self.village_level[building_idx]+level)
        self.clay -= v.calculate_clay(building_idx, self.village_level[building_idx]+level)
        self.iron -= v.calculate_iron(building_idx, self.village_level[building_idx]+level)
        #print(building_idx, level, v.calculate_wood(self.village[building_idx], self.village_level[building_idx]+level), v.calculate_clay(self.village[building_idx], self.village_level[building_idx]+level),v.calculate_iron(self.village[building_idx], self.village_level[building_idx]+level))

    #Calculate the building speed
    def build_speed(self, building_idx):
        speed = v.calculate_factor(0, self.village_level[0])
        _time = v.calculate_time(building_idx, self.village_level[building_idx])
        return int((speed/100)*_time)
          
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
            if self.progress_timer(self.build_speed(self.progress1)):
                self.village_level[self.progress1] += 1
                self.update()
                self.progress1 = self.progress2
                self.progress2 = -1










# #Load data from a file
# def load_database(filename='village.txt'):
#     global P
#     try:
#         with open (filename, 'r') as file:
#             global WOOD, CLAY, IRON
#             resources = file.readline().strip().split(',')      #Read data from te file
#             WOOD, CLAY, IRON, PROGRESS[0], PROGRESS[1], PROGRESS[2]= map(int, resources)              #Assigns data to variables
 
#             for i, line in enumerate(file):
#                 build = int(line.strip())                       #Read data from te file
#                 village[i].lv = build                           #Assigns data to variables
#     except FileNotFoundError:
#         pass

#     P = (PROGRESS[2] - build_speed(PROGRESS[0])) + time.time()

# Delay timer
    
    
# #Progress 1 timer
# def p_timer(t):
#     global P
#     if time.time() > t+P:
#         P = time.time()
#         return True
#     PROGRESS[2] = (P + t) - time.time()


# #Subtracts the resources needed to increase the lv from resources


# #Add 1 lv to a building
# def add_lv(b):
#     village[b].lv += 1
#     update()