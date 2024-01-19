#v.1.4.3
import pygame
#import game as g
#import village as v
from graphics import Graphics
from network import Network

n = Network()

WIDTH = 800
HEIGHT = 600


graph = Graphics(WIDTH, HEIGHT)

def create_upgrade_btn():
    btns = []
    for i in range(len(graph.village)):
        btns.append([373, 40*i+55])
    return btns


def game_screen(btn, pos):
    graph.win.fill(graph.background_color)
    #graph.draw_progress(graph.win, graph.WIDTH-350, 60, 300, 10)
    graph.draw_production(graph.width-350, 180, 300, 10)
    graph.draw_warehouse(graph.width-350, 330, 300, 10)
    graph.draw_population(graph.width-350, 510, 300, 10)
    graph.draw_village(50, 40, 300, 32, 10)
    mouse_x = pos[0]
    mouse_y = pos[1]
    for index, btns in enumerate(btn):
        x = btns[0]
        y = btns[1]
        if x-15 <= mouse_x <= x+15 and y-15 <= mouse_y <= y+15:
            graph.draw_requeriments(index, mouse_x, mouse_y, 300, 10)
    pygame.display.update()

def login_screen(choice, input, username, password, password2):#btn, pos
    graph.win.fill(graph.background_color)
    title = 'OBELISK'
    graph.drawTextCenter(title, 130, (96, 48, 45), 5, 5, graph.width, graph.height/3)
    graph.drawTextCenter(title, 130, (125, 81, 15), 0, 0, graph.width, graph.height/3)


    graph.draw_login_menu(choice, input, username, password, password2, graph.width/2, graph.height/2, 300, 10)
    
    pygame.display.update()





def main():
    n.connect()                 #connect to the server
    upgrade_btn = create_upgrade_btn()
    clock = pygame.time.Clock()
    run = True
    logged = False
    

    
    active_choice = ''

    print(n.read())
    
    while run:
        if logged:
            clock.tick(60)
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    run = False
                    pygame.quit()  
                
                
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     mouse_x = pos[0]
                #     mouse_y = pos[1]
                #     for i, btns in enumerate(add_btn):
                #         x = btns[0]
                #         y = btns[1]
                #         if x-15 <= mouse_x <= x+15 and y-15 <= mouse_y <= y+15:
                #             if i == g.PROGRESS[0] or i == g.PROGRESS[1]: l = 2
                #             else: l = 1
                #             if g.can_add_lv(i, l):
                #                 g.add_to_progress(i)
                #                 break
            #wood, clay, iron, headquartes, timbercamp, claypit, ironmine, farm, warehouse = n.read_data()
            #n.send('read')
            graph.update(n.read_data())
            game_screen(upgrade_btn, pos)
            #game_screen(add_btn, pos)


        else:
            clock.tick(60)
            username = ''
            password = ''
            password2 = ''
            active_input = 'username'
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x = pos[0]
                    mouse_y = pos[1]
                    x = graph.width/2
                    y = graph.height/2
                    if x-350 <= mouse_x <= x-50 and y <= mouse_y <= y+150:
                        active_choice = 'register'
                        n.send(active_choice)
                    elif x+50 <= mouse_x <= x+350 and y <= mouse_y <= y+150:
                        active_choice = 'login'
                        n.send(active_choice)
                    print(n.read())
                
                if active_choice == 'login':
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run = False
                                pygame.quit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_TAB:
                                    active_input = 'password' if active_input == 'username' else 'username'
                                elif event.key == pygame.K_RETURN:
                                    if active_input == 'username':
                                        active_input = 'password'
                                    elif active_input == "password":
                                        n.send(username)
                                        print(n.read())
                                        n.send(password)
                                        c = n.read()
                                        if c == 'connected':
                                            print(c)      
                                            logged = True
                                            break
                    
                                        else:   
                                            n.send(active_choice)
                                            print(n.read())
                                            active_input = 'username'

                                elif event.key == pygame.K_BACKSPACE:
                                    if active_input == 'username':
                                        username = username[:-1]
                                    elif active_input == "password":
                                        password = password[:-1]
                                else:
                                    if active_input == 'username':
                                        username += event.unicode
                                    elif active_input == "password":
                                        password += event.unicode
                        if logged: break
                        login_screen(active_choice, active_input,  username, password, password2)


                if active_choice == 'register':
                    created = False
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run = False
                                pygame.quit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_TAB:
                                    if active_input == 'username':
                                        active_input = 'password' 
                                    elif active_input == 'password':
                                        active_input = 'password2' 
                                    else: active_input = 'username'
                                elif event.key == pygame.K_RETURN:
                                    if active_input == 'username':
                                        active_input = 'password'
                                    elif active_input == "password":
                                        active_input = 'password2'
                                    elif active_input == "password2":
                                        n.send(username)
                                        print(n.read())
                                        n.send(password)
                                        print(n.read())
                                        n.send(password2)
                                        c = n.read()
                                        if c == 'created':
                                            print(c)      
                                            created = True
                                            active_choice = ''
                                            break
                                        elif c == 'exists':
                                            print('username already in use')
                                            n.send(active_choice)
                                            print(n.read())
                                            active_input = 'username'
                                        else:   
                                            print('password dont match')
                                            n.send(active_choice)
                                            print(n.read())
                                            active_input = 'username'
                                        
                                elif event.key == pygame.K_BACKSPACE:
                                    if active_input == 'username':
                                        username = username[:-1]
                                    elif active_input == "password":
                                        password = password[:-1]
                                    elif active_input == "password2":
                                        password2 = password2[:-1]
                                else:
                                    if active_input == 'username':
                                        username += event.unicode
                                    elif active_input == "password":
                                        password += event.unicode
                                    elif active_input == "password2":
                                        password2 += event.unicode

                        if created: break
                        login_screen(active_choice, active_input,  username, password, password2)

            login_screen(active_choice, active_input, username, password, password2)
            









if __name__ == '__main__':
    main()