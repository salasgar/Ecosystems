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
        pass

    def move(self):
        """
            Check if there is a new available location. If yes
            then: - Update biotope (organisms matrix)
                  - Update location
        """
        # 1. Get organism current data
        speed = self['speed']
        old_location = self['location']
        if speed > 0:
            # 2. Check if there is a new free location
            new_location = ecosystem.biotope.seek_free_location_close_to(
                old_location, radius=speed)
            if new_location is not None:
                # 3. Update biotope (organisms matrix)
                self.parent_ecosystem.biotope.move_organism_in_matrix(
                    self, new_location)
                # 4. Update location
                self.set_location(new_location)

    def eat(self, organism):
        pass
    
    def hunt(self):
        pass

    def do_photosynthesis(self):
        if ('photosynthesis_capacity' in self) and ('energy reserve' in self):
            self['energy reserve'] += 'photosynthesis_capacity'
            if ('energy storage capacity' in self):
                self['energy reserve'] = min(self['energy reserve'], self['energy storage capacity'])   

    def procreate_if_possible(self):
        """
            Depending on the reproduction frequency and the energy,
            a baby can be created and added to:
              - the organisms matrix in biotope
              - the list of organisms in parent_ecosystem
            Return true if procreated, else return false.
        """
        procreated = False
        # 1. Get organism current data
        reproduction_frequency = self['reproduction_frequency']
        location = self['location']
        energy_threshold = 5  # TODO: Define in genes

        # 2. Check if it is the moment to reproduce
        if ((random() < reproduction_frequency) and
                (self['energy'] > energy_threshold)):
            # 3. Find a new location in the biotope.
            new_location = self.parent_ecosystem.\
                biotope.seek_free_location_close_to(location, radius=3)
            # TODO: Why 3? Define elsewhere
            if new_location is not None:
                # 4. Create a baby
                # 4.1. Create a exact copy of self
                baby = deepcopy(self)
                # 4.2. Split substances between self and baby
                # TODO: Why divide by 2? Maybe baby is much smaller... check.
                """
                TODO: Rethink this
                for substance_code in self.substances.keys():
                    baby.variate_substance(
                        substance_code,
                        -1.0 * baby.amount_of_substance(substance_code) / 2)
                    self.variate_substance(
                        substance_code,
                        -1.0 * baby.amount_of_substance(substance_code) / 2)
                """
                # 4.3. Set location of baby
                baby.set_location(new_location)
                # 4.4. Add organism in organisms matrix in biotope
                self.parent_ecosystem.biotope.add_organism(baby,
                                                           new_location)
                # 4.5. Add organism to parent ecosystem
                self.parent_ecosystem.organisms_list.append(baby)
                procreated = True
        return procreated

    def age(self):
        if 'age' in self:
            self['age'] += 1
