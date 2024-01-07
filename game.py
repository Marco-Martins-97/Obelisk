#Obelisk v.1.1
import time
import village as v

WOOD = 0
CLAY = 0
IRON = 0
WAREHOUSE = v.calculate_factor(v.Warehouse())


def production():
    global WOOD, CLAY, IRON
    w = v.calculate_factor(v.TimberCamp())
    c = v.calculate_factor(v.ClayPit())
    i = v.calculate_factor(v.IronMine())
    WOOD = min(WOOD + w, WAREHOUSE)
    CLAY = min(CLAY + c, WAREHOUSE)
    IRON = min(IRON + i, WAREHOUSE)

def run_game():
    while True:
        production()
        print(f'WOOD: {WOOD}/{WAREHOUSE}\
                CLAY: {CLAY}/{WAREHOUSE}\
                IRON: {IRON}/{WAREHOUSE}')
        
        time.sleep(1)

        
if __name__=='__main__':
    run_game()