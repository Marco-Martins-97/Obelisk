import pygame
from datetime import datetime
import configurations as config
import village as v
 

class Button:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def at_button(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.x <= mouse_x <= self.x+self.width and self.y <= mouse_y <= self.y+self.height:
            return True
    
    def pressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.at_button():
                return True
    
    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height))


class Graphics:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.win = pygame.display.set_mode((width, height))             #Create a window
        pygame.display.set_caption('Obelisk')                           #Windown name
        pygame.font.init()                                              #initialize the font

        self.font = 'comicsans'                                         #font in use

        self.background_color = (244, 228, 188)                         #custom colors
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

        self.game_speed = config.game_speed                         #game speed
    
    #Check if can upgrade the building
    def upgrade_avaliable(self, building_idx, level):    
        if building_idx == self.progress1 or building_idx == self.progress2: lvl = 2                                                            #Check if they are in progress
        else: lvl = 1   
        if (self.wood >= v.calculate_wood(building_idx, level+lvl)                                                                              #Check if have the necessary wood for the upgrade
            and self.clay >= v.calculate_clay(building_idx, level+lvl)                                                                          #Check if have the necessary clay for the upgrade
            and self.iron >= v.calculate_iron(building_idx, level+lvl)                                                                          #Check if have the necessary iron for the upgrade
            and self.population >= (v.calculate_population(building_idx, level+lvl)-v.calculate_population(building_idx, level+lvl-1))          #Check if have the necessary population for the upgrad
            and self.village_level[building_idx]+lvl-1 < v.village[building_idx].max_lv                                                         #Check if it's below max_lv
            and (self.progress1 == -1 or self.progress2 == -1)):                                                                                #Checks if have a free space in the progress
            return True
        else:
            return False

    #Calculate the total of points  
    def get_points(self):
        pts = 0
        for building in range(len(v.village)):                                              #Go Through all buildings
            pts += v.calculate_points(building, self.village_level[building])               #calculate and add the points of ea building to a varaiable
        return pts
    
    #Calculate the population used
    def get_population(self):
        pop = 0
        for building in range(len(v.village)):                                              #Go Through all buildings
            if building == self.progress1 and building == self.progress2: lvl = 2           #check if they are in progress
            elif building == self.progress1 or building == self.progress2: lvl = 1
            else: lvl = 0
            pop += v.calculate_population(building, self.village_level[building]+lvl)       #calculate and add the population of ea building to a varaiable
        return pop

    #Update the calculated values
    def update(self, data):
        wood, clay, iron, progress1, progress2, progress_time, headquartes, timbercamp, claypit, ironmine, farm, warehouse = data
        self.wood = round(float(wood), 3)
        self.clay = round(float(clay), 3)
        self.iron = round(float(iron), 3)

        self.village_level = [int(headquartes), int(timbercamp), int(claypit), int(ironmine), int(farm), int(warehouse)]

        self.progress1 = int(progress1)
        self.progress2 = int(progress2)
        self.start_progress = datetime.strptime((progress_time), "%Y-%m-%d %H:%M:%S.%f")
        self.progress_time = int(v.calculate_time(self.progress1, self.village_level[self.progress1]+1, self.village_level[0])/self.game_speed - (datetime.now() - self.start_progress).total_seconds())

        self.wood_p = v.calculate_factor(1, self.village_level[1]) * self.game_speed
        self.clay_p = v.calculate_factor(2, self.village_level[2]) * self.game_speed
        self.iron_p = v.calculate_factor(3, self.village_level[3]) * self.game_speed
        self.farm = v.calculate_factor(4, self.village_level[4])
        self.warehouse = v.calculate_factor(5, self.village_level[5])

        self.population = self.farm - self.get_population()
        self.points = self.get_points()

    #Text alignment
    #Text aligned to center
    def drawTextCenter(self, text, size, color, x, y, width, height):
        font = pygame.font.SysFont(self.font, size)                                                                             #get the font and size
        text = font.render(str(text), 1, color)                                                                                 #render the text in the color
        self.win.blit(text, (x + round(width/2)-round(text.get_width()/2), y + round(height/2)-round(text.get_height()/2)))     #put it in the possition
    #Text aligned to the left
    def drawTextLeft(self, text, size, color, x, y, height):
        font = pygame.font.SysFont(self.font, size)                                                                             #get the font and size
        text = font.render(str(text), 1, color)                                                                                 #render the text in the color
        self.win.blit(text, (x, y + round(height/2)-round(text.get_height()/2)))                                                #put it in the possition
    #Text aligned to the right
    def drawTextRight(self, text, size, color, x, y, width, height):
        font = pygame.font.SysFont(self.font, size)                                                                             #get the font and size
        text = font.render(str(text), 1, color)                                                                                 #render the text in the color
        self.win.blit(text, (x + width -round(text.get_width()), y + round(height/2)-round(text.get_height()/2)))               #put it in the possition

    #Shapes
    #Draw a rectangle with a border aand roud corners
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
    #Draw a circle with a border
    def drawCircle(self, border_color, button_color, x, y, radius):
        pygame.draw.circle(self.win, border_color, (x, y), radius)
        pygame.draw.circle(self.win, button_color, (x, y), radius-3)
    #craw a +
    def drawCross(self, text_color, x, y, radius):
        pygame.draw.rect(self.win, (text_color), (x+radius/6, y+radius/2-2, radius/3*2, 4))
        pygame.draw.rect(self.win, (text_color), (x+radius/2-2, y+radius/6, 4, radius/3*2))
    
    #Dashboards
    #draw the points
    def draw_points(self, x, y, width, radius):
        rows = 1                                                                        #number of columns
        row_height = 32                                                                 #column height
        height = rows*row_height                                                        #get the height os the dashboard multipling the rown x row height
        text_color = self.text_color
        self.drawRoundRect(x, y, width, height+5, radius)                               #draw the dashboar rectangle
        self.drawTextLeft('POINTS: ', 20, text_color, x+20, y, row_height)              #draw the text
        self.drawTextRight(self.points, 20, text_color, x-20, y, width, row_height)     #draw the value

    #draw the progress
    def draw_progress(self, x, y, width, radius):
        rows = 3
        row_height = 32
        height = rows*row_height
        text_color = self.text_color
        mins, secs = divmod(self.progress_time, 60)
        progress_timer = '{:02d}:{:02d}'.format(mins, secs)
        self.drawRoundRect(x, y, width, height+5, radius)
        self.drawTextCenter('PROGRESS', 20, text_color, x, y+5, width, row_height)
        self.drawTextLeft('1: ', 20, text_color, x+20, y+row_height*1, row_height)
        if self.progress1 != -1:
            self.drawTextLeft(v.village[self.progress1].name, 20, text_color, x+40, y+row_height*1, row_height)
            self.drawTextRight(progress_timer, 20, text_color, x-20, y+row_height*1, width, row_height)    
        self.drawTextLeft('2: ', 20, text_color, x+20, y+row_height*2, row_height)
        if self.progress2 != -1:
            self.drawTextLeft(v.village[self.progress2].name, 20, text_color, x+40, y+row_height*2, row_height)
     
    #draw the production
    def draw_production(self, x, y, width, radius):
        rows = 4
        row_height = 32
        height = rows*row_height
        text_color = self.text_color
        self.drawRoundRect(x, y, width, height+5, radius)
        self.drawTextCenter('PRODUCTION', 20, text_color, x, y+5, width, row_height)
        self.drawTextLeft('WOOD: ', 20, text_color, x+20, y+row_height*1, row_height)
        self.drawTextRight(self.wood_p, 20, text_color, x-20, y+row_height*1, width, row_height)
        self.drawTextLeft('CLAY: ', 20, text_color, x+20, y+row_height*2, row_height)
        self.drawTextRight(self.clay_p, 20, text_color, x-20, y+row_height*2, width, row_height)
        self.drawTextLeft('IRON: ', 20, text_color, x+20, y+row_height*3, row_height)
        self.drawTextRight(self.iron_p, 20, text_color, x-20, y+row_height*3, width, row_height)

    #draw the warehouse
    def draw_warehouse(self, x, y, width, radius):
        rows = 5
        row_height = 32
        height = rows*row_height
        text_color = self.text_color
        self.drawRoundRect(x, y, width, height+5, radius)
        self.drawTextCenter('WAREHOUSE', 20, text_color, x, y+5, width, row_height)
        self.drawTextLeft('CAPACITY: ', 20, text_color, x+20, y+row_height*1 , row_height)
        self.drawTextRight(self.warehouse, 20, text_color, x-20, y+row_height*1, width, row_height)
        self.drawTextLeft('WOOD: ', 20, text_color, x+20, y+row_height*2, row_height)
        self.drawTextRight(self.wood, 20, text_color, x-20, y+row_height*2, width, row_height)
        self.drawTextLeft('CLAY: ', 20, text_color, x+20, y+row_height*3, row_height)
        self.drawTextRight(self.clay, 20, text_color, x-20, y+row_height*3, width, row_height)
        self.drawTextLeft('IRON: ', 20, text_color, x+20, y+row_height*4, row_height)
        self.drawTextRight(self.iron, 20, text_color, x-20, y+row_height*4, width, row_height)

    #draw the population
    def draw_population(self, x, y, width, radius):
        rows = 2
        row_height = 32
        height = rows*row_height
        text_color = self.text_color
        self.drawRoundRect(x, y, width, height+5, radius)
        self.drawTextCenter('FARM', 20, text_color, x, y+5, width, row_height)
        self.drawTextLeft('POPULATION: ', 20, text_color, x+20, y+row_height*1, row_height)
        self.drawTextRight(self.population, 20, text_color, x-20, y+row_height*1, width, row_height)

    #draw the connect menu
    def draw_connect_menu(self, x, y, width, radius):
        rows = 4
        row_height = 32
        height = rows*row_height
        text_color = self.text_color
        self.drawRoundRect(x-width-50, y, width, height+5, radius)
        self.drawRoundRect(x+50, y, width, height+5, radius)

        self.drawTextCenter('REGISTER', 40, text_color, x-width-50, y+height/3, width, row_height)
        self.drawTextCenter('LOGIN', 40, text_color, x+50, y+height/3, width, row_height)

    #draw the regist menu
    def draw_regist_menu(self, input, username, password, password2,  x, y, width, radius):
        rows = 4
        row_height = 32
        height = rows*row_height
        text_color = self.text_color
        self.drawRoundRect(x-width-50, y, width, height+5, radius)
        self.drawRoundRect(x+50, y, width, height+5, radius)

        self.drawTextCenter('LOGIN', 40, text_color, x+50, y+height/3, width, row_height)

        self.drawTextCenter('REGISTER', 20, text_color, x-width-50, y+5, width, row_height)
        self.drawTextLeft('USERNAME: ', 20, text_color, x-width-50+20, y+row_height*1, row_height)
        self.drawTextRight(username, 20, text_color, x-width-50-20, y+row_height*1, width, row_height)
        self.drawTextLeft('PASSWORD: ', 20, text_color, x-width-50+20, y+row_height*2, row_height)
        self.drawTextRight(password, 20, text_color, x-width-50-20, y+row_height*2, width, row_height)
        self.drawTextLeft('PASSWORD: ', 20, text_color, x-width-50+20, y+row_height*3, row_height)
        self.drawTextRight(password2, 20, text_color, x-width-50-20, y+row_height*3, width, row_height)
        if input == 'username': 
            self.drawTextRight('<', 20, text_color, x-width-40-20, y+row_height*1, width, row_height)
        elif input == 'password':
            self.drawTextRight('<', 20, text_color, x-width-40-20, y+row_height*2, width, row_height)
        else: 
            self.drawTextRight('<', 20, text_color, x-width-40-20, y+row_height*3, width, row_height)


    #draw the login menu
    def draw_login_menu(self, input, username, password,  x, y, width, radius):
        rows = 4
        row_height = 32
        height = rows*row_height
        text_color = self.text_color
        self.drawRoundRect(x-width-50, y, width, height+5, radius)
        self.drawRoundRect(x+50, y, width, height+5, radius)

        self.drawTextCenter('REGISTER', 40, text_color, x-width-50, y+height/3, width, row_height)

        self.drawTextCenter('LOGIN', 20, text_color, x+50, y+5, width, row_height)
        self.drawTextLeft('USERNAME: ', 20, text_color, x+50+20, y+row_height*2, row_height)
        self.drawTextRight(username, 20, text_color, x+50-20, y+row_height*2, width, row_height)
        self.drawTextLeft('PASSWORD: ', 20, text_color, x+50+20, y+row_height*3, row_height)
        self.drawTextRight(password, 20, text_color, x+50-20, y+row_height*3, width, row_height)
        if input == 'username': 
            self.drawTextRight('<', 20, text_color, x+60-20, y+row_height*2, width, row_height)
        else: 
            self.drawTextRight('<', 20, text_color, x+60-20, y+row_height*3, width, row_height)


    #draw the village buildings
    def draw_village_buildings(self, x, y, width, height, radius):
        text_color = self.text_color
        for i in range(len(v.village)):
            #builds
            self.drawRoundRect(x, y + i * 40, width, height, radius)                                                            #draw a rectangle with the building name
            self.drawTextCenter(v.village[i].name, 20, text_color, x, y+i*40, width, height-6)

    #draw the village levels
    def draw_village_levels(self, x, y, radius):
        text_color = self.text_color
        for i in range(len(v.village)):
            self.drawCircle(self.border_color, self.button_color, x, y+radius+i*40, radius)                      #draw a circle with the lever at left of the rectangle
            self.drawTextCenter(self.village_level[i], 20, text_color, x-radius/2, y+radius/2-1+i*40, radius, radius)


    #draw the village upgrade buttons
    def draw_village_upgrade_btns(self, x, y, radius):
        text_color = self.text_color
        for i in range(len(v.village)):
            if self.upgrade_avaliable(i, self.village_level[i]):                                                                #if can upgrade, draw a circle at right of the rectangle with a cross in
                #add button 
                self.drawCircle(self.border_color, self.button_color, x+radius, y+radius+i*40, radius)      
                self.drawCross(text_color, x, y+i*40, radius*2)
            else:                                                                                                               #if cant upgrade, draw a circle at right of the rectangle with a cross in, with no colors
                #add button 
                self.drawCircle(self.border_colorless, self.button_colorless, x+radius, y+radius+i*40, radius)
                self.drawCross(self.text_color_white, x, y+i*40, radius*2)

    #draw the resources, population and time needed to upgrade the building to the next level
    def draw_requeriments(self, index, x, y, width, radius):
        rows = 6
        row_height = 32
        height = rows*row_height
        if index == self.progress1 and index == self.progress2: lvl = 3
        elif index == self.progress1 or index == self.progress2: lvl = 2
        else: lvl = 1
        wood = v.calculate_wood(index, self.village_level[index]+lvl)                                                                                   #calculate the wood, clay, iron, population and time needed
        clay = v.calculate_clay(index, self.village_level[index]+lvl)                                                                                               
        iron = v.calculate_iron(index, self.village_level[index]+lvl)
        population = v.calculate_population(index, self.village_level[index]+lvl) - v.calculate_population(index, self.village_level[index]+lvl-1)
        _time = int(v.calculate_time(index, self.village_level[index]+lvl, self.village_level[0])/self.game_speed)                                              
        mins, secs = divmod(_time, 60)                                                                                                                  #converte the time in seconds to (min:sec)
        _time = '{:02d}:{:02d}'.format(mins, secs)
        
        self.drawRoundRect(x, y, width, height+5, radius)                                                                                               #draw the values in the dashboard
        self.drawTextCenter('REQERIMENTS', 20, self.text_color, x, y+5, width, row_height)
        self.drawTextLeft('WOOD: ', 20, self.text_color, x+20, y+row_height*1, row_height)
        if self.wood < wood : tc = self.text_color_red
        else: tc = self.text_color
        self.drawTextRight(wood, 20, tc, x-20, y+row_height*1, width, row_height)
        self.drawTextLeft('CLAY: ', 20, self.text_color, x+20, y+row_height*2, row_height)
        if self.clay < clay : tc = self.text_color_red
        else: tc = self.text_color
        self.drawTextRight(clay, 20, tc, x-20, y+row_height*2, width, row_height)
        self.drawTextLeft('IRON: ', 20, self.text_color, x+20, y+row_height*3, row_height)
        if self.iron < iron : tc = self.text_color_red
        else: tc = self.text_color
        self.drawTextRight(iron, 20, tc, x-20, y+row_height*3, width, row_height)
        self.drawTextLeft('POPULATION: ', 20, self.text_color, x+20, y+row_height*4, row_height)
        if self.population < population : tc = self.text_color_red
        else: tc = self.text_color
        self.drawTextRight(population, 20, tc, x-20, y+row_height*4, width, row_height)
        self.drawTextLeft('TIME: ', 20, self.text_color, x+20, y+row_height*5, row_height)
        self.drawTextRight(_time, 20, self.text_color, x-20, y+row_height*5, width, row_height)

    #Create Buttons
    def buttons_village(self, x, y, width, height):
        btns = []
        for i in range(len(v.village)):
            btns.append(Button(x, y + i * 40, width, height ))
        return btns


