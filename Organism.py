from random import random
from copy import deepcopy


class Organism(object):

    def __init__(self,
                 organism_data,
                 parent_ecosystem):
        self.organism_data = organism_data
        self.parent_ecosystem = parent_ecosystem

    def __getitem__(self, keys):
        return self.organism_data[keys]

    def __setitem__(self, keys, value):
        self.organism_data[keys] = value

    def __str__(self):  # Just for debug
        return str(tuple(self['status']['age']))

    def set_location(self, (x, y)):
        self['status']['coordinates'] = (x, y)

    def move(self, ecosystem):
        """
            Check if there is a new available location. If yes
            then: - Update biotope (organisms matrix)
                  - Update location
        """
        # 1. Get organism current data
        speed = self['genes']['speed']
        old_coordinates = self['status']['coordinates']
        if speed > 0:
            # 2. Check if there is a new available location
            new_coordinates = ecosystem.biotope.seek_free_pos_close_to(
                old_coordinates, radius=speed)
            if new_coordinates is not None:
                # 3. Update biotope (organisms matrix)
                self.parent_ecosystem.biotope.move_organism_in_matrix(
                    self, new_coordinates)
                # 4. Update location
                self.set_location(new_coordinates)

    def eat(self, organism, ecosystem):
        pass

    def do_photosynthesis(self, ecosystem):
        photosynthesis_capacity = self['genes']['photosynthesis_capacity']
        ENERGY_RESERVE = 0  # TODO: Import from somewhere
        self.variate_substance(ENERGY_RESERVE, photosynthesis_capacity)

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
        reproduction_frequency = self['genes']['reproduction_frequency']
        coordinates = self['status']['coordinates']
        energy_threshold = 5  # TODO: Define in genes

        # 2. Check if it is the moment to reproduce
        if ((random() < reproduction_frequency) and
                (self['status']['energy'] > energy_threshold)):
            # 3. Find a new location in the biotope. If there is not
            #    free position, the baby won't be born.
            new_coordinates = self.parent_ecosystem.\
                biotope.seek_free_pos_close_to(coordinates, radius=3)
            # TODO: Why 3? Define elsewhere
            if coordinates is not None:
                # 4. Create a baby
                # 4.1. Create a exact copy of self
                baby = deepcopy(self)
                # 4.2. Split substances between self and baby
                # TODO: Why divide by 2? Maybe baby is much smaller... check.
                for substance_code in self.substances.keys():
                    baby.variate_substance(
                        substance_code,
                        - baby.amount_of_substance(substance_code) / 2)
                    self.variate_substance(
                        substance_code,
                        - baby.amount_of_substance(substance_code) / 2)

                # 4.3. Set location of baby
                baby.set_location(new_coordinates)
                # 4.4. Add organism in organisms matrix in biotope
                self.parent_ecosystem.biotope.add_organism(baby,
                                                           new_coordinates)
                # 4.5. Add organism to parent ecosystem
                self.parent_ecosystem.organisms_list.append(baby)
                procreated = True
        return procreated

    def age(self, ecosystem):
        longevity = self['genes']['longevity']
        self['status']['age'] += 1
        if self['status']['age'] > longevity:  # Die
            self.parent_ecosystem.biotope.delete_organism(self)
            self.parent_ecosystem.organisms_list.remove(self)
