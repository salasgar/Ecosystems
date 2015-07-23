from random import *
from math import *
#from Basic_tools import *
import Organism

class Feature(object):
    def __init__(self, feature_settings, parent_ecosystem):
        self.parent_ecosystem = parent_ecosystem
        initial_value_generator = make_function(feature_settings['initial value'], [])
        self.current_value = initial_value_generator(self.parent_ecosystem)
        if 'value after updating' in feature_settings:
            self.calculate_value_after_update = \
                make_function(feature_settings['value after updating'], [])
            if 'update once every' in feature_settings:
                self.update_once_every = feature_settings['update once every']
            else:
                self.update_once_every = 1
            self.time_of_next_update = self.parent_ecosystem.time + self.update_once_every

    def update(self): # or   def evolve(self):
        if hasattr(self, 'time_of_next_update') and self.parent_ecosystem.time > self.time_of_next_update:
            self.current_value = self.calculate_value_after_update(self.parent_ecosystem)
            self.time_of_next_update += self.update_once_every

    def get_value(self):
        return self.current_value

    def set_value(self, new_value):
        self.current_value = new_value
        return new_value

    def modify_proportionally(self, proportion):
        value = self.get_value()
        increment = proportion * value
        self.set_value(value + increment)
        return increment

    def modify(self, increment):
        value = self.get_value() + increment
        self.set_value(value)
        return increment

class Feature_map(object):
    def __init__(self, feature_settings, parent_ecosystem):
        self.parent_ecosystem = parent_ecosystem
        (self.size_x, self.size_y) = feature_settings['matrix size']
        (size_x, size_y) = (self.size_x, self.size_y)
        initial_value_generator = make_function(feature_settings['initial value #x #y'], [], tags_list = ['#x', '#y'])
        self.current_value = Matrix(size_x, size_y)
        for i in range(size_x):
            for j in range(size_y):
                self.current_value[i, j] = \
                    initial_value_generator(self.parent_ecosystem, i/size_x, j/size_y)
        if 'value after updating #x #y' in feature_settings:
            self.calculate_value_after_update = \
                make_function(feature_settings['value after updating #x #y'], [], tags_list = ['#x', '#y'])
            if 'update once every' in feature_settings:
                self.update_once_every= feature_settings['update once every']
            else:
                self.update_once_every = 1
            self.time_of_next_update = self.parent_ecosystem.time + self.update_once_every
    
    def update(self): # or   def evolve(self):
        if hasattr(self, 'time_of_next_update') and self.parent_ecosystem.time > self.time_of_next_update:
            for i in range(size_x):
                for j in range(size_y):
                    self.current_value[i, j] = \
                        self.calculate_value_after_update(self.parent_ecosystem, i/size_x, j/size_y)
            self.time_of_next_update += self.update_once_every

    def get_value(self, x, y):
        return self.current_value[round(x * self.size_x), round(y * self.size_y)]

    def set_value(self, x, y, new_value):
        self.current_value[round(x * self.size_x), round(y * self.size_y)] = new_value
        return new_value

    def modify_proportionally(self, x, y, proportion):
        value = self.get_value(x, y)
        increment = proportion * value
        self.set_value(x, y, value + increment)
        return increment

    def modify(self, x, y, increment):
        value = self.get_value(x, y) + increment
        self.set_value(x, y, value)
        return increment

class Biotope(object):
    
    class random_free_locations_list(object):
        def __init__(self, parent_biotope): # warning: this is not the __init__ method of Biotope class!
            self.parent_biotope = parent_biotope
            self.reset()
        def reset(self):
            size = self.parent_biotope['size']
            self.list = [(x, y) for x in range(size[0]) for y in range(size[1])]
            shuffle(self.list)
            self.last_location_index = len(self.list) - 1           
        def get_new_free_location(self):
            if len(self.list) == 0:
                return None
            i = (self.last_location_index + 1)%len(self.list)
            while (self.parent_biotope.organisms_matrix[self.list[i]] != None) and (i != self.last_location_index):
                i = (i+1)%len(self.list)
            if self.parent_biotope.organisms_matrix[self.list[i]] == None:
                self.last_location_index = i
                return self.list[i]
            else:
                return None # Error: Full biotope. There're no more free locations 

    def __init__(self, settings, parent_ecosystem):
        self.settings = settings
        self.parent_ecosystem = parent_ecosystem
        self.organisms_matrix = Matrix(*self.settings['size'])
        self.initialize_feature_maps()
        self.random_free_locations = self.random_free_locations_list(self)
        # The 'distance' between two points A and B is subjective. Depends on
        # the topology of the biotope (currently it's a flat torus) and the
        # metric we use (euclidean, chess, taxicab,...). So, we define:      
        if 'distance' in self.settings:
            self.set_distance(self.settings['distance'])
        else:
            self.set_distance('euclidean distance')
        
    def __getitem__(self, keys):
        return self.settings[keys]

    def __setitem__(self, keys, value):
        self.settings[keys] = value

    def __str__(self):
        return str(self.organisms_matrix)
    
    def size_x(self):
        return self['size'][0]

    def size_y(self):
        return self['size'][1]

    def print_matrix(self):
        for y in range(self.size_y()):
            print [0 if self.organisms_matrix[x, y] == None else 1 for x in range(self.size_x())]
   
    def add_feature(self, feature_name, feature_settings):
        self.features[feature_name] = Feature(feature_settings, self.parent_ecosystem)

    def add_feature_map(self, feature_name, feature_settings):
        self.features[feature_name] = Feature_map(feature_settings, self.parent_ecosystem)

    def initialize_feature_maps(self):
        if 'biotope features' in self.settings:
            for feature in self.settings['biotope features']:
                if 'matrix size' in self.settings['biotope features'][feature]:
                    self.add_feature_map(feature, self.settings['biotope features'][feature])
                else:
                    self.add_feature(feature, self.settings['biotope features'][feature])

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
    def get_organism(self, location):
        return self.organisms_matrix[location]
        
    def add_organism(self, organism, location = 'find location'):
        if location == 'find location':
            if 'location' in organism.keys():
                location = organism['location']
            else:
                location = self.seek_free_location()
        if (location != None) and (self.organisms_matrix[location] == None):            
            organism['location'] = location # this way we assure that everything is in its place
            self.organisms_matrix[location] = organism
            #print "in", location, "there is", organism
            return 'success'
        else:
            return 'fail'
        
    def move_organism(self, old_location, new_location):
        if old_location != new_location:
            self.organisms_matrix[new_location] = self.organisms_matrix[old_location]
            self.organisms_matrix[old_location] = None
        
    def delete_organism(self, location):
        if location:
            self.organisms_matrix[location] = None

    def seek_free_location(self):
        """
            This method return a random free position 
            (None if not possible)
        """
        return self.random_free_locations.get_new_free_location()
        
    def list_of_locations_close_to(self, center, radius, condition = lambda x: (x==None)):
        (xc, yc) = center
        # borders of a square around center (xc, yc):
        left = int(round(xc - radius))
        right = int(round(xc + radius)) + 1 # we write + 1 because range(a, b+1) = [a, a+1, a+1, ..., b] = [a, ..., b]
        up = int(round(yc - radius))
        down = int(round(yc + radius)) + 1  # we write + 1 because range(a, b+1) = [a, a+1, a+1, ..., b] = [a, ..., b]
        return [(x, y) for x in range(left, right) for y in range(up, down) if condition(self.organisms_matrix[x, y]) and (self.distance(center, (x, y)) <= radius)]
                
    def seek_free_location_close_to(self, center, radius):
        """ 
            This method return a random free position close to a center within
            a radius (None if not possible)
        """
        list_of_free_locations = self.list_of_locations_close_to(center, radius, lambda x: (x==None))
        if list_of_free_locations == []:
            return None
        else:
            (x, y) = choice(list_of_free_locations)
            return (x % self['size'][0], y % self['size'][1])
    
    def seek_possible_prey_close_to(self, center, radius, condition = None):
        if condition == None:
            condition = lambda x: (x != None) and (x['location'] != center)
        list_of_locations = self.list_of_locations_close_to(center, radius, condition)
        if list_of_locations == []:
            return None
        else:
            (x, y) = choice(list_of_locations)
            return (x % self['size'][0], y % self['size'][1])
            
            
    def calculate_distance(self, A, B, distance = 'euclidean distance'): 
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
            if distance in {'square', 'chess', 'chess distance'}:
                return max(dif_x, dif_y)
            elif distance in {'circle', 'euclidean', 'euclidean distance'}:
                return sqrt(dif_x**2 + dif_y**2)
            elif distance in {'tilted square', 'taxicab', 'taxist', 'taxist distance', 'taxicab distance'}:
                return dif_x + dif_y
        else:
            return None

    def set_distance(self, distance):
        if is_function(distance):
            self.distance = distance
        elif isinstance(distance, str):            
            self.distance = lambda A, B: self.calculate_distance(A, B, distance)
        
    def get_featuremap(self, featuremap_code):
        return self.featuremaps[featuremap_code]

    def evolve(self):
        """ SALAS:
        TO DO: Posteriormente habra que definir el "clima", que consistira en cierto regimen de "lluvia" de distintas substancias, como agua, luz solar o sales minerales,
        que iran apareciendo en el biotopo y de las cuales se iran alimentando los organismos. Las sales minerales van apareciendo por la disolucion de las rocas.
        """
        for featuremap in self.featuremaps_dict.values():
            featuremap.spread()
























