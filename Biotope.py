from random import *
import initial_settings
import Tools
import Organism


class Biotope(object):
    class random_locations_list(object):
        def __init__(self, parent_biotope):
            self.parent_biotope = parent_biotope
            self.reset()
        def reset(self):
            size = self.parent_biotope['size']
            self.list = [(x, y) for x in range(size[0]) for y in range(size[1])]
            shuffle(self.list)
            self.last_location_index = len(self.list) - 1           
        def get_new_location(self):
            i = (self.last_location_index + 1)%len(self.list)
            while (self.parent_biotope.organisms_matrix[self.list[i]] != None) and (i != self.last_location_index):
                i = (i+1)%len(self.list)
            if self.parent_biotope.organisms_matrix[self.list[i]] == None:
                self.last_location_index = i
                return self.list[i]
            else:
                return None # Error: Full biotope. There're no more free locations 

    def __init__(self, biotope_data, parent_ecosystem):
        self.biotope_data = biotope_data
        self.parent_ecosystem = parent_ecosystem
        self.organisms_matrix = Tools.Matrix(*biotope_data['size'])
        self.featuremaps_dict = {}        
        self.random_locations = self.random_locations_list(self)

    def __getitem__(self, keys):
        return self.biotope_data[keys]

    def __setitem__(self, keys, value):
        self.biotope_data[keys] = value

    def __str__(self):  # Just sfor debug
        return str(self.organisms_matrix)
        
    def add_featuremap(featuremap):
        self.featuremaps_dict[featuremap.code] = featuremap

    def set_parent_ecosystem(self, parent_ecosystem):
        """
            Set self.parent_ecosystem, and add all organisms
            to self.organisms_matrix.
        """
        self.parent_ecosystem = parent_ecosystem
        for organism in self.parent_ecosystem.organisms:
            location = organism['location']
            self.add_organism(organism, location)
            """ SALAS:
            Deberiamos borrar los organismos que pueda haber previamente en este biotopo?
            """

    def add_organism(self, organism, location = None):
        if location == None:
            if 'location' in organism.keys():
                location = organism['location']
            else:
                location = self.seek_free_location()
                organism['location'] = location
        self.organisms_matrix[location] = organism
        
    def move_organism(self, organism, old_location, new_location):
        self.organisms_matrix[old_location] = None
        self.organisms_matrix[new_location] = organism

    def delete_organism(self, location):
        self.organisms_matrix[location] = None

    def location_is_ok(self, location):
        (x, y) = location
        (size_x, size_y) = self['dimensions']
        return ((x >= 0) and (y >= 0) and
                (x < size_x) and (y < size_y))

    def seek_free_location(self):
        """
            This method return a random free position 
            (None if not possible)
        """
        return self.random_locations.get_new_location()
        
    def seek_free_location_close_to(self, center, radius):
        """ 
            This method return a random free position close to a center within
            a radius (None if not possible)
        """
        # TODO: La misma idea de la lista que en el metodo anterior
        """ SALAS:
        Para la funcion anterior me parece muy buena idea, pero para esta no, ya que habria que guardar una lista para cada center y cada radius
        """
        pass 

    def get_featuremap(self, featuremap_code):
        return self.featuremaps[featuremap_code]

    def evolve(self):
        """ SALAS:
        TO DO: Posteriormente habra que definir el "clima", que consistira en cierto regimen de "lluvia" de distintas substancias, como agua, luz solar o sales minerales,
        que iran apareciendo en el biotopo y de las cuales se iran alimentando los organismos. Las sales minerales van apareciendo por la disolucion de las rocas.
        """
        for featuremap in self.featuremaps_dict.values():
            featuremap.spread()
