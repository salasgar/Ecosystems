from Ecosystem_main import *
from Ecosystem_definitions import ecosystem_definition


category = {'category': 'Plants',
         'number of organisms': 3,
         'genes': { 
             'strength': 4.0,
             'photosynthesis capacity': { 
                 'initial value': {
                     'type': 'random function',
                     'subtype': 'uniform distribution',
                     'interval': [10, 30] },
                 'mutability': {
                     'absolute variation': {
                         'type': 'random function',
                         'subtype': 'gaussian',
                         'mean': 0.0, 
                         'variance': 0.15},
                     'mutation frequency': 0.001}  },
         },
         'status': {
             'age': 0,
             'energy reserve': 100.0
         }  },


ecosystem_definition = {
    'biotope': {'size': (3, 3)},
    'organisms': category,
    'outlays': {},
    'constraints': {}                
}
    
E = Ecosystem(ecosystem_definition)

print_dictionary( E.organisms_list )



