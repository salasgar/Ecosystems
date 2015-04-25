# inviduals and biotope creation

from random import random

# Creation of biotope
BIOTOPE_SIZE_X = 10
BIOTOPE_SIZE_Y = 12

# Creation of inviduals
REPRODUCTION_FREQUENCY = 0.1
GLOBAL_LONGEVITY = 200

initial_organisms = []

N = 10 # Number of initial organisms of the following kind:
organism_data = {'genes': {'attack_capacity':  random() * 5.0,
                           'defense_capacity': random() * 100.0,
                           'speed': 0.0,
                           'do_photosynthesis': True},
                 'status': {'energy': 10,
                            'age': 0}
                }
initial_organisms.append((N, organism_data))

N = 10 # Number of initial organisms of the following kind:
organism_data = {'genes': {'attack_capacity':  random() * 100.0,
                           'defense_capacity': random() * 30.0,
                           'speed': 4.0,
                           'do_photosynthesis': False},
                 'status': {'energy': 10,
                            'age': 0}
                }
initial_organisms.append((N, organism_data))
    
#SUBSTANCES:
    
# Substance codes:
