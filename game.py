#Obelisk v.1.0
import time

WOOD = 0
CLAY = 0
IRON = 0
WAREHOUSE = 1000

def delay(t):
    s = time.time()
    while time.time() < s+t:
        pass

def production():
    global WOOD, CLAY, IRON
    WOOD = min(WOOD + 100, WAREHOUSE)
    CLAY = min(CLAY + 10, WAREHOUSE)
    IRON = min(IRON + 10, WAREHOUSE)

def run_game():
    while True:
        production()
        print(f'WOOD: {WOOD}/{WAREHOUSE}\
                CLAY: {CLAY}/{WAREHOUSE}\
                IRON: {IRON}/{WAREHOUSE}')
        
        delay(1)

        
if __name__=='__main__':
    run_game()