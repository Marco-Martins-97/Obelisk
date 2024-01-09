#Obelisk v.1.3
import time
import village as v

#Resources
WOOD = 0
CLAY = 0
IRON = 0
#Factor
WAREHOUSE = v.calculate_factor(v.Warehouse())
WOOD_P = v.calculate_factor(v.TimberCamp())
CLAY_P = v.calculate_factor(v.ClayPit())
IRON_P = v.calculate_factor(v.IronMine())
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

#Loads the data
load_database()

#Run the game
def run_game():

    if delay(1):                 #Game speed
        production()                      
    if autosave(5):                #Save frequency
        save_database(village)      #Save the data
