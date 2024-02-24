#Obelisk v.1.10.4
from datetime import datetime, timedelta
import village as v

class Game:
    def __init__(self, data, game_speed):
        logout_time, wood, clay, iron, progress1, progress2, progress_time, headquartes, timbercamp, claypit, ironmine, farm, warehouse = data           #unpack the data
        
        self.village_level = [int(headquartes), int(timbercamp), int(claypit), int(ironmine), int(farm), int(warehouse)]
        self.game_speed = game_speed             #Get the game speed
        
        self.wood = wood
        self.clay = clay
        self.iron = iron

        self.wood_p = v.calculate_factor(1, self.village_level[1]) * self.game_speed    #calculate the building factors
        self.clay_p = v.calculate_factor(2, self.village_level[2]) * self.game_speed
        self.iron_p = v.calculate_factor(3, self.village_level[3]) * self.game_speed
        self.farm = v.calculate_factor(4, self.village_level[4])
        self.warehouse = v.calculate_factor(5, self.village_level[5])

        self.start_delay = datetime.now()                  #start the timers  
        
        self.progress1 = int(progress1)
        self.progress2 = int(progress2)
        
        self.progress_time = datetime.now()                     #if is any building in progress , get the time it stated else get the atual time
        if self.progress1 != -1:
            self.progress_time = progress_time

        #PROPGRESS AND RESOURCES IN OFFLINE TIME

        #calculate offline time
        offline_time = datetime.now() - logout_time             #time from the last logout to login
        offline_seconds = offline_time.total_seconds()          #offline time in seconds

        if self.progress1 != -1:    #in case of one building in progress
            #building time - time beetween start and the login
            progress1_time_left_seconds = v.calculate_time(self.progress1, self.village_level[self.progress1]+1, self.village_level[0])/self.game_speed - ((datetime.now() - self.progress_time).total_seconds() - offline_seconds)

            if progress1_time_left_seconds < offline_seconds:                                       #in case the build is complete
                time_after_progress1_finish = offline_seconds - progress1_time_left_seconds         #the time left after the building is finished

                self.production(progress1_time_left_seconds)                                        #add the resources until the first build finish contruct
                self.progress_countdown()                                                           #update the buildings

                if self.progress1 != -1:  #in case of one building in progress
                    self.progress_time = progress_time + timedelta(seconds=progress1_time_left_seconds) #update progress time //start progress time + first building time
                    #building time - time beetween start and the login
                    progress2_time_left_seconds = v.calculate_time(self.progress1, self.village_level[self.progress1]+1, self.village_level[0])/self.game_speed - ((datetime.now() - self.progress_time).total_seconds() - time_after_progress1_finish)
                    
                    if progress2_time_left_seconds < time_after_progress1_finish:                                   #in case the build is complete  
                        time_after_progress2_finish = time_after_progress1_finish - progress2_time_left_seconds     #the time left after the building is finished

                        self.production(progress2_time_left_seconds)                                                #add the resources until the second build finish contruct
                        self.progress_countdown()                                                                   #update the buildings
                        self.production(time_after_progress2_finish)                                                #add the resources after the second build finish contruct

                    else:
                        self.production(time_after_progress1_finish)        #add the resources after the first building finish contruct and the second isnt finished
                else:
                    self.production(time_after_progress1_finish)            #add the resources after the first building finish contruct and there is no second     
            else:
                self.production(offline_seconds)                            #add the resources if the first building isnt finished
        else:
            self.production(offline_seconds)                                #add the resources if there isnt any building in progress

  
    #Update the calculated values
    def update(self):
        self.wood_p = v.calculate_factor(1, self.village_level[1]) * self.game_speed
        self.clay_p = v.calculate_factor(2, self.village_level[2]) * self.game_speed
        self.iron_p = v.calculate_factor(3, self.village_level[3]) * self.game_speed
        self.farm = v.calculate_factor(4, self.village_level[4])
        self.warehouse = v.calculate_factor(5, self.village_level[5])

    #Resources Production
    def production(self, time):
        sw,sc,si = self.wood, self.clay, self.iron 
        self.wood = min(self.wood + (self.wood_p/3600) * time, self.warehouse)        #Assigns too WOOD the WOOD+PRODUCTION*TIME if is smaller than WAREHOUSE
        self.clay = min(self.clay + (self.clay_p/3600) * time, self.warehouse)
        self.iron = min(self.iron + (self.iron_p/3600) * time, self.warehouse)
        fw,fc,fi = self.wood, self.clay, self.iron
        print(f'WOOD: {sw} + {self.wood_p/3600:.3f} x {time} ({(self.wood_p/3600)*time}) = {fw}')
        print(f'CLAY: {sc} + {self.clay_p/3600:.3f} x {time} ({(self.clay_p/3600)*time}) = {fc}')
        print(f'IRON: {si} + {self.iron_p/3600:.3f} x {time} ({(self.iron_p/3600)*time}) = {fi}')


    #Game ticks
    def delay(self, time):
        if datetime.now() - self.start_delay > timedelta(seconds=time):
            self.start_delay = datetime.now()
            return True
    
    #Pack the data
    def get_data(self):
        data = (self.wood, self.clay, self.iron, self.progress1, self.progress2, self.progress_time, self.village_level[0], self.village_level[1], self.village_level[2], self.village_level[3], self.village_level[4], self.village_level[5])
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
            self.progress_time = datetime.now()       #update the timer
        elif self.progress2 == -1:
            self.sub_resources(building_idx, 2)     #subtract the resources
            self.progress2 = building_idx           #put the building in the progress
        else: print('Cant add to progress!')

    #Process the progress
    def progress_countdown(self):
        if self.progress1 != -1:
            if (datetime.now() - self.progress_time).total_seconds() > (v.calculate_time(self.progress1, self.village_level[self.progress1]+1, self.village_level[0])/self.game_speed):  #Checks if progress has ended
                self.village_level[self.progress1] += 1     #Increases level by 1
                self.progress1 = self.progress2             #Put the progress2 in the progress1
                self.progress_time = datetime.now()
                self.progress2 = -1                         #remove from progress2
                self.update()                               #upfate the values
