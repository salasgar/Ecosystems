# inviduals and biotope creation

from random import random

# Creation of biotope
BIOTOPE_SIZE_X = 100;
BIOTOPE_SIZE_Y = 100;

biotope = {
    'size' : {'x': BIOTOPE_SIZE_X, 'y': BIOTOPE_SIZE_Y},
    'array_of_individuals':  [[None for j in range(BIOTOPE_SIZE_Y)] for i in range(BIOTOPE_SIZE_X)],
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

    biotope['array_of_individuals'][individual['status']['coordinates']['x']][individual['status']['coordinates']['y']] = individual
