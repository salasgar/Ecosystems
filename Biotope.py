from random import random

sRandom = lambda: 2*random() - 1  # Signed Random. From -1 to 1

def create_empty_list_of_lists(size_x, size_y):
    return [[None for i in range(size_x)] for j in range(size_y)]

class Biotope:
    ecosystem = None # Reference to the ecosystem it belongs to
    organismsArray = None # Array that indicates wich organism is in each place

    def __init__(self, size_x, size_y):
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
        
    def seek_free_pos_close_to(self, center, radius, attempts):
        # This is used by an organism in order to move to an empty place
        # or to give birth to a new organism in an empty place
        for i in range(attempts):
            x = int(center.x() + sRandom() * radius)
            y = int(center.y() + sRandom() * radius)
            if (organismsArray[x][y] == None): 
                return (x, y)
        return None
    
    def evolve(self):
        # Climate changes
        pass
        

