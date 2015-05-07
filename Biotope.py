from random import random
import initial_settings
import Tools
import Organism


class Biotope(object):

    def __init__(self, biotope_data, parent_ecosystem):
        self.biotope_data = biotope_data
        self.parent_ecosystem = parent_ecosystem
        self.organisms_matrix = Tools.Matrix(size_x, size_y)
        self.substances_dict = {}

    def __getitem__(self, keys):
        return self.biotope_data[keys]

    def __setitem__(self, keys, value):
        self.biotope_data[keys] = value

    def __str__(self):  # Just for debug
        return str(self.organisms_matrix)

    def add_substance(substance):
        self.substances_dict[substance.code] = substance

    def set_parent_ecosystem(self, parent_ecosystem):
        """
            Set self.parent_ecosystem, and add all organisms
            to self.organisms_matrix.
        """
        self.parent_ecosystem = parent_ecosystem
        for organism in self.parent_ecosystem.organisms:
            coordinates = organism['status']['coordinates']
            self.add_organism(organism, coordinates)

    def add_organism(self, organism, coordinates):
        (x, y) = coordinates
        self.organisms_matrix[x, y] = organism

    def move_organism(self, organism, new_coordinates):
        (new_x, new_y) = new_coordaintes
        (old_x, old_y) = organism['status']['coordinates']
        self.organismsArray[old_x, old_y] = None
        self.organismsArray[new_x, new_y] = organism

    def delete_organism(self, coordinates):
        (x, y) = coordinates
        self.organismsArray[x, y] = None

    def location_is_ok(self, coordinates):
        (x, y) = coordinates
        (size_x, size_y) = self['geography']['dimensions']
        return ((x >= 0) and (y >= 0) and
                (x < size_x) and (y < size_y))

    def seek_free_position(self, attempts=10):
        """
            This is used by an organism in order to move to an empty place
            or to give birth to a new organism in an empty place
        """
        # TODO: Yo tendría una lista de posiciones libres en el biotope.
        #       cada vez que se add o delete un organismo, se modificaría esta
        #       lista. Así no hay que hacer attemps.
        for i in range(attempts):
            x = int(random() * self.size_x) % self.size_x
            y = int(random() * self.size_y) % self.size_y
            if (self.organismsArray[x, y] == None):
                return (x, y)
        return None

    def seek_free_pos_close_to(self, center, radius, attempts=1):
        # This is used by an organism in order to move to an empty place
        # or to give birth to a new organism in an empty place
        # TODO: La misma idea de la lista que en el método anterior
        (size_x, size_y) = self['geography']['dimensions']
        for i in range(attempts):
            x = int(center[0] + Tools.sRandom() * radius) % size_x
            y = int(center[1] + Tools.sRandom() * radius) % size_y
            if (self.organismsArray[x, y] == None):
                return (x, y)
        return None

    def get_substance(self, substance_code):
        return self.substances[substance_code]

    def evolve(self):
        for substance in self.substances_dict.values():
            substance.spread()
