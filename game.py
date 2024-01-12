#Obelisk v.1.7
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
FARM = 0
WAREHOUSE = 0
POPULATION = 0
#Timers
S = time.time()
SA = time.time()
P = time.time()

#Progress
PROGRESS = [None, None, 0, 0]

#Village buildings
village = [v.Headquartes(), v.TimberCamp(), v.ClayPit(), v.IronMine(), v.Farm(), v.Warehouse()]


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
    
#Progress 1 timer
def p_timer(t):
    global P
    if time.time() > t+P:
        P = time.time()
        return True
    PROGRESS[2] = (P + t) - time.time()

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
    village[b].lv += 1
    update()

#Calculate the building speed
def build_speed(b):
    s = v.calculate_factor(village[0])
    t = v.calculate_time(village[b])
    return (s/100)*t

#Return if is possible add a lv to a building
def can_add_lv(b):
    global WOOD, CLAY, IRON 
    if WOOD >= v.calculate_wood(village[b]) and CLAY >= v.calculate_clay(village[b]) and IRON >= v.calculate_iron(village[b]) and POPULATION >= get_next_pop(b) and village[b].lv < village[b].maxlv and (PROGRESS[0] == None or PROGRESS[1] == None):
        return True
    else:
        return False
    
#Process the progress
def progress():
    if PROGRESS[0] is not None:
        if p_timer(build_speed(PROGRESS[0])):
            add_lv(PROGRESS[0])
            PROGRESS[0] = PROGRESS[1]
            PROGRESS[1] = None
    if PROGRESS[1] is not None:
            PROGRESS[3] = build_speed(PROGRESS[1])

#Add a build to progress
def add_to_progress(b):
    if PROGRESS[0] == None:
        sub_resources(b)
        PROGRESS[0] = b
        global P
        P = time.time()
    elif PROGRESS[1] == None:
        sub_resources(b)
        PROGRESS[1] = b
    else: print('Cant add to progress!')

#Return the actual population
def get_pop():
    pop = 0
    for b in range(len(village)):
        pop += v.calculate_pop(village[b])
    return pop

#Return the next population
def get_next_pop(b):
    return v.calculate_next_pop(village[b])

#Update the factor
def update():
    global WOOD_P, CLAY_P, IRON_P, FARM, WAREHOUSE, POPULATION
    WOOD_P = v.calculate_factor(village[1])
    CLAY_P = v.calculate_factor(village[2])
    IRON_P = v.calculate_factor(village[3])
    FARM = v.calculate_factor(village[4])
    WAREHOUSE = v.calculate_factor(village[5])
    POPULATION = FARM - get_pop()





#Run the game

load_database()                     #Loads the data
update()                            #Update
def run_game():

    progress()
    if delay(1):                    #Game speed
        production()                      
    if autosave(5):                 #Save frequency
        save_database(village)      #Save the data