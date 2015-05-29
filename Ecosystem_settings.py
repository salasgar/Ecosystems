                
ecosystem_settings = {
    'biotope': {'size': (70, 70)},
                
    'organisms': {
        'number of organisms': 1000,
        'genes': {
            'age': {
                'initial value': 0,
                'modifying': {'new value': {'+': ('age', 1)}},
                'mutability': {'new value': 0} },
            'photosynthesis capacity': 1000.0,
            'energy storage capacity': 10000.0,
            'energy reserve procreating threshold': 2000.0,
            'energy reserve at birth': 1000.0,
            'speed': 2.5,
            'hunt radius': 1.1,
            'radius of procreation': 1.5,
            'attack capacity': 10.0,
            'defense capacity': 10.0,
            'aggressiveness': 0.8,
            'indicator gene A': 1.0,
            'indicator gene B': 1.0,
            'energy reserve': {
                'initial value': 3000,
                'modifying': {
                    'new value': {'+': ('energy reserve', 'photosynthesis capacity')},
                    'allowed interval': [0, 'energy storage capacity']
                    }},
            'mutation frequency': 0.01,
            'moving frequency': 0.5,
            'procreating frequency': 0.2,
            'actions sequence': {
                'initial value': [
                    'move',
                    'hunt',
                    'interchange substances with the biotope',
                    'interchange substances with other organisms',
                    'fertilize',
                    'do internal changes',
                    'stay alive',
                    'procreate'],
                'mutability': {
                    'will mutate?': {'randbool': 'mutate frequency'},
                    'new value': {'shuffle': 'actions sequence'}                
                    }},
            ('speed',
            'hunt radius',
            'radius of procreation',
            'moving frequency',
            'attack capacity',
            'aggressiveness',
            'defense capacity', 
            'photosynthesis capacity',
            'energy storage capacity',
            'energy reserve procreating threshold',
            'energy reserve at birth',
            'mutation frequency',
            'indicator gene A',
            'indicator gene B'): {
                'mutability': {
                    'will mutate?': {'randbool': 'mutation frequency'},
                    'percentage variation': {'uniform': [-0.01, 0.01]},
                    'allowed interval': [0, 'infinity'] }},            
            
            'color': (
                {'comment': 'RED component',
                '*': (
                    255,
                    {'function': 'sigmoid',
                        'parameter': 'attack capacity',
                        'translation': -50.0,
                        'homothety':  0.2
                    })},

                {'comment': 'GREEN component',
                '*': (
                    255,
                    {'function': 'sigmoid',
                        'parameter': 'photosynthesis capacity',
                        'translation': -1.0,
                        'homothety':  0.01
                    })},

                {'comment': 'BLUE component',
                '*': (
                    255,
                    {'function': 'sigmoid',
                        'parameter': 'mutation frequency',
                        'translation': -5.0,
                        'homothety':  3
                    })})},

        'decisions': {
            'procreate?': {'and': (
                    {'>': ('energy reserve', 'energy reserve procreating threshold')}, 
                    {'randbool': 'procreating frequency'})},
            'move?': {'randbool': 'moving frequency'},
            'hunt?': {'randbool': 'aggressiveness'},
            'attack?': {'>': (
                {'built-in function': 'consanguinity degree'},
                'consanguinity threshold')},
            'fertilize?': {'in': (
                {'built-in function': 'consanguinity degree'},
                range(10, 100)                                
                )}
            }},

     'constraints': {
        'can kill?': {'>': (
                {'*': ({'predator': 'attack capacity'}, {'function': 'gaussian'})},
                {'*': ({'prey': 'defense capacity'}, {'function': 'gaussian'})} )},         
        'die?': {'or': (
                {'<': ('energy reserve', 50.0)},
                {'randbool': 0.001} )} },
            
    'outlays': {
        'hunt': {'energy reserve': {
            '+': (
                {'*': (0.3, 'attack capacity')}, 
                {'*': (0.2, 'speed')},
                0.1)}},         
        'move': {'energy reserve': {
            '+': (
                {'*': ('photosynthesis capacity', 0.005)}, 
                {'*': ('speed', 0.08)}, 
                {'*': ('energy reserve', 0.005)},
                {'*': ('energy storage capacity', 0.002)}, 
                0.1)}},
        'procreate': {'energy reserve': {
            '+': (
                {'*': ('attack capacity', 0.8)}, 
                {'*': ('photosynthesis capacity', 0.3)}, 
                {'*': ('speed', 0.1)}, 
                0.05)}},
        'stay alive': {'energy reserve': {
            '+': (
                {'*': ('attack capacity', 0.3)}, 
                {'*': ('photosynthesis capacity', 'photosynthesis capacity', 0.0008)},
                {'*': ('energy storage capacity', 0.002)}, 
                {'*': ('energy reserve', 0.05)},
                {'*': ('speed', 0.2)}, 
                0.1)}}}       
}

"""
from Tools import *              
print_dictionary(ecosystem_settings)
"""