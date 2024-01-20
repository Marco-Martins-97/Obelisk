class Headquartes:                                  # Building
    def __init__(self):
        self.name = 'Headquartes'                   # Name
        self.max_lv = 30                            # Max Level
        self.min_lv = 1                             # Nin Level
        # Base Upgrade Costs
        self.wood = 90                          
        self.clay = 80                          
        self.iron = 70                          
        self.population = 5                            
        self.factor = 95                        
        self.build_time = 900                      
        self.points = 5                         
        # Incrementing Factor
        self.wood_factor = 1.26                    
        self.clay_factor = 1.275
        self.iron_factor = 1.26
        self.population_factor = 1.17
        self.factor_factor = 0.953
        self.build_time_factor = 1.2
        self.points_factor = 1.1555


class TimberCamp:
    def __init__(self):
        self.name = 'Timber Camp'
        self.max_lv = 30
        self.min_lv = 1
        # Base Upgrade Costs
        self.wood = 50
        self.clay = 60
        self.iron = 40
        self.population = 5
        self.factor = 30
        self.build_time = 900
        self.points = 1
        # Incrementing Factor
        self.wood_factor = 1.25
        self.clay_factor = 1.275
        self.iron_factor = 1.245
        self.population_factor = 1.155
        self.factor_factor = 1.16313
        self.build_time_factor = 1.2
        self.points_factor = 1.2

        
class ClayPit:
    def __init__(self):
        self.name = 'Clay Pit'
        self.max_lv = 30
        self.min_lv = 1
        # Base Upgrade Costs
        self.wood = 65
        self.clay = 50
        self.iron = 40
        self.population = 10
        self.factor = 30
        self.build_time = 900
        self.points = 1
        # Incrementing Factor
        self.wood_factor = 1.27
        self.clay_factor = 1.265
        self.iron_factor = 1.24
        self.population_factor = 1.14
        self.factor_factor = 1.16313
        self.build_time_factor = 1.2
        self.points_factor = 1.2

        
class IronMine:
    def __init__(self):
        self.name = 'Iron Mine'
        self.max_lv = 30
        self.min_lv = 1
        # Base Upgrade Costs
        self.wood = 75
        self.clay = 65
        self.iron = 70
        self.population = 10
        self.factor = 30
        self.build_time = 1080
        self.points = 1
        # Incrementing Factor
        self.wood_factor = 1.252
        self.clay_factor = 1.275
        self.iron_factor = 1.24
        self.population_factor = 1.17
        self.factor_factor = 1.16313
        self.build_time_factor = 1.2
        self.points_factor = 1.2


class Farm:
    def __init__(self):
        self.name = 'Farm'
        self.max_lv = 30
        self.min_lv = 1
        # Base Upgrade Costs
        self.wood = 45
        self.clay = 40
        self.iron = 30
        self.population = 0
        self.factor = 240
        self.build_time = 1200
        self.points = 1
        # Incrementing Factor
        self.wood_factor = 1.3
        self.clay_factor = 1.32
        self.iron_factor = 1.29
        self.population_factor = 1
        self.factor_factor = 1.172103
        self.build_time_factor = 1.2
        self.points_factor = 1.1925

        
class Warehouse:
    def __init__(self):
        self.name = 'Warehouse'
        self.max_lv = 30
        self.min_lv = 1
        # Base Upgrade Costs
        self.wood = 60
        self.clay = 50
        self.iron = 40
        self.population = 0
        self.factor = 1000
        self.build_time = 1020
        self.points = 1
        # Incrementing Factor
        self.wood_factor = 1.265
        self.clay_factor = 1.27
        self.iron_factor = 1.245
        self.population_factor = 1.15
        self.factor_factor = 1.2294935
        self.build_time_factor = 1.2
        self.points_factor = 1.2


village = [Headquartes(), TimberCamp(), ClayPit(), IronMine(), Farm(), Warehouse()]                                 # Village array with all buidings
       
# Calculate wood costs
def calculate_wood(building_idx, lvl):
    return int((village[building_idx].wood * (village[building_idx].wood_factor ** (lvl - 1))))                     # duration = [build_time]*[build_time_factor]^(building_level] - 1)
    
# Calculate clay costs
def calculate_clay(building_idx, lvl):
    return int((village[building_idx].clay * (village[building_idx].clay_factor ** (lvl - 1))))

# Calculate iron costs
def calculate_iron(building_idx, lvl):
    return int((village[building_idx].iron * (village[building_idx].iron_factor ** (lvl - 1))))

# Calculate population costs
def calculate_population(building_idx, lvl):
    return int((village[building_idx].population * (village[building_idx].population_factor ** (lvl - 1))))

# Calculate the factor   
def calculate_factor(building_idx, lvl):
    return int((village[building_idx].factor * (village[building_idx].factor_factor ** (lvl - 1))))   

# Calculate the time to upgrade
def calculate_time(building_idx, lvl, hq_lv):
    return int((calculate_factor(0, hq_lv)/100) * (village[building_idx].build_time * (village[building_idx].build_time_factor ** (lvl - 1)))) 

# Calculate the points
def calculate_points(building_idx, lvl):
    return int((village[building_idx].points * (village[building_idx].points_factor ** (lvl - 1))))



# build = 5
# lv = 30
# print('W: ' + str(calculate_wood(build, lv)))
# print('C: ' + str(calculate_clay(build, lv)))
# print('I: ' + str(calculate_iron(build, lv)))
# print('P: ' + str(calculate_population(build, lv)))
# print('F: ' + str(calculate_factor(build, lv)))
# print('T: ' + str(calculate_time(build, lv, 1)))
# print('Pt: ' + str(calculate_points(build, lv)))

