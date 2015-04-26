from random import random
from Tools import coordinatesDict, coordinatesTuple
from copy import deepcopy
import initial_settings

class Organism(object):
    Data = None  # All organism's attributes (genes and status)
    
    def __init__(self, Data):
        self.Data = Data
    
    def __getitem__(self, keys):
        return self.Data[keys]
        
    def __setitem__(self, keys, value):
        self.Data[keys] = value        

    def __str__(self):
        return str(tuple(self.Data['status']['age']))

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
                ecosystem.biotope.move_organism(self, new_place)
                self.Data['status']['coordinates'] = coordinatesDict(new_place)

    def eat(self, organism, ecosystem):
        pass

    def do_photosynthesis(self, ecosystem):
        self.variate_substance(ENERGY_RESERVE, self.photosynthesis_capacity())

    def procreate(self, ecosystem):
        # TEMPORARY EXAMPLE
        # add new organisms at the beginning of the list (as a queue)
        # using ecosystem.organisms.insert(0, new_organism)
        if (random() < initial_settings.REPRODUCTION_FREQUENCY) and (self.status()['energy'] > 5):
            newLocation = ecosystem.biotope.seek_free_pos_close_to(self.position(), 3, 3)
            if newLocation != None:    
                baby = Organism(deepcopy(self.Data))
                # Reparto de reservas de sustancias:
                for SUSTANCE in self.substances.keys():
                    baby.variate_substance(SUSTANCE, - baby.amount_of_substance(SUSTANCE) / 2)
                    self.variate_substance(SUSTANCE, - baby.amount_of_substance(SUSTANCE) / 2)
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
            ecosystem.biotope.delete_org(self)
            return 'Dead'
        else:
            return 'Alive'








