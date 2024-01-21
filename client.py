#v.1.5.4
import pygame
import village as v
from graphics import Graphics
from network import Network

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

#Draw the login screen
def login_screen(choice, input, username, password, password2):
    graph.win.fill(graph.background_color)                                                                                                                     
    title = 'OBELISK'                                                                                                           #title
    graph.drawTextCenter(title, 130, (96, 48, 45), 5, 5, graph.width, graph.height/3)                                           #draw title shadow
    graph.drawTextCenter(title, 130, (125, 81, 15), 0, 0, graph.width, graph.height/3)                                          #draw title
    graph.draw_login_menu(choice, input, username, password, password2, graph.width/2, graph.height/2, 300, 10)                 #draw the menu
    pygame.display.update()                                                                                                     #update the screen

#Draw the reconnect screen
def reconnect_screen():
    graph.win.fill(graph.background_color)
    msg = 'Fail to Connect to the Server...'
    graph.drawTextCenter(msg, 40, (96, 48, 45), 0, 0, graph.width, graph.height/3)                                              #draw msg
    graph.drawRoundRect(graph.width/2-125, graph.height/2, 250, 32, 10)                                                         #draw a button
    graph.drawTextCenter('RECONNECT', 20, graph.text_color, graph.width/2-125, graph.height/2, 250, 32)                         #button text
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                                                                       #close the game
                pygame.quit()  
                                            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                mouse_x = pos[0]
                mouse_y = pos[1]            
                if graph.width/2-125 <= mouse_x <= graph.width/2+125 and graph.height/2-125 <= mouse_y <= graph.height/2+125:   #try connect if press the button
                    if n.connect():
                        return True

    





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
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x = pos[0]
                        mouse_y = pos[1]
                        for index, btns in enumerate(upgrade_btn):
                            x = btns[0]
                            y = btns[1]
                            if x-15 <= mouse_x <= x+15 and y-15 <= mouse_y <= y+15:                 #if a upgrade button is pressed
                                if graph.upgrade_avaliable(index, graph.village_level[index]):      #check is is possible upgrade
                                    n.send(str(index))                                              #send an istruction to the server
                                    n.read_data()                                                   #read the return
                                    break
                n.send('-1')                                                                        #send a msg with no instructions
                graph.update(n.read_data())                                                         #read data from server and update client data
                game_screen(upgrade_btn, pos)                                                       #update the game display
            else:                                                                                   #if not logged show the login/regist menu
                clock.tick(60)
                username = ''
                password = ''
                password2 = ''
                active_input = 'username'
                pos = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:                                                   #close the game
                        run = False
                        pygame.quit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x = pos[0]
                        mouse_y = pos[1]
                        x = graph.width/2
                        y = graph.height/2
                        if x-350 <= mouse_x <= x-50 and y <= mouse_y <= y+150:                      #if the regist buttos is pressed
                            active_choice = 'register'
                            n.send(active_choice)                                                   #send a msg with the choise to the server
                        elif x+50 <= mouse_x <= x+350 and y <= mouse_y <= y+150:                    #if the login button is presses
                            active_choice = 'login'     
                            n.send(active_choice)                                                   #send a msg with the choise to the server
                        print(n.read())                                                             #read the return
                    
                    if active_choice == 'login':                                                    #if the login button was pressed 
                        while True:
                            for event in pygame.event.get():                                        #wait for inputs
                                if event.type == pygame.QUIT:                                       #close the game
                                    run = False
                                    pygame.quit()
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
                            if logged: break                                                                        #if logged exit the login menu
                            login_screen(active_choice, active_input,  username, password, password2)               #update the login menu


                    if active_choice == 'register':
                        created = False
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    run = False
                                    pygame.quit()
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
                                                    active_choice = ''
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

                            if created: break                                                                       #if account created exit the regist menu
                            login_screen(active_choice, active_input,  username, password, password2)               #update the login menu

                login_screen(active_choice, active_input, username, password, password2)                            #update the login menu
                
        else:
           connection = reconnect_screen()








if __name__ == '__main__':
    main()