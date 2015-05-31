# EXPERIMENT 1. STONE, PAPER, SCISSORS

# Ecosystem 1:
# Goal: Adjust 'speed', 'hunt radius' and 'radius of procreation'
#       to get a stable ecosystem, in which the 3 species survive
ecosystem_settings_1 = {
    'ecosystem name': "Strength vs photosyntesis capacity",
    'biotope': { 
        'size': (70, 70),
        'featuremaps': None },
    'organisms': 
        {'number of organisms': 500,
        'genes': { 
            'weapon': {
                'initial value': {            
                    'function': 'discrete distribution',
                    'values list': (
                        {'value': 'stone', 'probability': 1.0/3},                            
                        {'value': 'paper', 'probability': 1.0/3},                            
                        {'value': 'scissors', 'probability': 1.0/3})}
                    },
            'color': {
                'choice': 'weapon',
                'stone': {'literal': (150, 20, 10)}, # brown
                'paper': {'literal': (200, 200, 200)}, # dark white
                'scissors': {'literal': (100, 100, 200)} }, # pale blue
            'procreating frequency': 0.1,
            'speed': 1.1,
            'hunt radius' : 1.1,
            'radius of procreation': 4.1,
            'actions list': ('move', 'hunt', 'procreate')}},
    'constraints': {
        'procreate?': {'<': (
                    {'uniform': [0, 1]}, 
                    'procreating frequency')},  
        'can kill?': {
            'number of organisms': 2,
            'in': (
                {'tuple': ({'predator': 'weapon'}, {'prey': 'weapon'})},
                {'literal': (
                    ('stone', 'scissors'),
                    ('scissors', 'paper'),
                    ('paper', 'stone') )})},
        'die?': {'randbool': 0.05}
                }  }

# Ecosystem 2:
# Goal: Evaluate the optimal speed for a species to survive in this ecosystem.
#       The optimal speed (if it exist) will be determined by natural selection
ecosystem_settings_2 = {
    'ecosystem name': "Strength vs photosyntesis capacity",
    'biotope': { 
        'size': (70, 70),
        'featuremaps': None },
    'organisms': 
        {'number of organisms': 500,
        'genes': { 
            'weapon': {
                'initial value': {            
                    'function': 'discrete distribution',
                    'values list': (
                        {'value': 'stone', 'probability': 1.0/3},                            
                        {'value': 'paper', 'probability': 1.0/3},                            
                        {'value': 'scissors', 'probability': 1.0/3})}
                    },
            'color': {
                'choice': 'weapon',
                'stone': {'literal': (150, 20, 10)}, # brown
                'paper': {'literal': (200, 200, 200)}, # dark white
                'scissors': {'literal': (100, 100, 200)} }, # pale blue
            'procreating frequency': 0.1,
            'speed': {
                'initial value': 0.8,
                'mutability': {
                    'will mutate?': {'function': 'random boolean', 'probability': 0.1},
                    'percentage variation': {'gauss': (0, 0.08)}
                    }
                },
            'hunt radius' : 1.1,
            'radius of procreation': 4.1,
            'actions list': ('move', 'hunt', 'procreate')}},
    'constraints': {
        'procreate?': {'<': (
                    {'function': 'uniform distribution', 'interval': [0, 1]}, 
                    'procreating frequency')},  
        'can kill?': {
            'number of organisms': 2,
            'in': (
                {'tuple': ({'predator': 'weapon'}, {'prey': 'weapon'})},
                {'literal': (
                    ('stone', 'scissors'),
                    ('scissors', 'paper'),
                    ('paper', 'stone') )})},
        'die?': {'function': 'random boolean', 'probability': 0.05}
                }  }

# Ecosystem 3:
# Goal: Determine by natural selection weather mutating is good for survival or not. 
ecosystem_settings_3 = {
    'ecosystem name': "Strength vs photosyntesis capacity",
    'biotope': { 
        'size': (70, 70),
        'featuremaps': None },
    'organisms': 
        {'number of organisms': 500,
        'genes': { 
            'weapon': {
                'initial value': {            
                    'function': 'discrete distribution',
                    'values list': (
                        {'value': 'stone', 'probability': 1.0/3},                            
                        {'value': 'paper', 'probability': 1.0/3},                            
                        {'value': 'scissors', 'probability': 1.0/3})},
                'mutability': {
                    'new value': {
                        'choice': 'weapon',
                        'stone': {
                            'function': 'discrete distribution',
                            'values list': (
                                {'value': 'stone', 'probability': 'remain stone probability'},                            
                                {'value': 'paper', 'probability': 'stone to paper probability'},                            
                                {'value': 'scissors', 'probability': 'stone to scissors probability'})},
                        'paper': {
                            'function': 'discrete distribution',
                            'values list': (
                                {'value': 'stone', 'probability': 'paper to stone probability'},                            
                                {'value': 'paper', 'probability': 'remain paper probability'},                            
                                {'value': 'scissors', 'probability': 'paper to scissors probability'})},
                        'scissors': {
                            'function': 'discrete distribution',
                            'values list': (
                                {'value': 'stone', 'probability': 'scissors to stone probability'},                            
                                {'value': 'paper', 'probability': 'scissors to paper probability'},                            
                                {'value': 'scissors', 'probability': 'remain scissors probability'})} }}},                         
            'stone to paper probability': {
                'initial value': 0.01,
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}}},
            'paper to scissors probability': {
                'initial value': 0.01,
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}}},
            'scissors to stone probability': {
                'initial value': 0.01,
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}}},
            'stone to scissors probability': {
                'initial value': 0.01,
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}}},
            'scissors to paper probability': {
                'initial value': 0.01,
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}}},
            'paper to stone probability': {
                'initial value': 0.01,
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}}},
            'remain stone probability': {
                'initial value': 0.98,
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}}},
            'remain paper probability': {
                'initial value': 0.98,
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}}},
            'remain scissors probability': {
                'initial value': 0.98,
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}}},
            'color': {
                'choice': 'weapon',
                'stone': {'literal': (150, 20, 10)}, # brown
                'paper': {'literal': (200, 200, 200)}, # dark white
                'scissors': {'literal': (100, 100, 200)} }, # pale blue
            'procreating frequency': 0.1,
            'speed': {
                'initial value': 0.8,
                'mutability': {
                    'will mutate?': {'function': 'random boolean', 'probability': 0.1},
                    'percentage variation': {'gauss': (0, 0.08)}
                    }
                },
            'hunt radius' : 1.1,
            'radius of procreation': 4.1,
            'actions list': ('move', 'hunt', 'procreate')}},
    'constraints': {
        'procreate?': {'<': (
                    {'function': 'uniform distribution', 'interval': [0, 1]}, 
                    'procreating frequency')},  
        'can kill?': {
            'number of organisms': 2,
            'in': (
                {'tuple': ({'predator': 'weapon'}, {'prey': 'weapon'})},
                {'literal': (
                    ('stone', 'scissors'),
                    ('scissors', 'paper'),
                    ('paper', 'stone') )})},
        'die?': {'function': 'random boolean', 'probability': 0.05}
                }  }

# Ecosystem 4:
# Goal: A simple color variation of the previous ecosystem to improve the observations
ecosystem_settings_4 = {
    'ecosystem name': "Strength vs photosyntesis capacity",
    'biotope': { 
        'size': (70, 70),
        'featuremaps': None },
    'organisms': 
        {'number of organisms': 500,
        'genes': { 
            'weapon': {
                'initial value': {            
                    'function': 'discrete distribution',
                    'values list': (
                        {'value': 'stone', 'probability': 1.0/3},                            
                        {'value': 'paper', 'probability': 1.0/3},                            
                        {'value': 'scissors', 'probability': 1.0/3})},
                'mutability': {
                    'new value': {
                        'choice': 'weapon',
                        'stone': {
                            'function': 'discrete distribution',
                            'values list': (
                                {'value': 'stone', 'probability': 'remain stone probability'},                            
                                {'value': 'paper', 'probability': 'stone to paper probability'},                            
                                {'value': 'scissors', 'probability': 'stone to scissors probability'})},
                        'paper': {
                            'function': 'discrete distribution',
                            'values list': (
                                {'value': 'stone', 'probability': 'paper to stone probability'},                            
                                {'value': 'paper', 'probability': 'remain paper probability'},                            
                                {'value': 'scissors', 'probability': 'paper to scissors probability'})},
                        'scissors': {
                            'function': 'discrete distribution',
                            'values list': (
                                {'value': 'stone', 'probability': 'scissors to stone probability'},                            
                                {'value': 'paper', 'probability': 'scissors to paper probability'},                            
                                {'value': 'scissors', 'probability': 'remain scissors probability'})} }}},                         
            'stone to paper probability': {
                'initial value': {'uniform': [0, 1]},
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}, 'allowed interval': [0, 1]}},
            'paper to scissors probability': {
                'initial value': {'uniform': [0, 1]},
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}, 'allowed interval': [0, 1]}},
            'scissors to stone probability': {
                'initial value': {'uniform': [0, 1]},
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}, 'allowed interval': [0, 1]}},
            'stone to scissors probability': {
                'initial value': {'uniform': [0, 1]},
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}, 'allowed interval': [0, 1]}},
            'scissors to paper probability': {
                'initial value': {'uniform': [0, 1]},
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}, 'allowed interval': [0, 1]}},
            'paper to stone probability': {
                'initial value': {'uniform': [0, 1]},
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}, 'allowed interval': [0, 1]}},
            'remain stone probability': {
                'initial value': {'uniform': [0, 1]},
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}, 'allowed interval': [0, 1]}},
            'remain paper probability': {
                'initial value': {'uniform': [0, 1]},
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}, 'allowed interval': [0, 1]}},
            'remain scissors probability': {
                'initial value': {'uniform': [0, 1]},
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}, 'allowed interval': [0, 1]}},
            'color': {
                'choice': 'weapon',
                'stone': {'tuple': (
                    {'+': (20, {'*': (200, 'stone to paper probability')})}, 
                    {'+': (20, {'*': (200, 'stone to scissors probability')})}, 
                    {'+': (20, {'*': (200, 'remain stone probability')})})}, 
                'paper': {'tuple': (
                    {'+': (20, {'*': (200, 'paper to scissors probability')})}, 
                    {'+': (20, {'*': (200, 'paper to stone probability')})}, 
                    {'+': (20, {'*': (200, 'remain paper probability')})})}, 
                'scissors': {'tuple': (
                    {'+': (20, {'*': (200, 'scissors to stone probability')})}, 
                    {'+': (20, {'*': (200, 'scissors to paper probability')})}, 
                    {'+': (20, {'*': (200, 'remain scissors probability')})})}},
            'procreating frequency': 0.1,
            'speed': {
                'initial value': {'uniform': [0, 10]},
                'mutability': {
                    'will mutate?': {'function': 'random boolean', 'probability': 0.1},
                    'percentage variation': {'gauss': (0, 0.08)},
                    'allowed interval': [0, 10]
                    }
                },
            'hunt radius' : 1.1,
            'radius of procreation': 4.1,
            'actions list': ('move', 'hunt', 'procreate')}},
    'constraints': {
        'procreate?': {'<': (
                    {'function': 'uniform distribution', 'interval': [0, 1]}, 
                    'procreating frequency')},  
        'can kill?': {
            'number of organisms': 2,
            'in': (
                {'tuple': ({'predator': 'weapon'}, {'prey': 'weapon'})},
                {'literal': (
                    ('stone', 'scissors'),
                    ('scissors', 'paper'),
                    ('paper', 'stone') )})},
        'die?': {'function': 'random boolean', 'probability': 0.05}
                }  }


