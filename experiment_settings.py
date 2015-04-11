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
biotope = {'status': {'temperature': 100}}
