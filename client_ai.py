#v.1.0
import pygame
import village as v
from graphics import Graphics
from network import Network
import configurations as config
import neural_network as nn
import numpy as np

n = Network()                               #Start network

WIDTH = 800                                 #window width
HEIGHT = 600                                #windown height

graph = Graphics(WIDTH, HEIGHT)             #start graphics

def create_upgrade_btn():                   #create the upgrade buttons
    btns = []
    for i in range(len(v.village)):
        btns.append([373, 65+16+i*40])      #add the buttons to an array
    return btns

#draw the game screen
def game_screen(btn, pos):
    graph.win.fill(graph.background_color)                                                                                  #backgroud color
    graph.draw_points(graph.width-350, 10, 300, 10)                                                                         #draw the info
    graph.draw_progress(graph.width-350, 65, 300, 10)
    graph.draw_production(graph.width-350, 185, 300, 10)
    graph.draw_warehouse(graph.width-350, 335, 300, 10)
    graph.draw_population(graph.width-350, 515, 300, 10)
    graph.draw_village(50, 65, 300, 32, 10)
    mouse_x = pos[0]
    mouse_y = pos[1]
    for index, btns in enumerate(btn):
        x = btns[0]
        y = btns[1]
        if x-16 <= mouse_x <= x+16 and y-16 <= mouse_y <= y+16:
            graph.draw_requeriments(index, mouse_x, mouse_y, 300, 10)
    pygame.display.update()                                                                                                 #update the screen

#process and compile data recieved from server to the neural network work
def process_data(data):
    wood, clay, iron, progress1, progress2, progress_time, headquartes, timbercamp, claypit, ironmine, farm, warehouse = data
    
    wood = round(wood, 3)
    clay = round(clay, 3)
    iron = round(iron, 3)
    village_level = [int(headquartes), int(timbercamp), int(claypit), int(ironmine), int(farm), int(warehouse)]
    data = []
    pop = 0
    farm_f = v.calculate_factor(4, int(farm))

    for building in range(len(v.village)):                                              #Go Through all buildings
        if building == progress1 and building == progress2: lvl = 2           #check if they are in progress
        elif building == progress1 or building == progress2: lvl = 1
        else: lvl = 0
        pop += v.calculate_population(building, int(farm)+lvl)       #calculate and add the population of ea building to a varaiable
        
    population = farm_f - pop

    #compile data
    for building in range(len(v.village)):
        if building == progress1 and building == progress2: lvl = 3
        elif building == progress1 or building == progress2: lvl = 2
        else: lvl = 1

        remain_wood = wood - v.calculate_wood(building, village_level[building]+lvl) 
        remain_clay = clay - v.calculate_clay(building, village_level[building]+lvl)
        remain_iron = iron - v.calculate_iron(building, village_level[building]+lvl) 
        remain_population = population - (v.calculate_population(building,village_level[building]+lvl) - v.calculate_population(building, village_level[building]+lvl-1))
        _time = int(v.calculate_time(building, village_level[building]+lvl, village_level[0])/config.game_speed)
        remain_lv = v.village[building].max_lv - village_level[building]
 
        data.append([remain_wood, remain_clay, remain_iron, remain_population, _time, remain_lv]) #building

    return data

class Neural_Network:
    def __init__(self):
        #self.X = np.reshape(np.array(data), (6, 6, 1))
        self.Y = np.reshape([[0], [1], [2], [3], [4], [5]], (6, 1, 1))

        self.learning_rate = 0.1
        self.epochs = 0
        self.error = 0
        
        self.network = [
            nn.Dense(6,256),
            nn.Tanh(),
            nn.Dense(256,6),
            nn.Tanh()
        ]

    def train(self, data):
        X = np.reshape(np.array(data), (6, 6, 1))
        for x, y in zip(X, self.Y):
            #forward
            output = x
            for layer in self.network:
                output = layer.forward(output)

            #error
            self.error = nn.mse(y, output)

            #backward
            grad = nn.mse_prime(y, output)
            for layer in reversed(self.network):
                grad = layer.backward(grad, self.learning_rate)
        self.error /= len(x)
        self.epochs += 1     
        print('%d, error=%f >%d' %(self.epochs+1, self.error, np.argmax(output)))
        return np.argmax(output)


def main():

    connection = n.connect()                #connect to the server
    upgrade_btn = create_upgrade_btn()      #create the upgrade buttons
    clock = pygame.time.Clock()             #start game clock
    run = True
    logged = False

    
    active_choice = ''

    print(n.read())                                                                                 #read msg from server
    
    while run:
        if connection:                                                                              #execute if connected
            if logged:                                                                              #if logged run the game
                clock.tick(60)                                                                      #game fps
                pos = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:                                                   #close the game
                        run = False
                        pygame.quit()  

                n.send('-1')                                                                        #send a msg with no instructions
                data = n.read_data()        #data from the server
                graph.update(data)                                                         #read data from server and update client data
                
                
                upgrade = neural_network.train(process_data(data))
                #if graph.upgrade_avaliable(upgrade, graph.village_level[upgrade]):      #check is is possible upgrade
                #    n.send(str(upgrade))                                              #send an istruction to the server
                #    n.read_data()                                                   #read the return
                #print(upgrade)

                game_screen(upgrade_btn, pos)                                                       #update the game display
            
            
            
            else:                                                                                   #if not logged show the login/regist menu
                username = 'ai'
                password = '123'
                active_choice = 'login'

                n.send(active_choice)                                                   #send a msg with the choise to the server
                print(n.read())                                                             #read the return
   

                n.send(username)                                                    #send the username and password
                print(n.read())
                n.send(password)
                c = n.read()                                                        #read the return 
                if c == 'connected':                                                #if is connected, is logged in
                    print(c)      
                    logged = True 

                    neural_network = Neural_Network()       #Inicialize the neural network




if __name__ == '__main__':
    main()