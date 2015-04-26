from random import random

import initial_settings
import Tools
import Organism

class Experiment(object):
    # Biotope:
    BIOTOPE_SIZE_X
    BIOTOPE_SIZE_Y
    # Organisms:
    REPRODUCTION_FREQUENCY = 0.1
    GLOBAL_LONGEVITY = 200

    initial_organisms = []

    gui = None