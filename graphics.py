import pygame
#import game as g
import village as v


#BG_COL = (244, 228, 188)    #background color
#BT_COL = (203, 171, 107)    #button color
#BOR_COL = (125, 81, 15)     #border color
#TEXT_COL = (96, 48, 45)     #text color
#colorless
BT_COL2 = (96, 96, 96)      #button color
BOR_COL2 = (0, 0, 0)        #border color
TEXT_COL2 = (200, 200, 200) #text color
#others
TEXT_COL3 = (222, 0,42)     #text color




class Graphics:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.win = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Obelisk')
        pygame.font.init()

        self.font = 'comicsans'

        self.background_color = (244, 228, 188)
        self.border_color = (125, 81, 15)
        self.button_color = (203, 171, 107)
        self.text_color = (96, 48, 45)

        self.wood_p = v.calculate_factor(v.TimberCamp(), v.TimberCamp().lv-1)
        self.clay_p = v.calculate_factor(v.ClayPit(), v.ClayPit().lv-1)
        self.iron_p = v.calculate_factor(v.IronMine(), v.IronMine().lv-1)

        self.warehouse = v.calculate_factor(v.Warehouse(), v.Warehouse().lv-1)

        self.wood = 0
        self.clay = 0
        self.iron = 0
        self.population = 100
        

    def update(self, wood, clay, iron):
        self.wood = wood
        self.clay = clay
        self.iron = iron

    #Text alignment
    def drawTextCenter(self, text, size, color, x, y, width, height):
        font = pygame.font.SysFont(self.font, size)
        text = font.render(str(text), 1, color)
        self.win.blit(text, (x + round(width/2)-round(text.get_width()/2), y + round(height/2)-round(text.get_height()/2)))

    def drawTextLeft(self, text, size, color, x, y, height):
        font = pygame.font.SysFont(self.font, size)
        text = font.render(str(text), 1, color)
        self.win.blit(text, (x, y + round(height/2)-round(text.get_height()/2)))

    def drawTextRight(self, text, size, color, x, y, width, height):
        font = pygame.font.SysFont(self.font, size)
        text = font.render(str(text), 1, color)
        self.win.blit(text, (x + width -round(text.get_width()), y + round(height/2)-round(text.get_height()/2)))


    def drawRoundRect(self, x, y, width, height, radius):  
        pygame.draw.rect(self.win, (self.border_color), (x, y+radius, width, height-2*radius))
        pygame.draw.rect(self.win, (self.border_color), (x+radius, y, width-2*radius, height))
        pygame.draw.circle(self.win, self.border_color, (x+radius, y+radius), radius)
        pygame.draw.circle(self.win, self.border_color, (x+width-radius, y+radius), radius)
        pygame.draw.circle(self.win, self.border_color, (x+radius, y+height-radius), radius)
        pygame.draw.circle(self.win, self.border_color, (x+width-radius, y+height-radius), radius)
        pygame.draw.rect(self.win, (self.button_color), (x+3, y+3+radius, width-6, height-6-2*radius))
        pygame.draw.rect(self.win, (self.button_color), (x+3+radius, y+3, width-6-2*radius, height-6))
        pygame.draw.circle(self.win, self.button_color, (x+3+radius, y+3+radius), radius)
        pygame.draw.circle(self.win, self.button_color, (x+3+width-6-radius, y+3+radius), radius)
        pygame.draw.circle(self.win, self.button_color, (x+3+radius, y+3+height-6-radius), radius)
        pygame.draw.circle(self.win, self.button_color, (x+3+width-6-radius, y+3+height-6-radius), radius)
    
    
    #Dashboards
    def draw_production(self, x, y, width, radius):
        columns = 4
        column_height = 32
        height = columns*column_height
        text_color = self.text_color
        self.drawRoundRect(x, y, width, height+5, radius)
        self.drawTextCenter('PRODUCTION', 20, text_color, x, y+5, width, column_height)
        self.drawTextLeft('WOOD: ', 20, text_color, x+20, y+column_height*1, column_height)
        self.drawTextRight(self.wood_p, 20, text_color, x-20, y+column_height*1, width, column_height)
        self.drawTextLeft('CLAY: ', 20, text_color, x+20, y+column_height*2, height/columns)
        self.drawTextRight(self.clay_p, 20, text_color, x-20, y+column_height*2, width, column_height)
        self.drawTextLeft('IRON: ', 20, text_color, x+20, y+column_height*3, height/columns)
        self.drawTextRight(self.iron_p, 20, text_color, x-20, y+column_height*3, width, column_height)


    def draw_warehouse(self, x, y, width, radius):
        columns = 5
        column_height = 32
        height = columns*column_height
        text_color = self.text_color
        self.drawRoundRect(x, y, width, height+5, radius)
        self.drawTextCenter('WAREHOUSE', 20, text_color, x, y+5, width, column_height)
        self.drawTextLeft('CAPACITY: ', 20, text_color, x+20, y+column_height*1 , column_height)
        self.drawTextRight(self.warehouse, 20, text_color, x-20, y+column_height*1, width, column_height)
        self.drawTextLeft('WOOD: ', 20, text_color, x+20, y+column_height*2, column_height)
        self.drawTextRight(self.wood, 20, text_color, x-20, y+column_height*2, width, column_height)
        self.drawTextLeft('CLAY: ', 20, text_color, x+20, y+column_height*3, column_height)
        self.drawTextRight(self.clay, 20, text_color, x-20, y+column_height*3, width, column_height)
        self.drawTextLeft('IRON: ', 20, text_color, x+20, y+column_height*4, column_height)
        self.drawTextRight(self.iron, 20, text_color, x-20, y+column_height*4, width, column_height)


    def draw_populçation(self, x, y, width, radius):
        columns = 2
        column_height = 32
        height = columns*column_height
        text_color = self.text_color
        self.drawRoundRect(x, y, width, height+5, radius)
        self.drawTextCenter('FARM', 20, text_color, x, y+5, width, column_height)
        self.drawTextLeft('POPULATION: ', 20, text_color, x+20, y+column_height*1, column_height)
        self.drawTextRight(self.population, 20, text_color, x-20, y+column_height*1, width, column_height)


    def draw_login_menu(self, choice, input, username, password, password2,  x, y, width, radius):
        columns = 4
        column_height = 32
        height = columns*column_height
        text_color = self.text_color
        self.drawRoundRect(x-width-50, y, width, height+5, radius)
        self.drawRoundRect(x+50, y, width, height+5, radius)
        if choice == 'login':
            self.drawTextCenter('REGISTER', 40, text_color, x-width-50, y+height/3, width, column_height)
            self.drawTextCenter('LOGIN', 20, text_color, x+50, y+5, width, column_height)
            self.drawTextLeft('USERNAME: ', 20, text_color, x+50+20, y+column_height*2, column_height)
            self.drawTextRight(username, 20, text_color, x+50-20, y+column_height*2, width, column_height)
            self.drawTextLeft('PASSWORD: ', 20, text_color, x+50+20, y+column_height*3, column_height)
            self.drawTextRight(password, 20, text_color, x+50-20, y+column_height*3, width, column_height)
            if input == 'username': 
                self.drawTextRight('<', 20, text_color, x+60-20, y+column_height*2, width, column_height)
            else: 
                self.drawTextRight('<', 20, text_color, x+60-20, y+column_height*3, width, column_height)
        elif choice == 'register': 
            self.drawTextCenter('LOGIN', 40, text_color, x+50, y+height/3, width, column_height)
            self.drawTextCenter('LOGIN', 20, text_color, x-width-50, y+5, width, column_height)
            self.drawTextLeft('USERNAME: ', 20, text_color, x-width-50+20, y+column_height*1, column_height)
            self.drawTextRight(username, 20, text_color, x-width-50-20, y+column_height*1, width, column_height)
            self.drawTextLeft('PASSWORD: ', 20, text_color, x-width-50+20, y+column_height*2, column_height)
            self.drawTextRight(password, 20, text_color, x-width-50-20, y+column_height*2, width, column_height)
            self.drawTextLeft('PASSWORD: ', 20, text_color, x-width-50+20, y+column_height*3, column_height)
            self.drawTextRight(password2, 20, text_color, x-width-50-20, y+column_height*3, width, column_height)
            if input == 'username': 
                self.drawTextRight('<', 20, text_color, x-width-40-20, y+column_height*1, width, column_height)
            elif input == 'password': 
                self.drawTextRight('<', 20, text_color, x-width-40-20, y+column_height*2, width, column_height)
            else: 
                self.drawTextRight('<', 20, text_color, x-width-40-20, y+column_height*3, width, column_height)
        else:
            self.drawTextCenter('REGISTER', 40, text_color, x-width-50, y+height/3, width, column_height)
            self.drawTextCenter('LOGIN', 40, text_color, x+50, y+height/3, width, column_height)








'''
    


#Shapes
    
def drawrectangle(win, x, y, w, h):
    pygame.draw.rect(win, ((0,0,0)), (x, y, w, h))
    pygame.draw.rect(win, ((255,255,255)), (x+3, y+3, w-6, h-6))




def drawCircle(win, brc, btc, x, y, b):
    pygame.draw.circle(win, brc, (x, y), b)
    pygame.draw.circle(win, btc, (x, y), b-3)

def drawCross(win, tc, x, y, b):
    pygame.draw.rect(win, (tc), (x+b/6, y+b/2-2, b/3*2, 4))
    pygame.draw.rect(win, (tc), (x+b/2-2, y+b/6, 4, b/3*2))

    



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

    '''