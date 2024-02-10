#v.1.6.4
import pygame
import village as v
from graphics import Graphics, Button
from network import Network

n = Network()                               #Start network

#WIDTH = 800                                 #window width
#HEIGHT = 600                                #windown height


#configs = [Width, Height, Auto-login]
default_configs = [0, False, 'username', 'password']

win_size = [[800, 600], [1280, 720], [1600, 900], [1920, 1080]]


def save_configs(configs, filename='client_configs.txt'):   #save the client configs in a file
    with open(filename, 'w') as file:
        for c in configs:
            file.write(f'{c}\n')
            print(f'saved: {c}')
            
    print('configs saved.')

def load_configs(filename='client_configs.txt'):            #load the client configs from a file
    configs = []
    try:
        with open (filename, 'r') as file:
            for line in file:
                configs.append(line.strip())
                
    except FileNotFoundError:
        save_configs(default_configs)

    print('configs loaded.')
    return configs

#save_configs(default_configs)
configs = load_configs()

width = int(win_size[int(configs[0])][0])
height = int(win_size[int(configs[0])][1])

graph = Graphics(width, height)             #start graphics

#draw the game screen
def game_screen(upgrade_btn):
    graph.win.fill(graph.background_color)                                                                                  #backgroud color
    graph.draw_top_bar()                                                                         #draw the info
    graph.draw_progress(graph.width-350, 65, 300, 10)
    graph.draw_production(graph.width-350, 185, 300, 10)
    graph.draw_warehouse(graph.width-350, 335, 300, 10)
    graph.draw_population(graph.width-350, 515, 300, 10)
    graph.draw_village_buildings(50, 65, 300, 32, 10)
    graph.draw_village_levels(23, 63, 18)
    graph.draw_village_upgrade_btns(356, 63, 18)
    for index, btn in enumerate(upgrade_btn):
        if btn.at_button():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            graph.draw_requeriments(index, mouse_x, mouse_y, 300, 10)
    pygame.display.update()                                                                                                 #update the screen

#Draw the connect screen
def connect_screen():
    graph.win.fill(graph.background_color)                                                                                                                     
    title = 'OBELISK'                                                                                                           #title
    graph.drawTextCenter(title, 130, (96, 48, 45), 5, 5, graph.width, graph.height/3)                                           #draw title shadow
    graph.drawTextCenter(title, 130, (125, 81, 15), 0, 0, graph.width, graph.height/3)                                          #draw title
    graph.draw_connect_menu(graph.width/2, graph.height/2, 300, 10)                                                             #draw the menu
    pygame.display.update()                                                                                                     #update the screen

#Draw the regist screen
def regist_screen(input, username, password, password2):
    graph.win.fill(graph.background_color)                                                                                                                     
    title = 'OBELISK'                                                                                                           #title
    graph.drawTextCenter(title, 130, (96, 48, 45), 5, 5, graph.width, graph.height/3)                                           #draw title shadow
    graph.drawTextCenter(title, 130, (125, 81, 15), 0, 0, graph.width, graph.height/3)                                          #draw title
    graph.draw_regist_menu(input, username, password, password2, graph.width/2, graph.height/2, 300, 10)               #draw the menu
    pygame.display.update()                                                                                                     #update the screen

#Draw the login screen
def login_screen(input, username, password):
    graph.win.fill(graph.background_color)                                                                                                                     
    title = 'OBELISK'                                                                                                           #title
    graph.drawTextCenter(title, 130, (96, 48, 45), 5, 5, graph.width, graph.height/3)                                           #draw title shadow
    graph.drawTextCenter(title, 130, (125, 81, 15), 0, 0, graph.width, graph.height/3)                                          #draw title
    graph.draw_login_menu(configs[1], input, username, password, graph.width/2, graph.height/2, 300, 10)                 #draw the menu
    pygame.display.update()                                                                                                     #update the screen

#Menus
def autologin():
    active_choice = 'login'
    username = configs[2]
    password = configs[3]

    while True:
        n.send(username)                                                    #send the username and password
        print(n.read())
        n.send(password)
        c = n.read()                                                        #read the return 
        if c == 'connected':                                                #if is connected, is logged in
            print(c)      
            return  True
                            
        else:                                                               #if not connectd , switch active choise to username, and repeat the prosess
            n.send(active_choice)
            print(n.read())

def login_menu():
    active_choice = 'login'
    logged = False
    username = ''
    password = ''
    active_input = 'username'
    autologin_button = Button(graph.width/2+300, (graph.height/2)+96, 32, 32)  
    while True:
        for event in pygame.event.get():                                        #wait for inputs
            if event.type == pygame.QUIT:                                       #close the game
                pygame.quit()
                break

            if autologin_button.pressed(event):
                if configs[1] == 'true':
                    configs[1] = 'false'
                else:
                    configs[1] = 'true'

            if event.type == pygame.KEYDOWN:                                                   
                if event.key == pygame.K_TAB:                                                   #if the tab key is pressed, switch the active choise beetween username and password 
                    active_input = 'password' if active_input == 'username' else 'username'
                elif event.key == pygame.K_RETURN:                                              #if the return key is pressed, and active choise is username, switch to password
                    if active_input == 'username':                                            
                        active_input = 'password'
                    elif active_input == "password":                                            #if the active choise is password and is not empty
                        if username != '' and password != '':
                            n.send(username)                                                    #send the username and password
                            print(n.read())
                            n.send(password)
                            c = n.read()                                                        #read the return 
                            if c == 'connected':                                                #if is connected, is logged in
                                print(c)      
                                logged = True 
                                break
                            
                            else:                                                               #if not connectd , switch active choise to username, and repeat the prosess
                                n.send(active_choice)
                                print(n.read())
                                active_input = 'username'

                elif event.key == pygame.K_BACKSPACE:                                           #delete character from username and password
                    if active_input == 'username':
                        username = username[:-1]
                    elif active_input == "password":
                        password = password[:-1]
                else:                                                                           #write character in username and password
                    if active_input == 'username':  
                        username += event.unicode
                    elif active_input == "password":
                        password += event.unicode
        if logged: 
            if configs[1] == 'true':
                configs[2] = username
                configs[3] = password
                save_configs(configs)
            return logged                                                                       #if logged exit the login menu
        login_screen(active_input, username, password)               #update the login menu

def regist_menu():
    active_choice = 'register'
    created = False
    username = ''
    password = ''
    password2 = ''
    active_input = 'username'
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:                                                   #if the tab key is pressed, switch the active choise beetween username and password and password2
                    if active_input == 'username':
                        active_input = 'password' 
                    elif active_input == 'password':
                        active_input = 'password2' 
                    else: active_input = 'username'
                elif event.key == pygame.K_RETURN:                                              #if the return key is pressed, and active choise is username, switch to password, is password switch to password2
                    if active_input == 'username':
                        active_input = 'password'
                    elif active_input == "password":
                        active_input = 'password2'
                    elif active_input == "password2":
                        if username != '' and password != '' and password2 != '':               #if the active choise is password2 and none choise is empty
                            n.send(username)                                                    #send the username and password and password2
                            print(n.read()) 
                            n.send(password)
                            print(n.read())
                            n.send(password2)
                            c = n.read()                                                        #read the return 
                            if c == 'created':                                                  #if the return is created, exit the regist menu
                                print(c)      
                                created = True
                                break
                            elif c == 'exists':                                                 #if the username already exists, repeat
                                print('username already in use')            
                                n.send(active_choice)
                                print(n.read())
                                active_input = 'username'
                            else:                                                               #if the password and password2 dont match, repeat
                                print('password dont match')
                                n.send(active_choice)
                                print(n.read())
                                active_input = 'username'
                                            
                elif event.key == pygame.K_BACKSPACE:                                           #delete character from username and passwords
                    if active_input == 'username':
                        username = username[:-1]
                    elif active_input == "password":
                        password = password[:-1]
                    elif active_input == "password2":
                        password2 = password2[:-1]
                else:                                                                           #write character in username and passwords
                    if active_input == 'username':
                        username += event.unicode
                    elif active_input == "password":
                        password += event.unicode
                    elif active_input == "password2":
                        password2 += event.unicode

        if created: return created                                                                       #if account created exit the regist menu
        regist_screen(active_input,  username, password, password2)               #update the login menu

def reconnect_menu():
    graph.win.fill(graph.background_color)
    msg = 'Fail to Connect to the Server...'
    graph.drawTextCenter(msg, 40, (96, 48, 45), 0, 0, graph.width, graph.height/3)                                              #draw msg
    graph.drawRoundRect(graph.width/2-125, graph.height/2, 250, 32, 10)                                                         #draw a button
    graph.drawTextCenter('RECONNECT', 20, graph.text_color, graph.width/2-125, graph.height/2, 250, 32)                         #button text
    pygame.display.update()

    reconnect_button = Button(graph.width/2-125, graph.height/2, 150, 32)                                                       #Create the button
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                                                                       #close the game
                pygame.quit()  

            if reconnect_button.pressed(event):
                print('Trying Reconnect...')
                if n.connect():
                    return True
                else:
                    print('Reconnect Fail!!')   

def config_menu():
    menu = True
    size_choise = int(configs[0])
    autologin = configs[1]
    #btn = Button(x, y, w, h)
    exit_button = Button(graph.width-105, graph.height-40, 100, 35)
    save_button = Button(graph.width-210, graph.height-40, 100, 35)
    restore_button = Button(graph.width-315, graph.height-40, 100, 35)

    x, y, width, height, margin = 20, 20, 200, 32, 40

    win_size_btns = graph.create_buttons(x, y, width, height, margin, 4)
    autologin_btn = Button(graph.width-50, y, 32, 32)  


    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                                   #close the game
                pygame.quit()  
                break
            
            #buttons
            if exit_button.pressed(event):
                print('exit')
                menu = False


            if save_button.pressed(event):
                print('save')
                configs[0] = size_choise
                configs[1] = autologin
                save_configs(configs)

            
            if restore_button.pressed(event):
                print('default')
                save_configs(default_configs)


            #windown size (width x height)
            for idx, btn in enumerate(win_size_btns):
                if btn.pressed(event):
                    size_choise = idx
                    break
            
            #auto-login (on/off)
            if autologin_btn.pressed(event):
                if autologin == 'true':
                    autologin = 'false'
                else:
                    autologin = 'true'





        graph.win.fill(graph.background_color) 
        graph.draw_config_menu(size_choise, autologin)
        pygame.display.update()

def map_menu():
    menu = True
    logout_button = Button(graph.width-105, 5, 100, 35)                             
    config_button = Button(graph.width-210, 5, 100, 35)
    village_button = Button(graph.width-315, 5, 100, 35)

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                                   #close the game
                pygame.quit()  
                break
            
            #buttons
            if village_button.pressed(event):
                menu = False

            if config_button.pressed(event):
                config_menu()
                    
            if logout_button.pressed(event):
                menu = False


        graph.win.fill(graph.map_background_color) 
        graph.draw_map()
        pygame.display.update()
    





def main():
    connection = n.connect()                #connect to the server
    clock = pygame.time.Clock()             #start game clock
    logged = False
    last_state = 0
    
    upgrade_button = graph.create_buttons(356, 63, 36, 36, 40, len(v.village))                             #create the upgrade buttons
    #menu buttons
    logout_button = Button(graph.width-105, 5, 100, 35)                             
    config_button = Button(graph.width-210, 5, 100, 35)
    map_button = Button(graph.width-315, 5, 100, 35)
    #connection buttons
    regist_button = Button(graph.width/2-350, graph.height/2, 300, 133)   
    login_button = Button(graph.width/2+50, graph.height/2, 300, 133)
    
    print(n.read())                                                                                 #read msg from server
    
    while True:
        clock.tick(60)                                                                      #game fps
        if connection:                                                                              #execute if connected
            if logged:                                                                              #if logged run the game
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:                                                   #close the game
                        pygame.quit()  
                        break
                  
                    for index, btn in enumerate(upgrade_button):
                        if btn.pressed(event):
                            if graph.upgrade_avaliable(index, graph.village_level[index]):      #check is is possible upgrade
                                n.send(str(index))                                              #send an istruction to the server
                                n.read_data()                                                   #read the return
                                break
                    
                    if map_button.pressed(event):
                        map_menu()

                    if config_button.pressed(event):
                        config_menu()
                    
                    if logout_button.pressed(event):
                        print('logout')
                        configs[1] = 'false'
                        save_configs(configs)
                        logged = False


                n.send('-1')                                                                        #send a msg with no instructions
                data, state = n.read_data()                                                         #read data from server

                if last_state != state:                                                             #update in the same speed the game run
                    last_state = state
                    
                graph.update(data)                                                                  #update client data
                game_screen(upgrade_button)                                                       #update the game display

            else:                                                                                   #if not logged show the login/regist menu
                active_choice = ''
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:                                                   #close the game
                        pygame.quit()
                        break

                    if regist_button.pressed(event):                                            #if the regist buttos is pressed
                        active_choice = 'register'
                        n.send(active_choice)                                                   #send a msg with the choise to the server
                        print(n.read())

                    elif login_button.pressed(event):                                            #if the login button is presses
                        active_choice = 'login'     
                        n.send(active_choice)                                                   #send a msg with the choise to the server
                        print(n.read())                                                             #read the return
                    
                    if active_choice == 'login':                                                    #if the login button was pressed 
                        if configs[1] == 'true':
                            logged = autologin()
                        else:    
                            logged = login_menu()
                        if logged: break
                        

                    if active_choice == 'register':
                        created = regist_menu()
                        if created: 
                            active_choice = ''
                            break     
                        
                connect_screen()                            #update the login menu
                
                 
        else:
           connection = reconnect_menu()








if __name__ == '__main__':
    main()