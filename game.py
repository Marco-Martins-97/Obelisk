# #Obelisk v.1.8.3
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

        self.village = [v.Headquartes(), v.TimberCamp(), v.ClayPit(), v.IronMine(), v.Farm(), v.Warehouse()]
        self.village_level = [int(headquartes), int(timbercamp), int(claypit), int(ironmine), int(farm), int(warehouse)]

        self.wood_p = v.calculate_factor(self.village[1], self.village_level[1]-1)
        self.clay_p = v.calculate_factor(self.village[2], self.village_level[2]-1)
        self.iron_p = v.calculate_factor(self.village[3], self.village_level[3]-1)
        self.farm = v.calculate_factor(self.village[4], self.village_level[4]-1)
        self.warehouse = v.calculate_factor(self.village[5], self.village_level[5]-1)

        self.start_delay = time.time()
        self.start_autosave = time.time()
        self.start_progress = time.time()
        


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

    def get_data(self):
        data = (self.wood, self.clay, self.iron, self.progress1, self.progress2, self.progress_time, self.village_level[0], self.village_level[1], self.village_level[2], self.village_level[3], self.village_level[1], self.village_level[5])
        return data

    def get_population(self):
        pop = 0
        for building in range(len(self.village)):
            pop += v.calculate_population(self.village[building], self.village_level[building]-1)
        return pop
    
    def upgrade_avaliable(self, building_idx, level):
        population = self.farm - self.get_population()       
        if self.wood >= v.calculate_wood(self.village[building_idx], level) and self.clay >= v.calculate_clay(self.village[building_idx], level) and self.iron >= v.calculate_iron(self.village[building_idx], level) and population >= v.calculate_population(self.village[building_idx], level) and self.village_level[building_idx] < self.village[building_idx].maxlv and (self.progress1 == -1 or self.progress2 == -1):
            return True
        else:
            return False
        
    def sub_resources(self, building_idx, level):
        self.wood -= v.calculate_wood(self.village[building_idx], self.village_level[building_idx]+level)
        self.clay -= v.calculate_clay(self.village[building_idx], self.village_level[building_idx]+level)
        self.iron -= v.calculate_iron(self.village[building_idx], self.village_level[building_idx]+level)
        print(v.calculate_wood(self.village[building_idx], self.village_level[building_idx]+level), v.calculate_clay(self.village[building_idx], self.village_level[building_idx]+level),v.calculate_iron(self.village[building_idx], self.village_level[building_idx]+level))
        
    def add_to_progress(self, building_idx):
        if self.progress1 == -1:
            self.sub_resources(building_idx, 0)
            self.progress1 = building_idx
            self.start_progress = time.time()
        elif self.progress2 == -1:
            self.sub_resources(building_idx, 1)
            self.progress2 = building_idx
        else: print('Cant add to progress!')









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

# #Calculate the building speed
# def build_speed(b):
#     s = v.calculate_factor(village[0], 0)
#     t = v.calculate_time(village[b], 0)
#     return (s/100)*t

    
# #Process the progress
# def progress():
#     if PROGRESS[0] != -1:
#         if p_timer(build_speed(PROGRESS[0])):
#             add_lv(PROGRESS[0])
#             PROGRESS[0] = PROGRESS[1]
#             PROGRESS[1] = -1
#     if PROGRESS[1] != -1:
#             PROGRESS[3] = build_speed(PROGRESS[1])

# #Add a build to progress
# def add_to_progress(b):
#     if PROGRESS[0] == -1:
#         sub_resources(b, 1)
#         PROGRESS[0] = b
#         global P
#         P = time.time()
#     elif PROGRESS[1] == -1:
#         sub_resources(b, 2)
#         PROGRESS[1] = b
#     else: print('Cant add to progress!')
