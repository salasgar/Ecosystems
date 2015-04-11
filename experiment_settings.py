# inviduals and biotope creation

from random import random

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
                                 'x': random(),
                                 'y': random()}
                             }
                }
    individuals.append(individual)

# Creation of biotope


BIOTOPE_SIZE_X = 100;
BIOTOPE_SIZE_Y = 100;

biotope = {
    'size' : {'x': BIOTOPE_SIZE_X, 'y': BIOTOPE_SIZE_Y},
    'array_of_individuals':  [[None for i in range(BIOTOPE_SIZE_X)] for j in range(BIOTOPE_SIZE_Y)],
    'status': {'temperature': 100}
    }
