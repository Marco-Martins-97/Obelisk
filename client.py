#v.1.6.13
import pygame
import village as v
from graphics import Graphics, Button
from network import Network

n = Network()                               #Start network

#WIDTH = 800                                 #window width
#HEIGHT = 600                                #windown height

USERNAME = ''
PASSWORD = ''

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
        print('configs loaded.')
        
                
    except FileNotFoundError:
        save_configs(default_configs)
        return default_configs

    return configs

def unpack_user_cords(data):
    cords = {}
    l = 0
    while l < len(data):
        #cords[user] = [x, y, x_pos, y_pos, dif_x, dif_y]
        cords[data[l]] = [int(data[l+1]), int(data[l+2]), int(data[l+1]), int(data[l+2]), 0, 0]
        l += 3
    return cords

def center_at_user(users_cords, user):
    #get the diffenece to the center os screen
    dif_x = graph.width/2 - users_cords[user][0]*graph.chunk_size
    dif_y = graph.height/2 - users_cords[user][1]*graph.chunk_size
    #apply the diffence to all objects
    for i in users_cords:
        users_cords[i][2] = dif_x + users_cords[i][0]*graph.chunk_size
        users_cords[i][3] = dif_y + users_cords[i][1]*graph.chunk_size

#Create Buttons
def create_buttons(x, y, width, height, margin, length):
    btns = []
    for i in range(length):
        btns.append(Button(x, y + i * margin, width, height ))
    return btns

def create_map_users_buttons(users_cords):
    btns = []
    for user, _ in users_cords.items():
        btns.append(Button(users_cords[user][2]-graph.chunk_size/2, users_cords[user][3]-graph.chunk_size/2, graph.chunk_size, graph.chunk_size ))
    return btns





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
def auto_login():
    conn = n.read()
    username = configs[2]
    password = configs[3]
    logged = False
    if conn == 'error':
        return False, False #connection, logged
    else:
        while True:
            print(n.send_read(username))
            account = n.send_read(password)                                                        #read the return 
                                
            if account == 'connected':  #login                                                #if the return is created, exit the regist menu
                print(account) 
                global USERNAME, PASSWORD
                USERNAME, PASSWORD = username, password  
                return True, True          #connection, logged                    
                #logged = True
                #break
            elif account == 'fail':                                                 #if the username already exists, repeat
                print('Username or Password Incorrect')  
                print(n.send_read('login')) 

            else:                                                               #if the password and password2 dont match, repeat
                print('connection lost !')
                return False, False #connection, logged
    #return True, logged

def login_menu():
    conn = n.read()
    username = ''
    password = ''
    logged = False
    active_input = 'username'
    autologin_button = Button(graph.width/2+300, (graph.height/2)+96, 32, 32)
    regist_button = Button(graph.width/2-350, graph.height/2, 300, 133)
    if conn == 'error':
        return False, False #connection, logged
    else:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if regist_button.pressed(event):
                    print(n.send_read('username'))
                    account = n.send_read('password')
                    if account == 'fail':  
                        #n.send('login')  
                        print('login > connect')                                             #if the username already exists, repeat 
                        return True, False #connection, created
                    else:                                                               #if the password and password2 dont match, repeat
                        print('connection lost !')
                        return False, False #connection, created

                #    #print('regist')
                #    n.send('username')
                #    print(n.read()) 
                #    n.send('password')
                #    print(n.read())
                #    return True, logged
                
                if autologin_button.pressed(event): #auto-login
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
                        elif active_input == "password": 
                            if username != '' and password != '':               #if the active choise is password2 and none choise is empty
                                
                                print(n.send_read(username))
                                account = n.send_read(password)
                                
                                if account == 'connected':  #login                                                #if the return is created, exit the regist menu
                                    print(account) 
                                    if configs[1] == 'true':
                                        configs[2] = username
                                        configs[3] = password
                                        save_configs(configs)
                                    global USERNAME, PASSWORD
                                    USERNAME, PASSWORD = username, password
                                    return True, True          #connection, logged
                                #    logged = True      
                                #    break
                                elif account == 'fail':                                                 #if the username already exists, repeat
                                    print('Username or Password Incorrect')  
                                    print(n.send_read('login'))          
                                #    n.send('login')
                                #    print(n.read())
                                    active_input = 'username'
                                else:                                                               #if the password and password2 dont match, repeat
                                    print('connection lost !')
                                    return False, False #connection, logged

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

            login_screen(active_input, username, password)               #update the login menu

    #return True, logged

def regist_menu():
    conn = n.read()
    username = ''
    password = ''
    password2 = ''
    created = False
    active_input = 'username'
    login_button = Button(graph.width/2+50, graph.height/2, 300, 133)
    if conn == 'error':
        return False, False #connection, created
    else:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if login_button.pressed(event):
                    print(n.send_read('username'))
                    print(n.send_read('password'))
                    account = n.send_read('password2')
                    if account == 'incorrect':  
                        #n.send('login')  
                        print('regist > connect')                                             #if the username already exists, repeat 
                        return True, False #connection, created
                    else:                                                               #if the password and password2 dont match, repeat
                        print('connection lost !')
                        return False, False #connection, created
                #    #print('login')
                #    n.send('username')
                #    print(n.read()) 
                #    n.send('password')
                #    print(n.read())
                #    n.send('password2')
                #    print(n.read())
                #    return True, created
                
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
                                print(n.send_read(username))
                                print(n.send_read(password))
                                account = n.send_read(password2)                                                        #read the return 
                                
                                if account == 'created':  #login                                                #if the return is created, exit the regist menu
                                    print(account) 
                                    #n.send('login')
                                    #print(n.read())
                                    #n.send(username)                                                    #send the username and password
                                    #print(n.read())
                                    #n.send(password)
                                    #print(n.read()) 
                                    return True, True          #connection, created
                                    #created = True
                                    #break

                                elif account == 'exists':                                                 #if the username already exists, repeat
                                    print('username already in use')  
                                    print(n.send_read('register'))           
                                    #n.send('register')
                                    #print(n.read())
                                    active_input = 'username'
                                elif account == 'incorrect':                                                 #if the username already exists, repeat
                                    print('password dont match')            
                                    print(n.send_read('register')) 
                                    #n.send('register')
                                    #print(n.read())
                                    active_input = 'username'
                                else:                                                               #if the password and password2 dont match, repeat
                                    print('connection lost !')
                                    return False, False #connection, created
                                    
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

                
            regist_screen(active_input,  username, password, password2)

    #return True, created

def reconnect_menu(logged):
    graph.win.fill(graph.background_color)
    graph.drawTextCenter('Lost Connection to the Server...', 40, (96, 48, 45), 0, 0, graph.width, graph.height/2)                                              #draw msg
    graph.drawTextCenter('Trying to Reconnect to the Server...', 20, (96, 48, 45), 0, 0, graph.width, graph.height)                                              #draw msg
    #graph.drawRoundRect(graph.width/2-125, graph.height/2, 250, 32, 10)                                                         #draw a button
    #graph.drawTextCenter('RECONNECT', 20, graph.text_color, graph.width/2-125, graph.height/2, 250, 32)                         #button text
    pygame.display.update()

   # reconnect_button = Button(graph.width/2-125, graph.height/2, 150, 32)                                                       #Create the button
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                                                                       #close the game
                pygame.quit()  

            #if reconnect_button.pressed(event):
                
        if logged:#reconnect
            print('Trying Reconnect...')
            if n.connect():
                while True:
                    server = n.read()
                    print(server)
                    if server == 'connection':
                        n.send('login')
                        print(n.read())
                        n.send(USERNAME)
                        print(n.read()) 
                        n.send(PASSWORD)
                        account = n.read()
                        if account == 'connected':  #login
                            print(account)
                            break
                return True
            else:
                print('Reconnect Failed!!') 
                return False

        else:    
            print('Trying Reconnect...')
            if n.connect():

                return True
            else:
                print('Reconnect Failed!!') 
                return False

def config_menu():
    menu = True
    size_choise = int(configs[0])
    #autologin = configs[1]
    #btn = Button(x, y, w, h)
    exit_button = Button(graph.width-105, graph.height-40, 100, 35)
    save_button = Button(graph.width-210, graph.height-40, 100, 35)
    restore_button = Button(graph.width-315, graph.height-40, 100, 35)

    x, y, width, height, margin = 20, 20, 200, 32, 40

    win_size_btns = create_buttons(x, y, width, height, margin, 4)
    #autologin_btn = Button(graph.width-50, y, 32, 32)  


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
                #configs[1] = autologin
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
            #if autologin_btn.pressed(event):
            #    if autologin == 'true':
            #        autologin = 'false'
            #    else:
            #        autologin = 'true'





        graph.win.fill(graph.background_color) 
        graph.draw_config_menu(size_choise)
        pygame.display.update()

def map_menu():
    menu = True
    #buttons
    logout_button = Button(graph.width-105, 5, 100, 35)                             
    center_button = Button(graph.width-105, graph.height-40, 100, 35)                             
    config_button = Button(graph.width-210, 5, 100, 35)
    village_button = Button(graph.width-315, 5, 100, 35)
    #state
    last_state = 0
    #users cords
    users_cords = unpack_user_cords(n.send_read_data('map_cords'))
    #drag n drop
    grab = False
    mouse_x, mouse_y = 0, 0
    center_at_user(users_cords, USERNAME)
    #buttons
    #user_buttons = create_map_users_buttons(users_cords)


    while menu:
        server = n.send_read('map')     #get data
        print(f'Client: {server}')


        if server == 'error':
            return False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                                   #close the game
                pygame.quit()  
                break
            
            #buttons
            if village_button.pressed(event):
                menu = False
                return True

            if config_button.pressed(event):
                config_menu()
                    
            #if logout_button.pressed(event):
            #    menu = False
            
            if center_button.pressed(event):
                #users_cords[USERNAME][2], users_cords[USERNAME][3] = users_cords[USERNAME][0], users_cords[USERNAME][1]
                center_at_user(users_cords, USERNAME)
                pass
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for user in users_cords:
                    users_cords[user][4] = mouse_x - users_cords[user][2]
                    users_cords[user][5] = mouse_y - users_cords[user][3]
                grab = True
                break

            if event.type == pygame.MOUSEBUTTONUP:
                grab = False
                #user_buttons = create_map_users_buttons(users_cords)
                

            if grab:
                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for user in users_cords:
                        users_cords[user][2] = mouse_x - users_cords[user][4]
                        users_cords[user][3] = mouse_y - users_cords[user][5]



        #if last_state != state:                                                             #update in the same speed the game run
        #    last_state = state
        #    print(state)

        graph.draw_map(users_cords, USERNAME)
        #for b in user_buttons:
        #        b.draw(graph.win)
    
def play():
    upgrade_buttons = create_buttons(356, 63, 36, 36, 40, len(v.village))                             #create the upgrade buttons
    #menu buttons
    logout_button = Button(graph.width-105, 5, 100, 35)                             
    config_button = Button(graph.width-210, 5, 100, 35)
    map_button = Button(graph.width-315, 5, 100, 35)

    graph.game_speed = int(n.read())
    print(graph.game_speed)
    playing = True
    last_state = 0
                
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                                   #close the game
                pygame.quit()  
                break
                        
            for idx, btn in enumerate(upgrade_buttons):
                if btn.pressed(event):
                    if graph.upgrade_avaliable(idx, graph.village_level[idx]):      #check is is possible upgrade    
                        n.send('upgrade')
                        print(n.read())
                        n.send(str(idx))                                              #send an istruction to the server   
                        break

            #if logout_button.pressed(event):
            # print(n.send_read('logout')) 
            #    n.send('logout')
                            
            #    configs[1] = 'false'
             #   save_configs(configs)
                #logged = False
                #connection = False
                #break

            #    logged, playing = False, False
            #    print(n.read())
            #    break

            if config_button.pressed(event):
                config_menu()
                        
            if map_button.pressed(event):
                conn = map_menu()
                if not conn:
                    return False, True

        #server = n.send_read('main')     
        server = n.send_read_state_time_data('main')  
        state, time, data = server   
        print(f'Client: {server}')
        #print(s)


        if server == 'error':
            return False, True #Connection, Logged

        #elif server == 'loggedout':
        #    print('loggedout')
        #    return False, False #Connection, Logged


        #if last_state != state:                                                             #update in the same speed the game run
        #    last_state = state
        #    print(state)

        graph.update(time, data)
        game_screen(upgrade_buttons) 
    



def main():
    connection = n.connect()                #connect to the server
    clock = pygame.time.Clock()             #start game clock
    logged = False
    last_state = 0
        
    #connection buttons
    regist_button = Button(graph.width/2-350, graph.height/2, 300, 133)   
    login_button = Button(graph.width/2+50, graph.height/2, 300, 133)
    
    print(n.read())                                                                                #read msg from server    
    while True:
        clock.tick(60)                                                                      #game fps
        if connection == False:
            print(f'Failed to connect to: {n.addr}')  
            connection = reconnect_menu(logged)
        else:                                                                              #execute if connected
            if not logged:
                    
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:                                                   #close the game
                        pygame.quit()
                        break

                    if regist_button.pressed(event):                                            #if the regist buttos is pressed
                        n.send('register')                                            #send a msg with the choise to the server
                        print('connect > regist') 
                        connection, created = regist_menu()
                        break
                        #if connection and not created:
                        #    print('l')
                        #    n.send('login')
                        #    break
                        #print(connection, created)

                    elif login_button.pressed(event):                                            #if the login button is presses   
                        n.send('login')                                                 #send a msg with the choise to the server
                        print('connect > login') 
                        if configs[1] == 'true':
                            connection, logged = auto_login()
                        else:    
                            connection, logged = login_menu()
                        break
                        #if connection and not logged:
                        #    print('r')
                        #    n.send('register') 
                        #    break

                connect_screen()                            #update the login menu
                
            else:   
                connection, logged = play()
                    

                    







if __name__ == '__main__':
    main()