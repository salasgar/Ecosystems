# inviduals and biotope creation

from random import random


def add_organism_to_biotope(organism, biotope):
    x = organism['status']['coordinates']['x']
    y = organism['status']['coordinates']['y']
    biotope['array_of_organisms'][x][y] = organism


def create_empty_list_of_lists(size_x, size_y):
    return [[None for i in range(size_x)] for j in range(size_y)]

# Creation of biotope
BIOTOPE_SIZE_X = 100
BIOTOPE_SIZE_Y = 100

biotope = {
    'size': {'x': BIOTOPE_SIZE_X, 'y': BIOTOPE_SIZE_Y},
    'array_of_organisms':  create_empty_list_of_lists(BIOTOPE_SIZE_X,
                                                      BIOTOPE_SIZE_Y),
    'status': {'temperature': 100}
    }

# Creation of inviduals
organisms = []
for i in range(0, 10):
    organism = {'genes': {'attack_capacity':  random() * 5.0,
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
    organisms.append(organism)

# Add organisms references in biotope
for organism in organisms:
    add_organism_to_biotope(organism, biotope)
