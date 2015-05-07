from random import random

sRandom = lambda: 2*random() - 1  # Signed Random. From -1 to 1

class CoordinatesTupleClass(object):
    x, y = None, None
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __getitem__(self, key):
        if (key == 0) or (key =='x'): 
            return self.x
        else:
            return self.y
    def __setitem__(self, key, value):
        if (key == 0) or (key == 'x'): 
            self.x = value
        else:
            self.y = value
    def __str__(self):
        return u"({0}, {1})".format(self.x, self.y)

def coordinatesDict(coordTuple):
    return {'x': coordTuple[0], 'y': coordTuple[1]}
    
def coordinatesTuple(coordDict):
    return CoordinatesTupleClass(coordDict['x'], coordDict['y'])

def create_empty_list_of_lists(size_x, size_y):
    return [[None] * size_y for i in range(size_x)] 


class Matrix(object):
    data = []
    size_x = 0
    size_y = 0
    
    def __init__(self, size_x, size_y, value = None):
        self.data = [[value] * size_y for i in range(size_x)]  # No usar [[None] * size_y] * size_x, ya que no hace copia profunda
        self.size_x = size_x
        self.size_y = size_y
        
    def __getitem__(self, coordinates):
        x, y = coordinates
        return self.data[x % self.size_x][y % self.size_y]
        
    def __setitem__(self, coordinates, value):
        x, y = coordinates
        self.Data[x % self.size_x][y % self.size_y] = value
        
    def __str__(self):
        return "\n".join(str(self.Data[i]) for i in range(len(self.Data)))
