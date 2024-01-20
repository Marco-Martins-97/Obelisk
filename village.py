

class Headquartes:
    def __init__(self):
        self.name = 'Headquartes'
        self.maxlv = 30
        self.lv = 1

        self.wood = 90
        self.clay = 80
        self.iron = 70
        self.pop = 5
        self.factor = 95
        self.build_t = 15
        self.points = 5

        self.wood_f = 1.2503
        self.clay_f = 1.2647
        self.iron_f = 1.25
        self.pop_f = 1.17
        self.factor_f = 0.953
        self.build_tf = 1.2
        self.points_f = 1.1555


class TimberCamp:
    def __init__(self):
        self.name = 'Timber Camp'
        self.maxlv = 30
        self.lv = 1

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

        
class ClayPit:
    def __init__(self):
        self.name = 'Clay Pit'
        self.maxlv = 30
        self.lv = 1

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

        
class IronMine:
    def __init__(self):
        self.name = 'Iron Mine'
        self.maxlv = 30
        self.lv = 1

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


class Farm:
    def __init__(self):
        self.name = 'Farm'
        self.maxlv = 30
        self.lv = 1

        self.wood = 45
        self.clay = 40
        self.iron = 30
        self.pop = 0
        self.factor = 240
        self.build_t = 17
        self.points = 1

        self.wood_f = 1.2887
        self.clay_f = 1.3078
        self.iron_f = 1.28
        self.pop_f = 0
        self.factor_f = 1.172103
        self.build_tf = 1.2
        self.points_f = 1.1925

        
class Warehouse:
    def __init__(self):
        self.name = 'Warehouse'
        self.maxlv = 30
        self.lv = 1

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
        self.pop_f = 0
        self.factor_f = 1.2294935
        self.build_tf = 1.2
        self.points_f = 1.2


village = [Headquartes(), TimberCamp(), ClayPit(), IronMine(), Farm(), Warehouse()]
       
def calculate_wood(building_idx, lvl):
    cost = village[building_idx].wood
    factor = village[building_idx].wood_f   
    if village[building_idx].lv == 0:
        return int(cost)
    else:
        for _ in range(lvl-1):
            cost =  cost * factor
        return int(cost)
    
def calculate_clay(building_idx, lvl):
    cost = village[building_idx].clay
    factor = village[building_idx].clay_f   
    if village[building_idx].lv == 0:
        return int(cost)
    else:
        for _ in range(lvl-1):
            cost =  cost * factor
        return int(cost)
    
def calculate_iron(building_idx, lvl):
    cost = village[building_idx].iron
    factor = village[building_idx].iron_f   
    if village[building_idx].lv == 0:
        return int(cost)
    else:
        for _ in range(lvl-1):
            cost =  cost * factor
        return int(cost)
    
def calculate_population(building_idx, lvl):
    cost = village[building_idx].pop
    factor = village[building_idx].pop_f   
    if village[building_idx].lv == 0:
        return int(cost)
    else:
        for _ in range(lvl-1):
            cost =  cost * factor
        return int(cost)
        
def calculate_factor(building_idx, lvl):
    cost = village[building_idx].factor
    factor = village[building_idx].factor_f   
    if village[building_idx].lv == 0:
        return 0
    else:
        for _ in range(lvl-1):
            cost =  cost * factor
        return int(cost)
    
def calculate_time(building_idx, lvl):
    cost = village[building_idx].build_t
    factor = village[building_idx].build_tf
    if village[building_idx].lv == 0:
        return int(cost)
    else:
        for _ in range(lvl-1):
            cost =  cost * factor
        return int(cost)
    
def calculate_points(building_idx, lvl):
    cost = village[building_idx].points
    factor = village[building_idx].points_f 
    if village[building_idx].lv == 0:
        return int(cost)
    else:
        for _ in range(lvl-1):
            cost =  cost * factor
        return int(cost)


# build = Headquartes()
# print('W: ' + str(calculate_wood(build)))
# print('C: ' + str(calculate_clay(build)))
# print('I: ' + str(calculate_iron(build)))
# print('P: ' + str(calculate_pop(build)))
# print('PN: ' + str(calculate_next_pop(build)))
# print('F: ' + str(calculate_factor(build)))
# print('T: ' + str(calculate_time(build)))
# print('Pts:' + str(calculate_points(build)))