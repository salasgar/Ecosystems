from Ecosystem_main import *
from Ecosystem_settings import ecosystem_settings

test1 = False
test2 = False
test3 = True

if test1:
    print " TEST 1 "
    basic_category = {'category': 'Plants',
         'number of organisms': 2,
         'genes': { 
             'strength': 4.0,
             'photosynthesis capacity': { 
                 'initial value': {
                     'function': 'uniform distribution',
                     'interval': [10, 30] },
                 'mutability': {
                     'absolute variation': {
                         'function': 'gaussian',
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
        'constraints': {} }
  
    E = Ecosystem(basic_ecosystem_settings)
    print_dictionary(E.settings)
    print_dictionary( E.organisms_list )

if test2:
    print " TEST 2 "
    E = Ecosystem(ecosystem_settings)
    #print_dictionary(E.settings)
    for i in range(40):    
        print "\n",
        E.biotope.print_matrix()
        for organism in E.organisms_list:
            organism.act()
        E.organisms_list += E.newborns
        E.newborns = []
    print_dictionary( E.organisms_list )
  
if test3:
    print " TEST 3"
    E = Ecosystem(ecosystem_settings)
    prey = E.organisms_list[0]
    predator = E.organisms_list[2]
    print "\nPREDATOR:", predator
    print "\nPREY:", prey
    print predator['attack capacity'](predator)
    print prey['defense capacity']
    print E.constraints['hunting'](predator, prey)
 