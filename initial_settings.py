# inviduals and biotope creation

from random import random

# Creation of biotope
BIOTOPE_SIZE_X = 4
BIOTOPE_SIZE_Y = 8

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
# Substances spread in the biotope:
NO_SUBSTANCE = 0
WATER = 1
CARBON_DIOXIDE = 2
OXIGEN = 3
NITRATE = 4
PHOSPHATE = 5
POISON = 10
POISON1 = 11
POISON2 = 12
FOOD = 13
FOOD1 = 14
FOOD2 = 15
TEMPERATURE = 101  
SUNLIGHT = 102  # Is there an equivalence between ENERGY and SUNLIGHT  ???
RAIN = 103 # The presence of RAIN increases the amount of WATER in the soil, and in the end, if there is enought humidity, it become DEPTH
ALTITUDE = 104
DEPTH = 105  # Depth of a sea, a lake or a river
# Substances inside organisms:
WATER_RESERVE = 201
NITRATE_RESERVE = 204
PHOSPHATE_RESERVE = 205



SUBSTANCES = [
{'Name': 'water',       'Code' : WATER,     'Block_size': 1,  'Spread_speed': 0.9,  'Spread_lapse': 10},
{'Name': 'nitrate',     'Code' : NITRATE,   'Block_size': 2,  'Spread_speed': 0.01, 'Spread_lapse': 200},
{'Name': 'phosphate',   'Code' : PHOSPHATE, 'Block_size': 1,  'Spread_speed': 0.02, 'Spread_lapse': 100}
]    
