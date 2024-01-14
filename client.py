#v.1.1
import pygame
import game as g
import village as v
import graphics as graph
from network import Network

n = Network()
n.connect()                 #connectto the server
print(n.read())




def create_btn():
    btns = []
    for i in range(len(g.village)):
        btns.append([373, 40*i+55])
    return btns


def update_screen(btn, pos):
    graph.win.fill(graph.BG_COL)
    graph.draw_progress(graph.win, graph.WIDTH-350, 60, 300, 10)
    graph.draw_production(graph.win, graph.WIDTH-350, 180, 300, 10)
    graph.draw_warehouse(graph.win, graph.WIDTH-350, 330, 300, 10)
    graph.draw_populçation(graph.win, graph.WIDTH-350, 510, 300, 10)
    graph.draw_village(graph.win, 50, 40, 300, 30, 10)
    mouse_x = pos[0]
    mouse_y = pos[1]
    for i, btns in enumerate(btn):
        x = btns[0]
        y = btns[1]
        if x-15 <= mouse_x <= x+15 and y-15 <= mouse_y <= y+15:
            graph.draw_requeriments(graph.win, i, mouse_x, mouse_y, 300, 10)
    pygame.display.update()






def game():
    add_btn = create_btn()
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x = pos[0]
                mouse_y = pos[1]
                for i, btns in enumerate(add_btn):
                    x = btns[0]
                    y = btns[1]
                    if x-15 <= mouse_x <= x+15 and y-15 <= mouse_y <= y+15:
                        if i == g.PROGRESS[0] or i == g.PROGRESS[1]: l = 2
                        else: l = 1
                        if g.can_add_lv(i, l):
                            g.add_to_progress(i)
                            break


        g.run_game()
        update_screen(add_btn, pos)










if __name__ == '__main__':
    game()