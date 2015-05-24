from random import random
from copy import deepcopy
from Tools import *

actions_dictionary = {
    'do photosynthesis': lambda organism: organism.do_photosynthesis(),
    'move': lambda organism: organism.move(),
    'hunt': lambda organism: organism.hunt(),
    'interchange substances with the biotope': lambda organism: organism.interchange_substances_with_the_biotope(),
    'interchange substances with other organisms': lambda organism: organism.interchange_substances_with_other_organisms(),
    'fertilize other organisms': lambda organism: organism.fertilize_other_organisms(),
    'procreate if possible': lambda organism: organism.procreate_if_possible(),
    'stay alive': lambda organism: organism.stay_alive(),
    'age': lambda organism: organism.age()
}

class Organism(dict):

    def __init__(self, parent_ecosystem, organism_data = None):
        self.parent_ecosystem = parent_ecosystem
        for key in organism_data:
            self[key] = organism_data[key]
    
    def __str__(self, indent_level = 0, list_of_attributes = None):  # Just for debug
        if (list_of_attributes == None) or len(list_of_attributes) == 0:
            return dictionary_to_string(self, indent_level)
        else:
            if isinstance(list_of_attributes, str):
                return self[list_of_attributes].__str__()                
            elif len(list_of_attributes) == 1:
                return self[list_of_attributes[0]].__str__()
            else:
                return " ".join((attribute, self[attribute]).__str__() for attribute in list_of_attributes if attribute in self)
            
    def act(self):
        for action in self['actions list']:
            actions_dictionary[action](self)
        if self.parent_ecosystem.constraints['dying'](self):
            #print "dying alone", self.__str__(list_of_attributes = ('category', 'age', 'energy reserve'))
            self.die()
                       
    def subtract_outlays(self, action, factor = 1):
        if action in self.parent_ecosystem.outlays:
            for reserve_substance in self.parent_ecosystem.outlays[action]:                       
                if reserve_substance in self:
                    print " - " + self.__str__(0, ('category', 'age', 'energy reserve')), 
                    self[reserve_substance] = max(0, self[reserve_substance] - factor * self.parent_ecosystem.outlays[action][reserve_substance](self)  )                  
                    print "--> " + self.__str__(0, 'energy reserve')

    def interchange_substances_with_the_biotope(self):
        pass

    def interchange_substances_with_other_organisms(self):
        """ 
        Peacefull trade of substances:
            Each organism has a list of offers for other organisms that can 
        buy or not. An organism may want to sell its surplus of certain substances 
        in exchange for other substances that it needs. It offers an 
        amount of substance and a price (i. e. a ratio) in terms of other
        substance.
        
        Not so pacefull interchange of substances:
            An organism can stole a part of substance reserves from other organisms,
        as herbivorous do with plants, or as parasites do with their hosts.
            An organism may also inject a substance to other organism in order
        to kill it or damage it in self-defense of to eat it after it dies.
        """
        pass

    def fertilize_other_organisms(self):
        """ To partially transmit its own genes to other organisms that
        accepts them in order to produce a new being that inherit genes from
        both parents
        """
        pass
    
    
    def stay_alive(self):
        """ An organism has to spend energy and maybe other substances only to
        stay alive.
        """
        self.subtract_outlays('stay alive')            

    def move(self):
        """
            Check if there is a new available location. If yes
            then: - Update biotope (organisms matrix)
                  - Update location
        """
        # 1. Check if this organism can move itself:
        if 'speed' in self:
            # 2. Check if this organism decide to move:
            if (('move?' in self) and self['move?']()) or not 'move?' in self:
                # 3. Get a new location:
                new_location = self.parent_ecosystem.biotope.seek_free_location_close_to(self['location'], self['speed'])
                # 4. Check if it has found a new location:
                if new_location != None:
                    old_location = self['location']
                    # 5. Update location
                    self['location'] = new_location
                    # 6. Update biotope (organisms matrix):
                    self.parent_ecosystem.biotope.move_organism(old_location, new_location)
                    # 7. The outlays are proportional to the distance we have jump:                    
                    self.subtract_outlays('move', factor = self.parent_ecosystem.biotope.distance(old_location, new_location))

                        
    def move2(self): 
        """
            Check if there is a new available location. If yes
            then: - Update biotope (organisms matrix)
                  - Update location
        """
        # No todos los organismos tienen por que usar la funcion "seek_free_location_close_to(center, radius)"    
        # para buscar un sitio al que moverse. Algun organismo puede usar una 
        # funcion mas inteligente, que dependa de la concentracion de determinada
        # sustancia o del gradiente de densidad de poblacion de determinada especie.
        # O tambien puede haber otros que decidan moverse siempre en linea recta
        # hasta que se topen con algo. Hay infinidad de maneras de moverse.
        
        # Por eso podriamos usar este metodo en lugar del anterior. La dejo aqui por si lo usamos en un futuro.
        # Esta es una forma alternativa de definir el movimiento. Lo considera
        # un cambio de estado como otro cualquiera. Un organismo puede ser capaz
        # de moverse de una determinada manera al igual que otro organismo puede
        # ser capaz de cambiar cualquier otro status interno de alguna otra manera.

        # Tenemos que decidir si usamos este metodo move o el anterior. La unica
        # diferencia para el usuario seria la manera de definir el movimiento
        # en ecosystem_settings
        
        # 1. Check if this organism can move itself:
        if 'location' in self['modifying status']:
            # 2. Check if this organism decide to move:
            if self['modifying status']['location']['will change?'](self):
                # 3. Get a new location:
                new_location = self['modifying status']['location']['new value'](self)
                # 4. Check if it has found a new location:
                if new_location != None:
                    old_location = self['location']
                    # 5. Update location
                    self['location'] = new_location
                    # 6. Update biotope (organisms matrix):
                    self.parent_ecosystem.biotope.move_organism(old_location, new_location)
                    # 7. The outlays are proportional to the distance we have jump:                    
                    self.subtract_outlays('move', factor = self.parent_ecosystem.biotope.distance(old_location, new_location))

    def eat(self, prey):
        for reserve_substance in prey['list of reserve substances']:
            if reserve_substance in self:
                #print 'eating', prey['category'], self[reserve_substance], "+", prey[reserve_substance], "=",                 
                self[reserve_substance] += prey[reserve_substance]
                storage_capacity = self.parent_ecosystem.storage_capacities_dictionary[reserve_substance] 
                if storage_capacity in self:
                    self[reserve_substance] = min(self[reserve_substance], self[storage_capacity])
                #print self['energy reserve']
        self.subtract_outlays('eat')
                
    def hunt(self):
        prey_location = None
        if 'seeking prey technique' in self:            
            prey_location = self['seeking prey technique'](self)
        else:
            if 'attack capacity' in self:
                prey_location = self.parent_ecosystem.biotope.seek_possible_prey_close_to(
                    center = self['location'],
                    radius = 4.5) # the radius should be in the genes
        if prey_location != None:
            prey = self.parent_ecosystem.biotope.get_organism(prey_location)
            if self.parent_ecosystem.constraints['hunting'](predator = self, prey = prey):
                self.eat(prey)
                prey.die('killed by a predator')  
            self.subtract_outlays('hunt', factor = self.parent_ecosystem.biotope.distance(self['location'], prey_location))

    def do_photosynthesis(self):
        if ('photosynthesis capacity' in self) and ('energy reserve' in self):
            if isinstance(self['photosynthesis capacity'], FunctionType):               
                self['energy reserve'] += self['photosynthesis capacity'](self)
            else:
                self['energy reserve'] += self['photosynthesis capacity']
            if ('energy storage capacity' in self):
                if isinstance(self['energy storage capacity'], FunctionType):                   
                    self['energy reserve'] = min(self['energy reserve'], self['energy storage capacity'](self))   
                else:
                    self['energy reserve'] = min(self['energy reserve'], self['energy storage capacity'])   
        
    def mutate(self):
        for mutating_gene in self['mutating genes']:
            if self['mutating genes'][mutating_gene]['will mutate?'](self):
                self[mutating_gene] = self['mutating genes'][mutating_gene]['new value'](self)

    def procreate_if_possible(self):
        """
            Depending on the reproduction frequency and the energy,
            a baby can be created and added to:
              - the organisms matrix in biotope
              - the list of organisms in parent_ecosystem
            Return true if procreated, else return false.
        """
        procreated = False
        # Check weather the organism can procreate:
        if self.parent_ecosystem.constraints['procreating'](self):
            # Get a new location for the new baby:
            if 'radius of procreation' in self:
                radius_of_procreation = self['radius of procreation']
            else:
                radius_of_procreation = 1.5
            new_location = self.parent_ecosystem.biotope.\
                seek_free_location_close_to(center = self['location'], radius = radius_of_procreation)
            if new_location != None: # if there is enough space:
                # Create the baby:
                newborn = deepcopy(self)
                newborn['location'] = new_location
                if 'age' in newborn:
                    newborn['age'] = 0
                # Trigger mutations:
                newborn.mutate()
                # The parent and the child share reserves:
                for reserve_substance in self['list of reserve substances']:
                    newborn[reserve_substance] = newborn['energy reserve at birth'] 
                    self[reserve_substance] -= newborn[reserve_substance]
                    pass
                # Add the new organism to the ecosystem:
                self.parent_ecosystem.add_organism(newborn)
                self.subtract_outlays('procreate', self.parent_ecosystem.biotope.distance(self['location'], new_location))
                procreated = True
        return procreated

    def age(self):
        if 'age' in self:
            self['age'] += 1
    
    def die(self, cause = 'natural deth'):
        # self.parent_ecosystem.delete_organism(self) # parent_ecosystem tells biotope to erase organism from it
        print 'dying', self.__str__(list_of_attributes = ('category', 'age', 'energy reserve')), cause        
        self.parent_ecosystem.new_deads.append(self)
