#Obelisk v.1.9.4
import time
import village as v
import configurations as config

class Game:
    def __init__(self, data):
        wood, clay, iron, progress1, progress2, progress_time, headquartes, timbercamp, claypit, ironmine, farm, warehouse = data           #unpack the data
        self.wood = float(wood)
        self.clay = float(clay)
        self.iron = float(iron)

        self.progress1 = int(progress1)
        self.progress2 = int(progress2)
        self.progress_time = int(progress_time)

        self.village_level = [int(headquartes), int(timbercamp), int(claypit), int(ironmine), int(farm), int(warehouse)]

        self.wood_p = 0
        self.clay_p = 0
        self.iron_p = 0
        self.farm = 0
        self.warehouse = 0

        self.start_delay = time.time()                  #start the timers
        self.start_autosave = time.time()
        self.start_progress = time.time()

        self.game_speed = config.game_speed             #Get the game speed

        self.start_progress = (self.progress_time - v.calculate_time(self.progress1, self.village_level[self.progress1], self.village_level[0])/self.game_speed) + time.time()          #load the remain time from database and apply it to progress
        self.update()
        
    #Update the calculated values
    def update(self):
        self.wood_p = v.calculate_factor(1, self.village_level[1]) * self.game_speed
        self.clay_p = v.calculate_factor(2, self.village_level[2]) * self.game_speed
        self.iron_p = v.calculate_factor(3, self.village_level[3]) * self.game_speed
        self.farm = v.calculate_factor(4, self.village_level[4])
        self.warehouse = v.calculate_factor(5, self.village_level[5])

    #Resources Production
    def production(self):
        self.wood = min(self.wood + self.wood_p/3600, self.warehouse)        #Assigns too WOOD the WOOD+PRODUCTION if is smaller than WAREHOUSE
        self.clay = min(self.clay + self.clay_p/3600, self.warehouse)
        self.iron = min(self.iron + self.iron_p/3600, self.warehouse)
        
    #Game ticks
    def delay(self, _time):
        if time.time() > _time + self.start_delay:
            self.start_delay = time.time()
            return True

    #Autosave timer
    def autosave(self, _time):
        if time.time() > _time+self.start_autosave:
            self.start_autosave = time.time()
            return True
        
    #Progress1 timer
    def progress_timer(self, _time):
        if time.time() > _time + self.start_progress:
            self.start_progress = time.time()
            return True
        self.progress_time = (self.start_progress + _time) - time.time()        #save the time left
    
    #Pack the data
    def get_data(self):
        data = (self.wood, self.clay, self.iron, self.progress1, self.progress2, int(self.progress_time), self.village_level[0], self.village_level[1], self.village_level[2], self.village_level[3], self.village_level[4], self.village_level[5])
        return data

    #Calculate the population used
    def get_population(self):
        pop = 0
        for building in range(len(v.village)):                                          #Go Through all buildings
            if building == self.progress1 and building == self.progress2: lvl = 2       #check if they are in progress
            elif building == self.progress1 or building == self.progress2: lvl = 1
            else: lvl = 0
            pop += v.calculate_population(building, self.village_level[building]+lvl)   #calculate and add the population of ea building to a varaiable
            #print(f'{building}: {pop}')
        return pop
    
    #Check if can upgrade the building
    def upgrade_avaliable(self, building_idx, level):
        population = self.farm - self.get_population()                                                                                      #Calculates the remaining population
        if building_idx == self.progress1 or building_idx == self.progress2: lvl = 2                                                        #Check if they are in progress
        else: lvl = 1   
        if (self.wood >= v.calculate_wood(building_idx, level+lvl)                                                                          #Check if have the necessary wood for the upgrade
            and self.clay >= v.calculate_clay(building_idx, level+lvl)                                                                      #Check if have the necessary clay for the upgrade
            and self.iron >= v.calculate_iron(building_idx, level+lvl)                                                                      #Check if have the necessary iron for the upgrade
            and population >= (v.calculate_population(building_idx, level+lvl)-v.calculate_population(building_idx, level+lvl-1))           #Check if have the necessary population for the upgrade
            and self.village_level[building_idx]+lvl-1 < v.village[building_idx].max_lv                                                     #Check if it's below max_lv
            and (self.progress1 == -1 or self.progress2 == -1)):                                                                            #Checks if have a free space in the progress
            return True
        else:
            return False
    
    #subtract the necessary resources to upgrade the building
    def sub_resources(self, building_idx, level):
        self.wood -= v.calculate_wood(building_idx, self.village_level[building_idx]+level)
        self.clay -= v.calculate_clay(building_idx, self.village_level[building_idx]+level)
        self.iron -= v.calculate_iron(building_idx, self.village_level[building_idx]+level)

    #Add the building to progress
    def add_to_progress(self, building_idx):
        if self.progress1 == -1:
            self.sub_resources(building_idx, 1)     #subtract the resources
            self.progress1 = building_idx           #put the building in the progress
            self.start_progress = time.time()       #update the timer
        elif self.progress2 == -1:
            self.sub_resources(building_idx, 2)     #subtract the resources
            self.progress2 = building_idx           #put the building in the progress
        else: print('Cant add to progress!')

    #Process the progress
    def progress_countdown(self):
        if self.progress1 != -1:
            if self.progress_timer(v.calculate_time(self.progress1, self.village_level[self.progress1]+1, self.village_level[0])/self.game_speed):  #Checks if progress has ended
                self.village_level[self.progress1] += 1     #Increases level by 1
                self.progress1 = self.progress2             #Put the progress2 in the progress1
                self.progress2 = -1                         #remove from progress2
                self.update()                               #upfate the values