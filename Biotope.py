from random import random

import Tools
import Organism

def create_empty_list_of_lists(size_x, size_y):
    return [[None for i in range(size_x)] for j in range(size_y)]

class Biotope:
    ecosystem = None # Reference to the ecosystem it belongs to
    organismsArray = None # Array that indicates wich organism is in each place
    size_x, size_y = 100, 100

    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.organismsArray = create_empty_list_of_lists(size_x, size_y)
    
    def set_Ecosystem(self, E):
        self.ecosystem = E
        for org in self.ecosystem.organisms:
            self.add_org(org, org['status']['coordinates'])
        
    def add_org(self, organism, x = None, y = None):
        if x == None:
            x_ = organism['status']['coordinates']['x']
            y_ = organism['status']['coordinates']['y']
        elif y == None: # in this case both coordinates are packed in the variable x
            if type(x) == dict:
                x_ = x['x']
                y_ = x['y']
            else:
                x_ = x[0]
                y_ = x[1]
        self.organismsArray[x_][y_] = organism

    def move_organism(self, organism, new_place):
        new_x, new_y = new_place
        old_x = organism['status']['coordinates']['x'] # Como debo acceder?
        old_y = organism['status']['coordinates']['y']
        self.organismsArray[old_x][old_y] = None
        self.organismsArray[new_x][new_y] = self

    
    def delete_org(self, x, y):
        self.organismsArray[x][y] = None

    def delete_org(self, organism):
        (x, y) = organism['status']['coordinates'].values()
        self.organismsArray[x][y] = None
    
    def __getitem__(self, x, y = None):
        if y == None:
            return self.organismsArray[x[0]][x[1]]
        else:
            return self.organismsArray[x][y]
        
    def __setitem__(self, organism, x, y = None):
        if y == None:
            self.organismsArray[x[0]][x[1]] = organism
        else:
            self.organismsArray[x][y] = organism
            
    def Location_is_OK(self, location):
        return Location_is_OK(location.x, location.y)

    def Location_is_OK(self, x, y):
        if (x >= 0) and (y >= 0) and (x < self.size_x) and (y < self.size_y):
            return True
        else:
            return False
        
    def seek_free_pos(self, attempts = 10):
        # This is used by an organism in order to move to an empty place
        # or to give birth to a new organism in an empty place
        for i in range(attempts):
            x = int(random() * self.size_x)
            y = int(random() * self.size_y)
            if self.Location_is_OK(x, y):
                if (self.organismsArray[x][y] == None): 
                    return (x, y)
        return None
    
    def seek_free_pos_close_to(self, center, radius, attempts = 1):
        # This is used by an organism in order to move to an empty place
        # or to give birth to a new organism in an empty place
        for i in range(attempts):
            x = int(center[0] + Tools.sRandom() * radius)
            y = int(center[1] + Tools.sRandom() * radius)
            if self.Location_is_OK(x, y):
                if (self.organismsArray[x][y] == None): 
                    return (x, y)
        return None
    
    def evolve(self):
        # Climate changes
        pass
        

