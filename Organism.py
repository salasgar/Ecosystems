from random import random
from copy import deepcopy
from Tools import *


class Organism(dict):

    def __init__(self, parent_ecosystem, organism_data = None):
        self.parent_ecosystem = parent_ecosystem
        for key in organism_data:
            self[key] = organism_data[key]
    
    def __str__(self, indent_level = 0):  # Just for debug
        return dictionary_to_string(self, indent_level)
        
    def act(self):
        self.do_photosynthesis()
        self.move()
        self.hunt()
        self.procreate_if_possible()
        self.age()
        if self.parent_ecosystem.constraints['dying'](self):
            self.die()

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

    def move2(self):
        """
            Check if there is a new available location. If yes
            then: - Update biotope (organisms matrix)
                  - Update location
        """
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

    def eat(self, prey):
        for substance_reserve in prey['list of reserve substances']:
            if substance_reserve in self:
                self[substance_reserve] += prey[substance_reserve]
                storage_capacity = parent_ecosystem.storage_capacities_dictionary[substance_reserve] 
                if storage_capacity in self:
                    self[substance_reserve] = min(self[substance_reserve], self[storage_capacity])
    
    def hunt(self):
        if 'seeking prey technique' in self:            
            prey_location = self['seeking prey technique'](self)
        else:
            prey_location = self.parent_ecosystem.biotope.seek_possible_prey_close_to(
                center = self['location'],
                radius = 1.5)
        if prey_location != None:
            prey = self.parent_ecosystem.biotope.get_organism(prey_location)
            if self.parent_ecosystem.constraints['hunting'](predator = self, prey = prey):
                self.eat(prey)
                prey.die()            

    def do_photosynthesis(self):
        if ('photosynthesis_capacity' in self) and ('energy reserve' in self):
            self['energy reserve'] += 'photosynthesis_capacity'
            if ('energy storage capacity' in self):
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
                # Trigger mutations:
                newborn.mutate()
                # Add the new organism to the ecosystem:
                self.parent_ecosystem.add_organism(newborn)
                procreated = True
        return procreated

    def age(self):
        if 'age' in self:
            self['age'] += 1
            
    def die(self):
        parent_ecosystem.delete_organism(self) # parent_ecosystem tells biotope to erase organism from it
        
