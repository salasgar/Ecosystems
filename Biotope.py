from random import random

import initial_settings
import Tools
import Organism
BIOTOPE_SIZE_X = initial_settings.BIOTOPE_SIZE_X  #  TO DO: Mirar si se puede conseguir de alguna manera que no haya que poner siempre "initial_settings." delante cada vez que usamos una constante.
BIOTOPE_SIZE_Y = initial_settings.BIOTOPE_SIZE_Y 


class Array:
    Array = []
    size_x = 0
    size_y = 0
    
    def __init__(self, size_x, size_y):
        self.Array = [[None] * size_y for i in range(size_x)]  # No usar [[None] * size_y] * size_x, ya que no hace copia profunda
        self.size_x = size_x
        self.size_y = size_y
        
    def __getitem__(self, coords):
        return self.Array[coords[0] % self.size_x][coords[1] % self.size_y]
        
    def __setitem__(self, coords, value):
        self.Array[coords[0] % self.size_x][coords[1] % self.size_y] = value
        
    def __str__(self):
        return "\n".join(str(self.Array[i]) for i in range(len(self.Array)))

# Substance codes:
NO_SUBSTANCE = 0
WATER = 1
ENERGY = 2
NITRATE = 3
PHOSPHATE = 4
TEMPERATURE = 5  
ALTITUDE = 6
DEPTH = 7  # Depth of a sea, a lake or a river
SUNLIGHT = 8  # Is there an equivalence between ENERGY and SUNLIGHT  ???
RAIN = 9 # The presence of RAIN increases the amount of WATER in the soil, and in the end, if there is enought humidity, it become DEPTH

class SubstanceOfDegree0(Array):
    Name = NO_SUBSTANCE
    
    def __init__(self, Name, size_x = BIOTOPE_SIZE_X, size_y = BIOTOPE_SIZE_Y):
        self.size_x = min(size_x, BIOTOPE_SIZE_X)
        self.size_y = min(size_y, BIOTOPE_SIZE_Y)
        self.Array = [[0] * self.size_y for i in range(self.size_x)]
        self.Name = Name
        
    def __getitem__(self, coords): #if self.size_x < BIOTOPE_SIZE_X, we reduce the coordinates proportionally:
        return self.Array[int(coords[0]*self.size_x/BIOTOPE_SIZE_X) % self.size_x][int(coords[1]*self.size_y/BIOTOPE_SIZE_Y) % self.size_y]
        
    def __setitem__(self, coords, value): #if self.size_x < BIOTOPE_SIZE_X, we reduce the coordinates proportionally:
        self.Array[int(coords[0]*self.size_x/BIOTOPE_SIZE_X) % self.size_x][int(coords[1]*self.size_y/BIOTOPE_SIZE_Y) % self.size_y] = value

    def Modify(self, coords, variation): # Increments or decrements the quantity of substance in the given area
        old_value = self[coords]
        new_value = old_value + variation*self.size_x*self.size_y/(BIOTOPE_SIZE_X * BIOTOPE_SIZE_Y)  # El incremento o decremento se reparte entre todo el area del biotopo representada por esa casilla del Array de la sustancia
        self[coords] = new_value        
    
class SubstanceOfDegree1(Array):
    Name = NO_SUBSTANCE
    
    def __init__(self, Name, size_x = BIOTOPE_SIZE_X, size_y = BIOTOPE_SIZE_Y):
        self.size_x = min(size_x, BIOTOPE_SIZE_X)
        self.size_y = min(size_y, BIOTOPE_SIZE_Y)
        self.Array = [[None] * self.size_y for j in range(self.size_x)]
        self.Name = Name
        
    def __getitem__(self, coords): #we interpolate linearly the values:
        Ax = int((coords[0] % BIOTOPE_SIZE_X)*self.size_x/BIOTOPE_SIZE_X)
        Ay = int((coords[1] % BIOTOPE_SIZE_Y)*self.size_y/BIOTOPE_SIZE_Y)
        Bx = (Ax + 1) % self.size_x
        By = (Ay + 1) % self.size_y
        # interpolamos el valor en las coordenadas exactas a partir del valor en los puntos (Ax, Ay), (Ax, By), (Bx, Ay) y (Bx, By),
        # que son los puntos de la tabla que estan alrededor del punto del biotopo del cual queremos averiguar su concentracion de 
        # sustancia. Las coordenadas (x, y) son las coordenadas relativas de ese punto dentro del cuadrado (Ax, Ay), (Bx, By)
        x = coords[0] % BIOTOPE_SIZE_X - Ax * BIOTOPE_SIZE_X / self.size_x
        y = coords[1] % BIOTOPE_SIZE_Y - Ay * BIOTOPE_SIZE_Y / self.size_y
        return (1-x)*(1-y)*Array[Ax][Ay]  +  x*(1-y)*Array[Bx][Ay] + (1-x)*y*Array[Ax][By]  +  x*y*Array[Bx][By] 
    
    def __setitem__(self, coords, value): #we interpolate linearly the values:
        pass        
    
    def Modify(self, coords, variation): # Increments or decrements the quantity of substance in the given area
        pass
    
class Biotope:
    ecosystem = None # Reference to the ecosystem it belongs to
    organismsArray = None # Array that indicates wich organism is in each place
    size_x, size_y = 100, 100
    substances = []

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
        
A = SubstanceOfDegree0(NO_SUBSTANCE, BIOTOPE_SIZE_X/2, BIOTOPE_SIZE_Y/2)

A[9, 1] = 7
A[1, 10] = 2
print A
