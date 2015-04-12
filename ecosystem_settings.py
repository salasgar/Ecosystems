# inviduals and biotope creation

from random import random


def add_individual_to_biotope(individual, biotope):
    x = individual['status']['coordinates']['x']
    y = individual['status']['coordinates']['y']
    biotope['array_of_individuals'][x][y] = individual


def create_empty_list_of_lists(size_x, size_y):
    return [[None for i in range(size_x)] for j in range(size_y)]

# Creation of biotope
BIOTOPE_SIZE_X = 100
BIOTOPE_SIZE_Y = 100

biotope = {
    'size': {'x': BIOTOPE_SIZE_X, 'y': BIOTOPE_SIZE_Y},
    'array_of_individuals':  create_empty_list_of_lists(BIOTOPE_SIZE_X,
                                                        BIOTOPE_SIZE_Y),
    'status': {'temperature': 100}
    }

# Creation of inviduals
individuals = []
for i in range(0, 10):
    individual = {'genes': {'attack_capacity':  random() * 5.0,
                            'defense_capacity': random() * 3.0,
                            'speed': 0.0,
                            'do_photosynthesis': True},
                  'status': {'energy': 10,
                             'age': 50,
                             'coordinates': {
                                 'x': int(random()*BIOTOPE_SIZE_X),
                                 'y': int(random()*BIOTOPE_SIZE_Y)}
                             }
                  }
    individuals.append(individual)

# Add individuals references in biotope
for individual in individuals:
    add_individual_to_biotope(individual, biotope)
