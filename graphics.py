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
#others
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
    
def drawrectangle(win, x, y, w, h):
    pygame.draw.rect(win, ((0,0,0)), (x, y, w, h))
    pygame.draw.rect(win, ((255,255,255)), (x+3, y+3, w-6, h-6))



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
    
def draw_login_menu(win, c, ai, u, p, p2,  x, y, w, b):
    col = 4
    i = 30
    h = col*i
    tc= TEXT_COL
    drawRoundRect(win, x-w-50, y, w, h+5, b)
    drawRoundRect(win, x+50, y, w, h+5, b)
    if c == 'login':
        drawTextC(win, 'REGISTER', 40, tc, x-w-50, y+h/3, w, h/col)
        drawTextC(win, 'LOGIN', 20, tc, x+50, y+5, w, h/col)
        drawTextL(win, 'USERNAME: ', 20, tc, x+50+20, y+i*2, h/col)
        drawTextR(win, u, 20, tc, x+50-20, y+i*2, w, h/col)
        drawTextL(win, 'PASSWORD: ', 20, tc, x+50+20, y+i*3, h/col)
        drawTextR(win, p, 20, tc, x+50-20, y+i*3, w, h/col)
        if ai == 'username': 
            drawTextR(win, '<', 20, tc, x+60-20, y+i*2, w, h/col)
        else: 
            drawTextR(win, '<', 20, tc, x+60-20, y+i*3, w, h/col)
    elif c == 'register': 
        drawTextC(win, 'LOGIN', 40, tc, x+50, y+h/3, w, h/col)
        drawTextC(win, 'LOGIN', 20, tc, x-w-50, y+5, w, h/col)
        drawTextL(win, 'USERNAME: ', 20, tc, x-w-50+20, y+i*1, h/col)
        drawTextR(win, u, 20, tc, x-w-50-20, y+i*1, w, h/col)
        drawTextL(win, 'PASSWORD: ', 20, tc, x-w-50+20, y+i*2, h/col)
        drawTextR(win, p, 20, tc, x-w-50-20, y+i*2, w, h/col)
        drawTextL(win, 'PASSWORD: ', 20, tc, x-w-50+20, y+i*3, h/col)
        drawTextR(win, p2, 20, tc, x-w-50-20, y+i*3, w, h/col)
        if ai == 'username': 
            drawTextR(win, '<', 20, tc, x-w-40-20, y+i*1, w, h/col)
        elif ai == 'password': 
            drawTextR(win, '<', 20, tc, x-w-40-20, y+i*2, w, h/col)
        else: 
            drawTextR(win, '<', 20, tc, x-w-40-20, y+i*3, w, h/col)
    else:
        drawTextC(win, 'REGISTER', 40, tc, x-w-50, y+h/3, w, h/col)
        drawTextC(win, 'LOGIN', 40, tc, x+50, y+h/3, w, h/col)

   



























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
    if ix == g.PROGRESS[0] and ix == g.PROGRESS[1]: l = 3
    elif ix == g.PROGRESS[0] or ix == g.PROGRESS[1]: l = 2
    else: l = 1
    wood = v.calculate_wood(g.village[ix], l)
    clay = v.calculate_clay(g.village[ix], l)
    iron = v.calculate_iron(g.village[ix], l)
    pop = v.calculate_pop(g.village[ix], l)
    t = int(g.build_speed(ix)+l)

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
        if i == g.PROGRESS[0] or i == g.PROGRESS[1]: l = 2
        else: l = 1
        if g.can_add_lv(i, l):
            #add button 
            drawCircle(win, BOR_COL, BT_COL, x+w+h-7, y*i+40+h/2, h/2+3)
            drawCross(win, TEXT_COL, x+w+h/2-7, y*i+40, h)
        else:
            #add button 
            drawCircle(win, BOR_COL2, BT_COL2, x+w+h-7, y*i+40+h/2, h/2+3)
            drawCross(win, TEXT_COL2, x+w+h/2-7, y*i+40, h)

    