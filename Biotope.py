from random import *
from math import *
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
        
    def move_organism(self, old_location, new_location):
        self.organisms_matrix[new_location] = self.organisms_matrix[old_location]
        self.organisms_matrix[old_location] = None
        
    def delete_organism(self, location):
        self.organisms_matrix[location] = None

    def seek_free_location(self):
        """
            This method return a random free position 
            (None if not possible)
        """
        return self.random_locations.get_new_location()
        
    def seek_free_location_close_to(self, center, radius, mode = 'circle'):
        """ 
            This method return a random free position close to a center within
            a radius (None if not possible)
        """
        (xc, yc) = center
        left = int(round(xc - radius))
        right = int(round(xc + radius))
        up = int(round(yc - radius))
        down = int(round(yc + radius))
        if mode in {'square', 'chess'}:
            list_of_free_locations = [(x, y) for x in range(left, right) for y in range(up, down) if (self.organisms_matrix[x, y] == None)]
        elif mode in {'circle', 'euclidean'}:
            list_of_free_locations = [(x, y) for x in range(left, right) for y in range(up, down) if (self.organisms_matrix[x, y] == None) and ((x-xc)**2 + (y-yc)**2 <= radius**2)]
        elif mode in {'tilted square', 'taxist'}:
            list_of_free_locations = [(x, y) for x in range(left, right) for y in range(up, down) if (self.organisms_matrix[x, y] == None) and (abs(x-xc) + abs(y-yc) <= radius)]        
        if list_of_free_locations == []:
            return None
        else:
            (x, y) = choice(list_of_free_locations)
            return (x % self['size'][0], y % self['size'][1])
            
    def distance(self, A, B, mode = 'circle'): 
        """
            Gives the distance from the location A to the location B, taking 
            into account that coordinates are taken (x % size_x, y % size_y)
            and, thus, the location (size_x, size_y) is equivalent to (0, 0),
            so the distance between the locations (0, 0) and (size_x - 1, size_y - 1)
            is really small
        """
        if hasattr(A, '__iter__') and hasattr(B, '__iter__') and (len(A)==2) and (len(B)==2):
            size_x, size_y = self['size']
            Ax, Ay, Bx, By = A[0] % size_x, A[1] % size_y, B[0] % size_x, B[1] % size_y
            dif_x = min(abs(Bx - Ax), size_x - abs(Bx - Ax))
            dif_y = min(abs(By - Ay), size_y - abs(By - Ay))
            if mode in {'square', 'chess'}:
                return max(dif_x, dif_y)
            elif mode in {'circle', 'euclidean'}:
                return sqrt(dif_x**2 + dif_y**2)
            elif mode in {'tilted square', 'taxist'}:
                return dif_x + dif_y
        else:
            return None


    def get_featuremap(self, featuremap_code):
        return self.featuremaps[featuremap_code]

    def evolve(self):
        """ SALAS:
        TO DO: Posteriormente habra que definir el "clima", que consistira en cierto regimen de "lluvia" de distintas substancias, como agua, luz solar o sales minerales,
        que iran apareciendo en el biotopo y de las cuales se iran alimentando los organismos. Las sales minerales van apareciendo por la disolucion de las rocas.
        """
        for featuremap in self.featuremaps_dict.values():
            featuremap.spread()
























