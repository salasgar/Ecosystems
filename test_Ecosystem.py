from Ecosystem_main import *
from Ecosystem_settings import ecosystem_settings

"""
print " TEST 1 "
basic_category = {'category': 'Plants',
         'number of organisms': 2,
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


basic_ecosystem_settings = {
    'biotope': {'size': (3, 3)},
    'organisms': basic_category,
    'outlays': {},
    'constraints': {}                
}
    
E = Ecosystem(basic_ecosystem_settings)
print_dictionary( E.organisms_list )
"""

print " TEST 2 "
E = Ecosystem(ecosystem_settings)
print_dictionary( E.organisms_list )
