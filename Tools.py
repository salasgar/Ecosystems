from random import random

sRandom = lambda: 2*random() - 1  # Signed Random. From -1 to 1

class CoordinatesTupleClass:
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
