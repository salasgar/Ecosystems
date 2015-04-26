from random import random

import initial_settings
import Tools
import Organism
BIOTOPE_SIZE_X = initial_settings.BIOTOPE_SIZE_X  #  TO DO: Mirar si se puede conseguir de alguna manera que no haya que poner siempre "initial_settings." delante cada vez que usamos una constante.
BIOTOPE_SIZE_Y = initial_settings.BIOTOPE_SIZE_Y 


# Substance codes:
# Substances spread in the biotope:
NO_SUBSTANCE = 0
WATER = 1
CARBON_DIOXIDE = 2
OXIGEN = 3
NITRATE = 4
PHOSPHATE = 5
POISON = 10
POISON1 = 11
POISON2 = 12
FOOD = 13
FOOD1 = 14
FOOD2 = 15
TEMPERATURE = 101  
SUNLIGHT = 102  # Is there an equivalence between ENERGY and SUNLIGHT  ???
RAIN = 103 # The presence of RAIN increases the amount of WATER in the soil, and in the end, if there is enought humidity, it become DEPTH
ALTITUDE = 104
DEPTH = 105  # Depth of a sea, a lake or a river
# Substances inside organisms:
WATER_RESERVE = 201
NITRATE_RESERVE = 204
PHOSPHATE_RESERVE = 205


class substance(Tools.Array):
    Name = ''
    Code = NO_SUBSTANCE
    Block_size = 1
    Block_area = 1
    Time_counter = 0
    Spread_speed = 0
    
    def __init__(self, Name, Code, Block_size = 1, Spread_speed = 0):
        super(substance, self).__init__(BIOTOPE_SIZE_X // self.Block_size, BIOTOPE_SIZE_Y // self.Block_size, Value = 0)        
        self.Name = Name
        self.Code = Code
        self.Block_size = Block_size
        self.Block_area = self.Block_size * self.Block_size
        self.Spread_speed = Spread_speed

    def setValue(self, coordinates, value):
        (i, j) = (int(coordinates[0] // self.Block_size), int(coordinates[1] // self.Block_size))
        self[i, j] = value
        
    def getValue(self, coordinates):
        (i, j) = (int(coordinates[0] // self.Block_size), int(coordinates[1] // self.Block_size))
        return self[i, j]

    def concentration(self, coordinates):   # The amount of substance that an organism can absorve depends on the concentration of that substance
        (i, j) = (int(coordinates[0] // self.Block_size), int(coordinates[1] // self.Block_size))
        return self[i, j] / self.Block_area
        
    def variate_value(self, coordinates, variation):
        (i, j) = (int(coordinates[0] // self.Block_size), int(coordinates[1] // self.Block_size))
        self[i, j] += value
        
    def Evolve(self):
        New_array = Array(self.size_x, self.size_y)
        for i in range(self.size_x):
            for j in range(self.size_y):
                New_array[i, j] = self.Spread_speed * math.fsum(self[i+k, j+m] for k in (-1, 0, 1) for m in (-1, 0, 1)) / 9 + (1-self.Spread_speed)*self[i,j]
        self.Array = New_array.Array
    
    def setRandomValues(self, lowerBond = 0, higherBond = 100):
        for i in range(self.size_x):
            for j in range(self.size_y):
                self[i,j] = lowerBond + random() * (higherBond - lowerBond)
        
    
class Biotope(object):
    ecosystem = None # Reference to the ecosystem it belongs to
    organismsArray = None # Array that indicates wich organism is in each place
    size_x, size_y = 100, 100
    substances = []
    substanceIndex = []

    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.organismsArray = Tools.create_empty_list_of_lists(size_x, size_y)

    def __getitem__(self, coords):
        return self.organismsArray[coords[0] % self.size_x][coords[1] % self.size_y]
        
    def __setitem__(self, coords, value):
        self.organismsArray[coords[0] % self.size_x][coords[1] % self.size_y] = value
        
    def __str__(self):
        return '\n'.join(str(row) for row in self.organismsArray)

    def set_Substances(self, substances_list):
        self.substanceIndex = [None] * 200  
        index = 0
        for S in substances_list:
            new_substance = substance(S['Name'], S['Code'], S['Block_size'], S['Spread_speed'])
            new_substance.setRandomValues(0, 100)
            self.substances.append(new_substance)
            self.substanceIndex[S['Code']] = index          
            index += 1
    
    def set_Ecosystem(self, E):
        self.ecosystem = E
        for org in self.ecosystem.organisms:
            self.add_org(org, org['status']['coordinates'])
        
    def add_org(self, organism, location):
        self[location] = organism

    def move_organism(self, organism, new_place):
        new_x, new_y = new_place
        old_x = organism['status']['coordinates']['x'] # Como debo acceder?
        old_y = organism['status']['coordinates']['y']
        self[old_x, old_y] = None
        self[new_x, new_y] = self
    
    def delete_org(self, x, y):
        self[x, y] = None

    def delete_org(self, organism):
        (x, y) = organism['status']['coordinates'].values()
        self[x, y] = None
    
    def Location_is_OK(self, location):
        return self.Location_is_OK(location.x, location.y)

    def Location_is_OK(self, x, y):
        if (x >= 0) and (y >= 0) and (x < self.size_x) and (y < self.size_y):
            return True
        else:
            return False
        
    def seek_free_pos(self, attempts = 10):
        # This is used by an organism in order to move to an empty place
        # or to give birth to a new organism in an empty place
        for i in range(attempts):
            x = int(random() * self.size_x) % self.size_x
            y = int(random() * self.size_y) % self.size_y
            if (self[x, y] == None): 
                return (x, y)
        return None
    
    def seek_free_pos_close_to(self, center, radius, attempts = 1):
        # This is used by an organism in order to move to an empty place
        # or to give birth to a new organism in an empty place
        for i in range(attempts):
            x = int(center[0] + Tools.sRandom() * radius) % self.size_x
            y = int(center[1] + Tools.sRandom() * radius) % self.size_y
            if (self[x, y] == None): 
                return (x, y)
        return None
    
    def modify_amount_of_substance(self, Code, coordinates, Variation):
        self.substances[self.SubstanceIndex[Code]][coordinates] += Variation
        
    def substance(self, Code):
        return self.substances[self.substanceIndex[Code]]
    
    def evolve(self):
        for S in self.substances:
            S.Evolve()


# Ejemplos:

# probar con (BIOTOPE_SIZE_X, BIOTOPE_SIZE_Y) = (4, 8)
B = Biotope(BIOTOPE_SIZE_X, BIOTOPE_SIZE_Y)
B.set_Substances(initial_settings.SUBSTANCES)
B.substance(WATER).setRandomValues(10, 99)
B.substance(NITRATE).setRandomValues(40, 99)

print "WATER:"
for j in range(BIOTOPE_SIZE_Y):
    S = B.substance(WATER)
    print [int(S.concentration([i, j])) for i in range(BIOTOPE_SIZE_X)]

print "NITRATE:"
for j in range(BIOTOPE_SIZE_Y):
    S = B.substance(NITRATE)
    print [int(S.concentration([i, j])) for i in range(BIOTOPE_SIZE_X)]


print B.substance(NITRATE).Spread_speed

for i in range(7):
    new_pos = B.seek_free_pos()
    if new_pos:
        B[new_pos] = 'Ey'      
print B

