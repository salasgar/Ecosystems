from random import *
from math import *
# from Basic_tools import *
# import Organism
from SYNTAX import *


class Feature(object):  # A float variable

    def __init__(self, feature_name, feature_settings, parent_ecosystem):
        self.feature_name = feature_name
        self.parent_ecosystem = parent_ecosystem
        functions_dict = parent_ecosystem.function_maker\
            .turn_settings_into_functions(
                feature_settings,
                caller='#ecosystem'
            )
        self.current_value = functions_dict['initial value'](
            self.parent_ecosystem)
        if 'value after updating' in functions_dict:
            self.calculate_value_after_update = functions_dict[
                # we take the function without calling it
                'value after updating']
            if 'update once every' in functions_dict:
                self.update_once_every = functions_dict[
                    'update once every'](self.parent_ecosystem)
            else:
                self.update_once_every = 1
            self.time_of_next_update = \
                self.parent_ecosystem.time + self.update_once_every

    def update(self):  # or def evolve(self):
        # print 'Updating', self.feature_name # ***
        if (
            hasattr(self, 'time_of_next_update') and
            self.parent_ecosystem.time > self.time_of_next_update
        ):
            self.current_value = self.calculate_value_after_update(
                self.parent_ecosystem)
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


class Feature_map(object):  # A function f(x, y)

    def __init__(self, feature_name, feature_settings, parent_ecosystem):
        self.feature_name = feature_name
        self.parent_ecosystem = parent_ecosystem
        functions_dict = parent_ecosystem.function_maker.\
            turn_settings_into_functions(
                feature_settings,
                caller='#ecosystem'
            )
        (self.size_x, self.size_y) = feature_settings['matrix size']
        (size_x, size_y) = (self.size_x, self.size_y)
        self.current_value = Matrix(size_x, size_y)
        for i in range(size_x):
            for j in range(size_y):
                self.current_value[i, j] = \
                    functions_dict['initial value'](
                        self.parent_ecosystem,
                        float(i) / size_x,
                        float(j) / size_y)
        if 'value after updating' in functions_dict:
            self.calculate_value_after_update = functions_dict[
                'value after updating'
            ]  # we take the function without calling it
            if 'update once every' in functions_dict:
                self.update_once_every = functions_dict['update once every'](
                    self.parent_ecosystem)
            else:
                self.update_once_every = 1
            self.time_of_next_update = (
                self.parent_ecosystem.time + self.update_once_every)

    def update(self):  # or   def evolve(self):
        # print 'Updating', self.feature_name # ***
        if (
            hasattr(self, 'time_of_next_update') and
            self.parent_ecosystem.time > self.time_of_next_update
        ):
            new_value = Matrix(self.size_x, self.size_y)
            for i in range(self.size_x):
                for j in range(self.size_y):
                    new_value[i, j] = \
                        self.calculate_value_after_update(
                            self.parent_ecosystem,
                            float(i) / self.size_x,
                            float(j) / self.size_y)
            self.current_value = new_value
            self.time_of_next_update += self.update_once_every

    def get_value(self, x, y):
        # PRECONDITION:  0 <= x <= 1,  0 <= y <= 1
        for n in (x, y, self.size_x, self.size_y):
            if not is_number(n):
                print n, 'is not a FLOAT!!!'  # ***
                halt()
        return self.current_value[
            int(round(x * self.size_x)),
            int(round(y * self.size_y))
            ]

    def set_value(self, x, y, new_value):
        # PRECONDITION:  0 <= x <= 1,  0 <= y <= 1
        self.current_value[
            int(round(x * self.size_x)),
            int(round(y * self.size_y))
            ] = new_value
        return new_value

    def modify_proportionally(self, x, y, proportion):
        # PRECONDITION:  0 <= x <= 1,  0 <= y <= 1
        value = self.get_value(x, y)
        increment = proportion * value
        self.set_value(x, y, value + increment)
        return increment

    def modify(self, x, y, increment):
        # PRECONDITION:  0 <= x <= 1,  0 <= y <= 1
        value = self.get_value(x, y) + increment
        self.set_value(x, y, value)
        return increment


class Biotope(object):

    class random_free_locations_list(object):

        # warning: this is not the __init__ method of Biotope class!

        def __init__(self, parent_biotope):
            self.parent_biotope = parent_biotope
            self.reset()

        def reset(self):
            size = self.parent_biotope['size']
            self.list = [(x, y) for x in range(size[0])
                         for y in range(size[1])]
            shuffle(self.list)
            self.last_location_index = len(self.list) - 1

        def get_new_free_location(self):
            if len(self.list) == 0:
                return None
            i = (self.last_location_index + 1) % len(self.list)
            while (
                self.parent_biotope.organisms_matrix[self.list[i]] is not None
                and i != self.last_location_index
                    ):
                i = (i + 1) % len(self.list)
            if self.parent_biotope.organisms_matrix[self.list[i]] is None:
                self.last_location_index = i
                return self.list[i]
            else:
                # Error: Full biotope. There're no more free locations
                return None

    def __init__(self, settings, parent_ecosystem):
        self.settings = settings
        self.parent_ecosystem = parent_ecosystem
        self.organisms_matrix = Matrix(*self.settings['size'])
        self.initialize_biotope_features()
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
        return self.settings['size'][0]

    def size_y(self):
        return self.settings['size'][1]

    def print_matrix(self):
        for y in range(self.size_y()):
            print [
                0
                if self.organisms_matrix[x, y] is None
                else 1 for x in range(self.size_x())
                ]

    def add_feature(self, feature_name, feature_settings):
        # print 'add_feature:', feature_name # ***
        self.biotope_features[feature_name] = Feature(
            feature_name, feature_settings, self.parent_ecosystem)

    def add_feature_map(self, feature_name, feature_settings):
        # print 'add_feature_map:', feature_name # ***
        self.biotope_features[feature_name] = Feature_map(
            feature_name, feature_settings, self.parent_ecosystem)

    def initialize_biotope_features(self):

        """
            We don't need to initialize features in a particular
        order. That's why we don't initialize them the same way as genes or
        new operators. Features can refer to each other and can even refer to
        themselves, because we built feature operators (such as '#biotope
        seasons speed' or  'extract #biotope nutrient A') before initializing
        features themselves. We built them out of features' names.
        """

        if print_methods_names:
            print 'Biotope.py: initialize_biotope_features'  # ***
        self.biotope_features = {}
        if 'biotope features' in self.settings:
            for feature_name in self.settings['biotope features']:
                if 'matrix size' in self.settings[
                    'biotope features'][
                        feature_name
                        ]:
                    self.add_feature_map(
                        feature_name,
                        self.settings['biotope features'][feature_name]
                    )
                else:
                    self.add_feature(
                        feature_name,
                        self.settings['biotope features'][feature_name])
        if print_methods_names:
            print 'initialize_biotope_features done!!'  # ***

    def get_organism(self, location):
        return self.organisms_matrix[location]

    def add_organism(self, organism, location='find location'):
        if location == 'find location':
            if 'location' in organism.keys():
                location = organism['location']
            else:
                location = self.seek_free_location()
        if location is not None and self.organisms_matrix[location] is None:
            # this way we assure that everything is in its place
            organism['location'] = location
            self.organisms_matrix[location] = organism
            # print "in", location, "there is", organism # ***
            return 'success'
        else:
            return 'fail'

    def move_organism(self, old_location, new_location):
        if old_location != new_location:
            self.organisms_matrix[
                new_location] = self.organisms_matrix[old_location]
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

    def list_of_locations_close_to(
            self,
            center,
            radius,
            condition=lambda x: (x is None)
            ):
        (xc, yc) = center
        # borders of a square around center (xc, yc):
        left = int(round(xc - radius))
        # we write + 1 because range(a, b+1) = [a, a+1, a+1, ..., b] = [a, ...,
        # b]
        right = int(round(xc + radius)) + 1
        up = int(round(yc - radius))
        # we write + 1 because range(a, b+1) = [a, a+1, a+1, ..., b] = [a, ...,
        # b]
        down = int(round(yc + radius)) + 1
        return [
            (x, y)
            for x in range(left, right)
            for y in range(up, down)
            if (
                condition(self.organisms_matrix[x, y]) and
                self.distance(center, (x, y)) <= radius
                )
            ]

    def seek_free_location_close_to(self, center, radius):
        """
            This method return a random free position close to a center within
            a radius (None if not possible)
        """
        list_of_free_locations = self.list_of_locations_close_to(
            center,
            radius,
            lambda x: (x is None)
            )
        if list_of_free_locations == []:
            return None
        else:
            (x, y) = choice(list_of_free_locations)
            return (x % self['size'][0], y % self['size'][1])

    def seek_organism_close_to(self, center, radius, condition=None):
        def default_condition(organism):
            return (organism is not None) and (organism['location'] != center)
        if condition is None:
            condition = default_condition
        list_of_locations = self.list_of_locations_close_to(
            center, radius, condition)
        if list_of_locations == []:
            return None
        else:
            (x, y) = choice(list_of_locations)
            return (x % self['size'][0], y % self['size'][1])

    def calculate_distance(self, A, B, distance='euclidean distance'):
        """
            Gives the distance from the location A to the location B, taking
            into account that coordinates are taken (x % size_x, y % size_y)
            and, thus, the location (size_x, size_y) is equivalent to (0, 0),
            so the distance between the locations (0, 0) and
            (size_x - 1, size_y - 1) is really small
        """
        if (
            hasattr(A, '__iter__') and
            hasattr(B, '__iter__') and
            len(A) == 2 and
            len(B) == 2
                ):
            size_x, size_y = self['size']
            Ax, Ay, Bx, By = A[0] % size_x, A[
                1] % size_y, B[0] % size_x, B[1] % size_y
            dif_x = min(abs(Bx - Ax), size_x - abs(Bx - Ax))
            dif_y = min(abs(By - Ay), size_y - abs(By - Ay))
            if distance in {'square', 'chess', 'chess distance'}:
                return max(dif_x, dif_y)
            elif distance in {'circle', 'euclidean', 'euclidean distance'}:
                return sqrt(dif_x**2 + dif_y**2)
            elif distance in {
                'tilted square',
                'taxicab',
                'taxist',
                'taxist distance',
                'taxicab distance'
                    }:
                return dif_x + dif_y
        else:
            return None

    def set_distance(self, distance):
        if is_function(distance):
            self.distance = distance
        elif isinstance(distance, str):
            self.distance = lambda A, B: self.calculate_distance(
                A, B, distance)

    def evolve(self):
        for feature in self.biotope_features:
            self.biotope_features[feature].update()
