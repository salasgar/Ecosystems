from random import random

import Tools

REPRODUCTION_FREQUENCY = 0.01

class CoordinatesTupleClass:
    x, y = None, None
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __getitem__(self, key):
        if key == 0: 
            return self.x
        else:
            return self.y
    def __setitem__(self, key, value):
        if key == 0: 
            self.x = value
        else:
            self.y = value
    def x():
        return self.x
    def y():
        return self.y        

def coordinatesDict(coordTuple):
    return {'x': coordTuple[0], 'y': coordTuple[1]}
    
def coordinatesTuple(coordDict):
    return CoordinatesTupleClass(coordDict['x'], coordDict['y'])

class Organism:
    Data = None  # All organism's attributes (genes and status)
    
    def __init__(self, Data):
        self.Data = Data
    
    def __getitem__(self, keys):
        return self.Data[keys]
        
    def __setitem__(self, keys, value):
        self.Data[keys] = value        
        
    def genes(self):
        return self.Data['genes']
        
    def status(self):
        return self.Data['status']
        
    def position(self):
        return coordinatesTuple(self.Data['status']['coordinates'])     
    
    def setLocation(self, newLocation):
        self.Data['status']['coordinates'] = coordinatesDict(newLocation)
    
    def speed(self):
        return self.Data['genes']['speed']
        
    def move(self, ecosystem):
        if self.speed() > 0:
            new_place = ecosystem.biotope.seek_free_pos_close_to(self.position(), self.speed(), 3)
            if new_place != None:
                ecosystem.biotope.move_org(self, new_place)
                self.Data['status']['coordinates'] = coordinatesDict(new_place)
        pass

    def eat(self, organism, ecosystem):
        pass

    def do_photosynthesis(self, ecosystem):
        pass

    def procreate(self, ecosystem):
        # TEMPORARY EXAMPLE
        # add new organisms at the beginning of the list (as a queue)
        # using ecosystem.organisms.insert(0, new_organism)
        if (random() < REPRODUCTION_FREQUENCY) and (self.status()['energy'] > 5):
            newLocation = ecosystem.biotope.seek_free_pos_close_to(self.position(), 3, 3)
            if newLocation != None:    
                print ('Oh organism %d-th had a baby:' % ecosystem.organisms.index(self))
                baby = self.copy()
                baby.setLocation(newLocation)
                ecosystem.newborns.append(baby)  # Mutation?
                print 'Num of organisms: %d' % len(ecosystem.organisms)
                return 1
            else:
                return 0
        else:
            return 0

    def check_if_die_and_delete(self, ecosystem):
        # Temporary random delete
        from random import random
        if random() > 0.98:
            print ('%d-th organism DIED:' %
                   ecosystem.organisms.index(organism))
            ecosystem.organisms.remove(organism)
            print 'Num of organisms: %d' % len(ecosystem.organisms)
            return 1
        else:
            return 0
