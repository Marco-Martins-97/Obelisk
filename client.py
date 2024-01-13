import pygame
import game as g
import village as v


WIDTH = 800
HEIGHT = 600

BG_COL = (244, 228, 188)    #background color
BT_COL = (203, 171, 107)    #button color
BOR_COL = (125, 81, 15)     #border color
TEXT_COL = (96, 48, 45)     #text color
#colorless
BT_COL2 = (96, 96, 96)      #button color
BOR_COL2 = (0, 0, 0)        #border color
TEXT_COL2 = (200, 200, 200) #text color
TEXT_COL3 = (222, 0,42)     #text color

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Obelisk')
pygame.font.init()

#Text alignment
def drawTextC(win, t, s, c, x, y, w, h):
    font = pygame.font.SysFont('comicsans', s)
    text = font.render(str(t), 1, c)
    win.blit(text, (x + round(w/2)-round(text.get_width()/2), y + round(h/2)-round(text.get_height()/2)))
    
def drawTextL(win, t, s, c, x, y, h):
    font = pygame.font.SysFont('comicsans', s)
    text = font.render(str(t), 1, c)
    win.blit(text, (x, y + round(h/2)-round(text.get_height()/2)))

def drawTextR(win, t, s, c, x, y, w, h):
    font = pygame.font.SysFont('comicsans', s)
    text = font.render(str(t), 1, c)
    win.blit(text, (x + w -round(text.get_width()), y + round(h/2)-round(text.get_height()/2)))

#Shapes
def drawRoundRect(win, x, y, w, h, b):  
    pygame.draw.rect(win, (BOR_COL), (x, y+b, w, h-2*b))
    pygame.draw.rect(win, (BOR_COL), (x+b, y, w-2*b, h))
    pygame.draw.circle(win, BOR_COL, (x+b, y+b), b)
    pygame.draw.circle(win, BOR_COL, (x+w-b, y+b), b)
    pygame.draw.circle(win, BOR_COL, (x+b, y+h-b), b)
    pygame.draw.circle(win, BOR_COL, (x+w-b, y+h-b), b)
    pygame.draw.rect(win, (BT_COL), (x+3, y+3+b, w-6, h-6-2*b))
    pygame.draw.rect(win, (BT_COL), (x+3+b, y+3, w-6-2*b, h-6))
    pygame.draw.circle(win, BT_COL, (x+3+b, y+3+b), b)
    pygame.draw.circle(win, BT_COL, (x+3+w-6-b, y+3+b), b)
    pygame.draw.circle(win, BT_COL, (x+3+b, y+3+h-6-b), b)
    pygame.draw.circle(win, BT_COL, (x+3+w-6-b, y+3+h-6-b), b)

def drawCircle(win, brc, btc, x, y, b):
    pygame.draw.circle(win, brc, (x, y), b)
    pygame.draw.circle(win, btc, (x, y), b-3)

def drawCross(win, tc, x, y, b):
    pygame.draw.rect(win, (tc), (x+b/6, y+b/2-2, b/3*2, 4))
    pygame.draw.rect(win, (tc), (x+b/2-2, y+b/6, 4, b/3*2))

#Dashboards
def draw_progress(win, x, y, w, b):
    c = 3
    i = 30
    h = c*i
    tc= TEXT_COL
    drawRoundRect(win, x, y, w, h+5, b)
    drawTextC(win, 'PROGRESS', 20, tc, x, y+5, w, h/c)
    drawTextL(win, '1: ', 20, tc, x+20, y+i*1, h/c)
    if g.PROGRESS[0] != -1:
        drawTextL(win, g.village[g.PROGRESS[0]].name, 20, tc, x+40, y+i*1, h/c)
        drawTextR(win, int(g.PROGRESS[2]+1), 20, tc, x-20, y+i*1, w, h/c)
    else:
        drawTextL(win, '', 20, tc, x+40, y+i*1, h/c)
    drawTextL(win, '2: ', 20, tc, x+20, y+i*2, h/c)
    if g.PROGRESS[1] != -1:
        drawTextL(win, g.village[g.PROGRESS[1]].name, 20, tc, x+40, y+i*2, h/c)
        drawTextR(win, int(g.PROGRESS[3]+1), 20, tc, x-20, y+i*2, w, h/c)
    else:
        drawTextL(win, '', 20, tc, x+40, y+i*2, h/c)

def draw_production(win, x, y, w, b):
    c = 4
    i = 30
    h = c*i
    tc= TEXT_COL
    drawRoundRect(win, x, y, w, h+5, b)
    drawTextC(win, 'PRODUCTION', 20, tc, x, y+5, w, h/c)
    drawTextL(win, 'WOOD: ', 20, tc, x+20, y+i*1, h/c)
    drawTextR(win, g.WOOD_P, 20, tc, x-20, y+i*1, w, h/c)
    drawTextL(win, 'CLAY: ', 20, tc, x+20, y+i*2, h/c)
    drawTextR(win, g.CLAY_P, 20, tc, x-20, y+i*2, w, h/c)
    drawTextL(win, 'IRON: ', 20, tc, x+20, y+i*3, h/c)
    drawTextR(win, g.IRON_P, 20, tc, x-20, y+i*3, w, h/c)

def draw_warehouse(win, x, y, w, b):
    c = 5
    i = 30
    h = c*i
    tc= TEXT_COL
    drawRoundRect(win, x, y, w, h+5, b)
    drawTextC(win, 'WAREHOUSE', 20, tc, x, y+5, w, h/c)
    drawTextL(win, 'CAPACITY: ', 20, tc, x+20, y+i*1 , h/c)
    drawTextR(win, g.WAREHOUSE, 20, tc, x-20, y+i*1, w, h/c)
    drawTextL(win, 'WOOD: ', 20, tc, x+20, y+i*2, h/c)
    drawTextR(win, g.WOOD, 20, tc, x-20, y+i*2, w, h/c)
    drawTextL(win, 'CLAY: ', 20, tc, x+20, y+i*3, h/c)
    drawTextR(win, g.CLAY, 20, tc, x-20, y+i*3, w, h/c)
    drawTextL(win, 'IRON: ', 20, tc, x+20, y+i*4, h/c)
    drawTextR(win, g.IRON, 20, tc, x-20, y+i*4, w, h/c)

def draw_populçation(win, x, y, w, b):
    c = 2
    i = 30
    h = c*i
    tc= TEXT_COL
    drawRoundRect(win, x, y, w, h+5, b)
    drawTextC(win, 'FARM', 20, tc, x, y+5, w, h/c)
    drawTextL(win, 'POPULATION: ', 20, tc, x+20, y+i*1, h/c)
    drawTextR(win, g.POPULATION, 20, tc, x-20, y+i*1, w, h/c)

def draw_requeriments(win, ix, x, y, w, b):
    c = 6
    i = 30
    h = c*i
    wood = v.calculate_wood(g.village[ix])
    clay = v.calculate_clay(g.village[ix])
    iron = v.calculate_iron(g.village[ix])
    pop = v.calculate_next_pop(g.village[ix])
    t = int(g.build_speed(ix)+1)

    drawRoundRect(win, x, y, w, h+5, b)
    drawTextC(win, 'REQERIMENTS', 20, TEXT_COL, x, y+5, w, h/c)
    drawTextL(win, 'WOOD: ', 20, TEXT_COL, x+20, y+i*1, h/c)
    if g.WOOD < wood : tc = TEXT_COL3
    else: tc = TEXT_COL
    drawTextR(win, wood, 20, tc, x-20, y+i*1, w, h/c)
    drawTextL(win, 'CLAY: ', 20, TEXT_COL, x+20, y+i*2, h/c)
    if g.CLAY < clay : tc = TEXT_COL3
    else: tc = TEXT_COL
    drawTextR(win, clay, 20, tc, x-20, y+i*2, w, h/c)
    drawTextL(win, 'IRON: ', 20, TEXT_COL, x+20, y+i*3, h/c)
    if g.IRON < iron : tc = TEXT_COL3
    else: tc = TEXT_COL
    drawTextR(win, iron, 20, tc, x-20, y+i*3, w, h/c)
    drawTextL(win, 'POPULATION: ', 20, TEXT_COL, x+20, y+i*4, h/c)
    if g.POPULATION < pop : tc = TEXT_COL3
    else: tc = TEXT_COL
    drawTextR(win, pop, 20, tc, x-20, y+i*4, w, h/c)
    drawTextL(win, 'TIME: ', 20, TEXT_COL, x+20, y+i*5, h/c)
    drawTextR(win, t, 20, TEXT_COL, x-20, y+i*5, w, h/c)

def draw_village(win, x, y, w, h, b):
    tc= TEXT_COL
    for i in range(len(g.village)):
        #builds
        drawRoundRect(win, x, y * i + 40, w, h, b)
        drawTextC(win, g.village[i].name, 20, tc, x, y*i+40, w, h-6)
        #lv
        drawCircle(win, BOR_COL, BT_COL, x-h+7, y*i+40+h/2, h/2+3)
        drawTextC(win, g.village[i].lv, 20, tc, x-h+7, y*i+38, 0, h)
        if g.can_add_lv(i):
            #add button 
            drawCircle(win, BOR_COL, BT_COL, x+w+h-7, y*i+40+h/2, h/2+3)
            drawCross(win, TEXT_COL, x+w+h/2-7, y*i+40, h)
        else:
            #add button 
            drawCircle(win, BOR_COL2, BT_COL2, x+w+h-7, y*i+40+h/2, h/2+3)
            drawCross(win, TEXT_COL2, x+w+h/2-7, y*i+40, h)

def create_btn():
    btns = []
    for i in range(len(g.village)):
        btns.append([373, 40*i+55])
    return btns


def update_screen(btn, pos):
    win.fill(BG_COL)
    draw_progress(win, WIDTH-350, 60, 300, 10)
    draw_production(win, WIDTH-350, 180, 300, 10)
    draw_warehouse(win, WIDTH-350, 330, 300, 10)
    draw_populçation(win, WIDTH-350, 510, 300, 10)
    draw_village(win, 50, 40, 300, 30, 10)
    mouse_x = pos[0]
    mouse_y = pos[1]
    for i, btns in enumerate(btn):
        x = btns[0]
        y = btns[1]
        if x-15 <= mouse_x <= x+15 and y-15 <= mouse_y <= y+15:
            draw_requeriments(win, i, mouse_x, mouse_y, 300, 10)
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
                        if g.can_add_lv(i):
                            g.add_to_progress(i)
                            break


        g.run_game()
        update_screen(add_btn, pos)










if __name__ == '__main__':
    game()