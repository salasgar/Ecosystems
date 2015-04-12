from random import random

sRandom = lambda: 2*random() - 1  # Signed Random. From -1 to 1

def create_empty_list_of_lists(size_x, size_y):
    return [[None for i in range(size_x)] for j in range(size_y)]

class Biotope:
    ecosystem = None # Reference to the ecosystem it belongs to
    organismsArray = None # Array that indicates wich organism is in each place

    def __init__(self, size_x, size_y):
        self.ecosystem = ecosystem_
        self.organismsArray = create_empty_list_of_lists(size_x, size_y)
        for org in ecosystem.organisms:
            self.add_org(org, org.coordinates)
    
    def set_Ecosystem(self, E):
        self.ecosystem = E
        
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
        

