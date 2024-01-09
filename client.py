import pygame
import game as g


WIDTH = 800
HEIGHT = 600

BG_COL = (244, 228, 188)    #background color
BT_COL = (203, 171, 107)    #button color
BOR_COL = (125, 81, 15)     #border color
TEXT_COL = (96, 48, 45)     #text color

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Obelisk')
pygame.font.init()

#Text alignment
def drawTextC(win, t, s, x, y, w, h):
    font = pygame.font.SysFont('comicsans', s)
    text = font.render(str(t), 1, TEXT_COL)
    win.blit(text, (x + round(w/2)-round(text.get_width()/2), y + round(h/2)-round(text.get_height()/2)))
    
def drawTextL(win, t, s, x, y, h):
    font = pygame.font.SysFont('comicsans', s)
    text = font.render(str(t), 1, TEXT_COL)
    win.blit(text, (x, y + round(h/2)-round(text.get_height()/2)))

def drawTextR(win, t, s, x, y, w, h):
    font = pygame.font.SysFont('comicsans', s)
    text = font.render(str(t), 1, TEXT_COL)
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

def drawCircle(win, x, y, b):
    pygame.draw.circle(win, BOR_COL, (x, y), b)
    pygame.draw.circle(win, BT_COL, (x, y), b-3)


#Dashboards
def draw_production(win, x, y, w, b):
    c = 4
    i = 30
    h = c*i
    drawRoundRect(win, x, y, w, h+5, b)
    drawTextC(win, 'PRODUCTION', 20, x, y+5, w, h/c)
    drawTextL(win, 'WOOD: ', 20, x+20, y+i*1, h/c)
    drawTextR(win, g.WOOD_P, 20, x-20, y+i*1, w, h/c)
    drawTextL(win, 'CLAY: ', 20, x+20, y+i*2, h/c)
    drawTextR(win, g.CLAY_P, 20, x-20, y+i*2, w, h/c)
    drawTextL(win, 'IRON: ', 20, x+20, y+i*3, h/c)
    drawTextR(win, g.IRON_P, 20, x-20, y+i*3, w, h/c)

def draw_warehouse(win, x, y, w, b):
    c = 5
    i = 30
    h = c*i
    drawRoundRect(win, x, y, w, h+5, b)
    drawTextC(win, 'WAREHOUSE', 20, x, y+5, w, h/c)
    drawTextL(win, 'CAPACITY: ', 20, x+20, y+i*1 , h/c)
    drawTextR(win, g.WAREHOUSE, 20, x-20, y+i*1, w, h/c)
    drawTextL(win, 'WOOD: ', 20, x+20, y+i*2, h/c)
    drawTextR(win, g.WOOD, 20, x-20, y+i*2, w, h/c)
    drawTextL(win, 'CLAY: ', 20, x+20, y+i*3, h/c)
    drawTextR(win, g.CLAY, 20, x-20, y+i*3, w, h/c)
    drawTextL(win, 'IRON: ', 20, x+20, y+i*4, h/c)
    drawTextR(win, g.IRON, 20, x-20, y+i*4, w, h/c)

def draw_village(win, x, y, w, h, b):
    for i in range(len(g.village)):
        #builds
        drawRoundRect(win, x, y * i + 40, w, h, b)
        drawTextC(win, g.village[i].name, 20, x, y*i+40, w, h-6)
        #lv
        drawCircle(win, x-h+7, y*i+40+h/2, h/2+3)
        drawTextC(win, g.village[i].lv, 20, x-h+7, y*i+38, 0, h)


def update_screen():
    win.fill(BG_COL)
    draw_production(win, WIDTH-350, 150, 300, 10)
    draw_warehouse(win, WIDTH-350, 300, 300, 10)
    draw_village(win, 50, 40, 300, 30, 10)
    pygame.display.update()






def game():

    run = True
    clock = pygame.time.Clock()
    update_screen()
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()




        g.run_game()
        update_screen()










if __name__ == '__main__':
    game()