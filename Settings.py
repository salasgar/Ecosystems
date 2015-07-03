mutability = {'absolute variation': {'gauss': (0, 0.1)},
              'allowed interval': [0, 100]}



ecosystem_settings_1 = {
    'ecosystem name': "attack, defense, photosynthesis",
    'biotope': { 
        'size': (70, 60),
        'featuremaps': None },
    'organisms': 
        {'number of organisms': 1000,
        'genes': { 
            'attack capacity': {
                'initial value': {'uniform': [0, 50]},
                'mutability': mutability},
            'defense capacity': {
                'initial value': {'uniform': [0, 50]},
                'mutability': mutability},
            'photosynthesis capacity': {'-': (100, {'+': ('attack capacity', 'defense capacity')})},
            'color': ({'roundint': {'*': (2.5, 'attack capacity')}},
                      {'roundint': {'*': (2.5, 'photosynthesis capacity')}},
                      {'roundint': {'*': (2.5, 'defense capacity')}}
                      ),
            'speed': 1.5,
            'hunt radius' : 5.5,
            'radius of procreation': 2.1,
            'procreation frequency': {
                'initial value': {'uniform': (0, 1)},
                'mutability': {
                    'percentage variation': {'gauss': (0, 0.01)},
                    'allowed interval': [0, 1]
                }},
            'energy reserve': {
                'initial value': 1000,
                'variability': {
                    'new value': {'+': ('energy reserve', 'photosynthesis capacity')}
                },
                'allowe interval': [0, 10000]},
            'energy reserve at birth': 100,
            'actions sequence': ['do internal changes', 'stay alive', 'move', 'hunt', 'procreate']}},
            
    'costs':  {
        'stay alive': {'energy reserve': 
            {'+': (
                6,
                {'*': ('attack capacity', 'photosynthesis capacity', 0.00251)},
                {'*': ('defense capacity', 'photosynthesis capacity', 0.005)},
                {'*': ('procreation frequency', 5)} 
            )}},
        'procreate': {'energy reserve': 300}
        },
            
    'constraints': {
        'move?': {'randbool': 0.2},
        'procreate?': {'and': ({'randbool': 'procreation frequency'}, {'>': ('energy reserve', {'*': (3, {'cost': 'procreate'})})})},  
        'can kill?': {
            'number of organisms': 2,
            '>': ({'predator': 'attack capacity'}, {'prey': 'defense capacity'}) },
        'die?': {'or': ({'randbool': 0.005}, {'<': ('energy reserve', 50)})}
                }  }











