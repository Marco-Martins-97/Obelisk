#Obelisk v.1.2
import time
import village as v

WOOD = 0
CLAY = 0
IRON = 0
WAREHOUSE = v.calculate_factor(v.Warehouse())
WOOD_P = v.calculate_factor(v.TimberCamp())
CLAY_P = v.calculate_factor(v.ClayPit())
IRON_P = v.calculate_factor(v.IronMine())


def production():
    global WOOD, CLAY, IRON
    WOOD = min(WOOD + WOOD_P, WAREHOUSE)
    CLAY = min(CLAY + CLAY_P, WAREHOUSE)
    IRON = min(IRON + IRON_P, WAREHOUSE)

def run_game():

    production()
        #print(f'WOOD: {WOOD}/{WAREHOUSE}\
        #        CLAY: {CLAY}/{WAREHOUSE}\
        #        IRON: {IRON}/{WAREHOUSE}')
        
    #time.sleep(1)

        
#if __name__=='__main__':
#    run_game()