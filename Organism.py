from random import random
from copy import deepcopy


class Organism(object):

    def __init__(self,
                 organism_settings,
                 parent_ecosystem):
        self.organism_settings = organism_settings
        self.parent_ecosystem = parent_ecosystem

    def __getitem__(self, key):
        return self.organism_settings[key]

    def __setitem__(self, key, value):
        self.organism_settings[key] = value

    def __str__(self):  # Just for debug
        return str(tuple(self['age']))

    def set_location(self, (x, y)):
        self['location'] = (x, y)

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

    def do_photosynthesis(self, ecosystem):
        pass

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

    def age(self, ecosystem):
        self['status']['age'] += 1
        if self['status']['age'] > self['longevity']:  # Die
            self.parent_ecosystem.biotope.delete_organism(self)
            self.parent_ecosystem.organisms_list.remove(self)
