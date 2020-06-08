
organisms_types = ['PLANT A', 'PLANT B', 'HERBIVORE', 'CARNIVORE']




_PLANT_A = {'type': 'PLANT A'}
_PLANT_B = {'type': 'PLANT B'}
_HERBIVORE = {'type': 'HERBIVORE'}
_CARNIVORE = {'type': 'CARNIVORE'}

_PLANT_A = {'initial number of organisms': 5000}
_PLANT_B = {'initial number of organisms': 5000}
_HERBIVORE = {'initial number of organisms': 5000}
_CARNIVORE = {'initial number of organisms': 1600}

_PLANT_A = {
    'attributes': {
        'photosynthesis capacity': {
            'initial value': 100,
        },
        'energy reserve': {
            'initial value': 100,
            'value in next cycle': {
                'help':
                """
                    The increasement of the energy reserve depends
                    both on the amount of sunlight
                    and the photosynthesis capacity of the organism.

                    'extract feature' returns certain amount of sunlight
                    and also decreased the
                    available amount of sunlight for other organisms that
                    act after this one.

                    'normalized location' returns the location of the current
                    organisms but in these terms:
                        If the location of the organism is (i, j) and the size
                        of the ecosystem is (size_x, size_y), then:
                            'normalized location x' returns  i / size_x
                            and
                            'normalized location y' returns j / size_y
                """,
                'c++ code': """
                    this->energy_reserve += -10 + 20
                        * (this->parent_biotope_ptr->sun_light
                            ->get_value(floatLocation(this->location)));
                """},
            'value after mutation': 'energy reserve at birth',
            #'allowed interval': [0, 'energy storage capacity'],
        },
        'minimum energy reserve for procreating': {
            'initial value': 300,
            'value after mutation': {
                'c++ code': """

                """
            }

        },
        'energy reserve at birth': {
           'initial value': 100,
        },


    }
}
_PLANT_B = {}
_HERBIVORE = {}
_CARNIVORE = {}


first_example_of_ecosystem_settings = {
    'help':
    '''
        This is an example of ecosystem settings
        to automatically generate C++ code
    ''',
    'biotope': _biotope,
    'organisms':
        {
            'PLANT A': _PLANT_A,
            'PLANT B': _PLANT_B,
            'HERBIVORE': _HERBIVORE,
            'CARNIVORE': _CARNIVORE,
        },
}

_help = {
    
    #etc...

}

initial_values = {
    'generation': 0,
    'photosynthesis capacity': 0.5,
    # etc...
}

value_in_next_clycle = {
    'photosynthesis capacity': {
        '+': (
            'photosynthesis capacity',
            'photosynthesis capacity growth'
        )
    }
}

mutation = {
    'generation': {'+': ('generation', 1)},
    'photosynthesis capacity': 0.5
}


allowed_intervals = {
    
    #etc...
}

       
            'value after mutation': {'+': ('generation', 1)}
        },
        
            'value in next cycle': {
                '+': (
                    'photosynthesis capacity',
                    'photosynthesis capacity growth'
                )
            },
            'value after mutation': 0.5,
            'allowed interval': [0, 'infinity']
        },

