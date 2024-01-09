#Obelisk v.1.4
import time
import village as v

#Resources
WOOD = 0
CLAY = 0
IRON = 0
#Factor
WOOD_P = 0
CLAY_P = 0
IRON_P = 0
WAREHOUSE = 0
#Timers
S = time.time()
SA = time.time()
#Village buildings
village = [v.TimberCamp(), v.ClayPit(), v.IronMine(), v.Warehouse()]


#Save data to a file
def save_database(village, filename='village.txt'):
    with open (filename, 'w') as file:
        file.write(f'{WOOD},{CLAY},{IRON}\n')           #write resources
        for build in village:
            file.write(f'{build.lv}\n')                 #write building levels
    print('Database Saved.')

#Load data from a file
def load_database(filename='village.txt'):
    try:
        with open (filename, 'r') as file:
            global WOOD, CLAY, IRON
            resources = file.readline().strip().split(',')      #Read data from te file
            WOOD, CLAY, IRON = map(int, resources)              #Assigns data to variables
            for i, line in enumerate(file):
                build = int(line.strip())                       #Read data from te file
                village[i].lv = build                           #Assigns data to variables
    except FileNotFoundError:
        pass

#Delay timer
def delay(t):
    global S
    if time.time() > t+S:
        S = time.time()
        return True
    
#Autosave timer
def autosave(t):
    global SA
    if time.time() > t+SA:
        SA = time.time()
        return True

#Production
def production():
    global WOOD, CLAY, IRON                     #call globar variables
    WOOD = min(WOOD + WOOD_P, WAREHOUSE)        #Assigns too WOOD the WOOD+PRODUCTION if is smaller than WAREHOUSE
    CLAY = min(CLAY + CLAY_P, WAREHOUSE)
    IRON = min(IRON + IRON_P, WAREHOUSE)

#Subtracts the resources needed to increase the lv from resources
def sub_resources(b):
    global WOOD, CLAY, IRON
    WOOD -= v.calculate_wood(village[b])
    CLAY -= v.calculate_clay(village[b])
    IRON -= v.calculate_iron(village[b])

#Add 1 lv to a building
def add_lv(b):
    sub_resources(b)
    village[b].lv += 1
    update()

#Return if is possible add a lv to a building
def can_add_lv(b):
    global WOOD, CLAY, IRON 
    if WOOD >= v.calculate_wood(village[b]) and CLAY >= v.calculate_clay(village[b]) and IRON >= v.calculate_iron(village[b]) and village[b].lv < village[b].maxlv:
        return True
    else:
        return False

#Update the factor
def update():
    global WOOD_P, CLAY_P, IRON_P, WAREHOUSE
    WOOD_P = v.calculate_factor(village[0])
    CLAY_P = v.calculate_factor(village[1])
    IRON_P = v.calculate_factor(village[2])
    WAREHOUSE = v.calculate_factor(village[3])





#Run the game

load_database()                     #Loads the data
update()                            #Update
def run_game():

    if delay(1):                    #Game speed
        production()                      
    if autosave(5):                 #Save frequency
        save_database(village)      #Save the data

