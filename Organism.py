from random import random

import Tools
import initial_settings

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
        return Tools.coordinatesTuple(self.Data['status']['coordinates'])     
    
    def setLocation(self, newLocation):
        self.Data['status']['coordinates'] = Tools.coordinatesDict(newLocation)
    
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
        if (random() < initial_settings.REPRODUCTION_FREQUENCY) and (self.status()['energy'] > 5):
            newLocation = ecosystem.biotope.seek_free_pos_close_to(self.position(), 3, 3)
            if newLocation != None:    
                print ('Oh organism %d-th had a baby:' % ecosystem.organisms.index(self))
                baby = Organism(self.Data.copy()) 
                # Mutation?
                baby.setLocation(newLocation)
                ecosystem.biotope.add_org(baby, newLocation)
                ecosystem.newborns.append(baby)  
                return 1
            else:
                return 0
        else:
            return 0

    def age(self, ecosystem):
        self.Data['status']['age'] += 1 
        if random()*self.Data['status']['age'] > initial_settings.GLOBAL_LONGEVITY:
            ecosystem.organisms.remove(self)
            ecosystem.biotope.delete_org(self)
            return 'Dead'
        else:
            return 'Still alive'

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








