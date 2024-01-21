import pygame
import configurations as config
import village as v





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
        self.border_colorless = (50, 50, 50)
        self.button_colorless = (96, 96, 96) 
        self.text_color_white = (200, 200, 200)
        self.text_color_red = (222, 0,42)
        
        self.village_level = []

        self.wood_p = 0
        self.clay_p = 0
        self.iron_p = 0
        self.farm = 0
        self.warehouse = 0

        self.wood = 0
        self.clay = 0
        self.iron = 0
        self.population = 0
        self.points = 0

        self.progress1 = -1
        self.progress2 = -1
        self.progress_time = 0

        self.game_speed = config.game_speed
        
    def upgrade_avaliable(self, building_idx, level):       
        if self.wood >= v.calculate_wood(building_idx, level+1) and self.clay >= v.calculate_clay(building_idx, level+1) and self.iron >= v.calculate_iron(building_idx, level+1) and self.population >= v.calculate_population(building_idx, level+1) and self.village_level[building_idx] < v.village[building_idx].max_lv and (self.progress1 == -1 or self.progress2 == -1):
            return True
        else:
            return False
        
    def get_points(self):
        pts = 0
        for building in range(len(v.village)):
            pts += v.calculate_points(building, self.village_level[building])
        return pts
    
    def get_population(self):
        pop = 0
        for building in range(len(v.village)):
            pop += v.calculate_population(building, self.village_level[building])
        return pop


    def update(self, data):
        wood, clay, iron, progress1, progress2, progress_time, headquartes, timbercamp, claypit, ironmine, farm, warehouse = data
        self.wood = round(wood, 3)
        self.clay = round(clay, 3)
        self.iron = round(iron, 3)
        self.progress1 = int(progress1)
        self.progress2 = int(progress2)
        self.progress_time = int(progress_time)

        self.village_level = [int(headquartes), int(timbercamp), int(claypit), int(ironmine), int(farm), int(warehouse)]

        self.wood_p = v.calculate_factor(1, self.village_level[1]) * self.game_speed
        self.clay_p = v.calculate_factor(2, self.village_level[2]) * self.game_speed
        self.iron_p = v.calculate_factor(3, self.village_level[3]) * self.game_speed
        self.farm = v.calculate_factor(4, self.village_level[4])
        self.warehouse = v.calculate_factor(5, self.village_level[5])

        self.population = self.farm - self.get_population()
        self.points = self.get_points()

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

    #Shapes
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

    def drawCircle(self, border_color, button_color, x, y, radius):
        pygame.draw.circle(self.win, border_color, (x, y), radius)
        pygame.draw.circle(self.win, button_color, (x, y), radius-3)
    
    def drawCross(self, text_color, x, y, radius):
        pygame.draw.rect(self.win, (text_color), (x+radius/6, y+radius/2-2, radius/3*2, 4))
        pygame.draw.rect(self.win, (text_color), (x+radius/2-2, y+radius/6, 4, radius/3*2))
    
    #Dashboards
    def draw_points(self, x, y, width, radius):
        columns = 1
        column_height = 32
        height = columns*column_height
        text_color = self.text_color
        self.drawRoundRect(x, y, width, height+5, radius)
        self.drawTextLeft('POINTS: ', 20, text_color, x+20, y, column_height)
        self.drawTextRight(self.points, 20, text_color, x-20, y, width, column_height)


    def draw_progress(self, x, y, width, radius):
        columns = 3
        column_height = 32
        height = columns*column_height
        text_color = self.text_color
        mins, secs = divmod(self.progress_time, 60)
        progress_timer = '{:02d}:{:02d}'.format(mins, secs)
        self.drawRoundRect(x, y, width, height+5, radius)
        self.drawTextCenter('PROGRESS', 20, text_color, x, y+5, width, column_height)
        self.drawTextLeft('1: ', 20, text_color, x+20, y+column_height*1, column_height)
        if self.progress1 != -1:
            self.drawTextLeft(v.village[self.progress1].name, 20, text_color, x+40, y+column_height*1, column_height)
            self.drawTextRight(progress_timer, 20, text_color, x-20, y+column_height*1, width, column_height)    
        self.drawTextLeft('2: ', 20, text_color, x+20, y+column_height*2, column_height)
        if self.progress2 != -1:
            self.drawTextLeft(v.village[self.progress2].name, 20, text_color, x+40, y+column_height*2, column_height)
     

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


    def draw_population(self, x, y, width, radius):
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

    def draw_village(self, x, y, width, height, radius):
        text_color = self.text_color
        for i in range(len(v.village)):
            #builds
            self.drawRoundRect(x, y + i * 40, width, height, radius)
            self.drawTextCenter(v.village[i].name, 20, text_color, x, y+i*40, width, height-6)
            #lv
            self.drawCircle(self.border_color, self.button_color, x-height+7, y+i*40+height/2, height/2+3)
            self.drawTextCenter(self.village_level[i], 20, text_color, x-height+7, y-1+i*40, 0, height)

            if self.upgrade_avaliable(i, self.village_level[i]):
                #add button 
                self.drawCircle(self.border_color, self.button_color, x+width+height-7, y+i*40+height/2, height/2+3)
                self.drawCross(text_color, x+width+height/2-7, y+i*40, height)
            else:
                #add button 
                self.drawCircle(self.border_colorless, self.button_colorless, x+width+height-7, y+i*40+height/2, height/2+3)
                self.drawCross(self.text_color_white, x+width+height/2-7, y+i*40, height)

    def draw_requeriments(self, index, x, y, width, radius):
        columns = 6
        column_height = 32
        height = columns*column_height
        if index == self.progress1 and index == self.progress2: lvl = 3
        elif index == self.progress1 or index == self.progress2: lvl = 2
        else: lvl = 1
        wood = v.calculate_wood(index, self.village_level[index]+lvl)
        clay = v.calculate_clay(index, self.village_level[index]+lvl)
        iron = v.calculate_iron(index, self.village_level[index]+lvl)
        population = v.calculate_population(index, self.village_level[index]+lvl)
        _time = int(v.calculate_time(index, self.village_level[index]+lvl, self.village_level[0])/self.game_speed)
        print(_time)
        mins, secs = divmod(_time, 60)
        _time = '{:02d}:{:02d}'.format(mins, secs)
        
        self.drawRoundRect(x, y, width, height+5, radius)
        self.drawTextCenter('REQERIMENTS', 20, self.text_color, x, y+5, width, column_height)
        self.drawTextLeft('WOOD: ', 20, self.text_color, x+20, y+column_height*1, column_height)
        if self.wood < wood : tc = self.text_color_red
        else: tc = self.text_color
        self.drawTextRight(wood, 20, tc, x-20, y+column_height*1, width, column_height)
        self.drawTextLeft('CLAY: ', 20, self.text_color, x+20, y+column_height*2, column_height)
        if self.clay < clay : tc = self.text_color_red
        else: tc = self.text_color
        self.drawTextRight(clay, 20, tc, x-20, y+column_height*2, width, column_height)
        self.drawTextLeft('IRON: ', 20, self.text_color, x+20, y+column_height*3, column_height)
        if self.iron < iron : tc = self.text_color_red
        else: tc = self.text_color
        self.drawTextRight(iron, 20, tc, x-20, y+column_height*3, width, column_height)
        self.drawTextLeft('POPULATION: ', 20, self.text_color, x+20, y+column_height*4, column_height)
        if self.population < population : tc = self.text_color_red
        else: tc = self.text_color
        self.drawTextRight(population, 20, tc, x-20, y+column_height*4, width, column_height)
        self.drawTextLeft('TIME: ', 20, self.text_color, x+20, y+column_height*5, column_height)
        self.drawTextRight(_time, 20, self.text_color, x-20, y+column_height*5, width, column_height)





'''   
def drawrectangle(win, x, y, w, h):
    pygame.draw.rect(win, ((0,0,0)), (x, y, w, h))
    pygame.draw.rect(win, ((255,255,255)), (x+3, y+3, w-6, h-6))

    '''