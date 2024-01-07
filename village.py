

class TimberCamp:
    def __init__(self):
        self.maxlv = 30
        self.wood = 50
        self.clay = 60
        self.iron = 40
        self.pop = 5
        self.factor = 30
        self.build_t = 15
        self.points = 1

        self.wood_f = 1.25
        self.clay_f = 1.275
        self.iron_f = 1.245
        self.pop_f = 1.155
        self.factor_f = 1.16313
        self.build_tf = 1.2
        self.points_f = 1.2

        self.lv = 1

class ClayPit:
    def __init__(self):
        self.maxlv = 30
        self.wood = 65
        self.clay = 50
        self.iron = 40
        self.pop = 10
        self.factor = 30
        self.build_t = 15
        self.points = 1

        self.wood_f = 1.27
        self.clay_f = 1.265
        self.iron_f = 1.24
        self.pop_f = 1.14
        self.factor_f = 1.16313
        self.build_tf = 1.2
        self.points_f = 1.2

        self.lv = 1

class IronMine:
    def __init__(self):
        self.maxlv = 30
        self.wood = 75
        self.clay = 65
        self.iron = 70
        self.pop = 10
        self.factor = 30
        self.build_t = 18
        self.points = 1

        self.wood_f = 1.252
        self.clay_f = 1.275
        self.iron_f = 1.24
        self.pop_f = 1.17
        self.factor_f = 1.16313
        self.build_tf = 1.2
        self.points_f = 1.2

        self.lv = 1

class Warehouse:
    def __init__(self):
        self.maxlv = 30
        self.wood = 60
        self.clay = 50
        self.iron = 40
        self.pop = 0
        self.factor = 1000
        self.build_t = 17
        self.points = 1

        self.wood_f = 1.265
        self.clay_f = 1.27
        self.iron_f = 1.245
        self.pop_f = 1
        self.factor_f = 1.2294935
        self.build_tf = 1.2
        self.points_f = 1.2

        self.lv = 1

       
def calculate_wood(build):
    c = build.wood
    f = build.wood_f   
    if build.lv == 0:
        return int(c)
    else:
        for _ in range(build.lv-1):
            c =  c * f
        return int(c)
    
def calculate_clay(build):
    c = build.clay
    f = build.clay_f   
    if build.lv == 0:
        return int(c)
    else:
        for _ in range(build.lv-1):
            c =  c * f
        return int(c)
    
def calculate_iron(build):
    c = build.iron
    f = build.iron_f   
    if build.lv == 0:
        return int(c)
    else:
        for _ in range(build.lv-1):
            c =  c * f
        return int(c)
    
def calculate_pop(build):
    c = build.pop
    f = build.pop_f   
    if build.lv == 0:
        return int(c)
    else:
        for _ in range(build.lv-1):
            c =  c * f
        return int(c)
    
def calculate_factor(build):
    c = build.factor
    f = build.factor_f   
    if build.lv == 0:
        return int(c)
    else:
        for _ in range(build.lv-1):
            c =  c * f
        return int(c)
    
def calculate_time(build):
    c = build.build_t
    f = build.build_tf
    if build.lv == 0:
        return int(c)
    else:
        for _ in range(build.lv-1):
            c =  c * f
        return int(c)
    
def calculate_points(build):
    c = build.points
    f = build.points_f 
    if build.lv == 0:
        return int(c)
    else:
        for _ in range(build.lv-1):
            c =  c * f
        return int(c)



# print('W: ' + str(calculate_wood(Warehouse())))
# print('C: ' + str(calculate_clay(Warehouse())))
# print('I: ' + str(calculate_iron(Warehouse())))
# print('P: ' + str(calculate_pop(Warehouse())))
# print('F: ' + str(calculate_factor(Warehouse())))
# print('T: ' + str(calculate_time(Warehouse())))
# print('Pts:' + str(calculate_points(Warehouse())))