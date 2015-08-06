def _default_value_after_mutation(gene):
    """
        Since this module is common to many genes,
        we define it as an independent function 
    """
    relative_variation = {
        'uniform': [-0.05, 0.05]
    }
    total_variation = {
        '*': (gene, relative_variation)
    }
    new_value = {'+': (gene, total_variation)}
    value_after_mutation =  {
        'if': ({'random true': 'mutation frequency'},
               new_value)}
    return value_after_mutation

biotope = {
    # Mandatory atributes
    'size': (100, 100)
} 

organisms_category_a = {
    # Define initial number of organisms:
    'initial number of organisms': 200,
    'genes': {
        'age': {
            'initial value': 0,
            'value after cycle': {
                '+': ('age', 1)
            },
            'value after mutation': {
                'if': ({'>': ('age', 1000)},
                       0)
            }
        },
        'photosynthesis capacity': {
            'initial value': {
                'uniform': [0, 3000]
            },
            'value after mutation': \
                _default_value_after_mutation('photosynthesis capacity')
        },
        'energy storage capacity': {
            'initial value': {
                'uniform': [0, 20000]
            },
            'value after mutation': \
                _default_value_after_mutation('energy storage capacity')
        },
        'minimum energy reserve for procreating': {
            'initial value': {
                'uniform': [0, 3000]
            }
        },
        'speed': {
            'initial value': {
                'uniform': [0, 4]
            },
            'value after mutation': \
                _default_value_after_mutation('speed')
        },
        'hunt radius': {
            'initial value': 1.1,
            'value after mutation': \
                _default_value_after_mutation('hunt radius')
            }
        'radius of procreation': {
            'initial value': 1.5,
            'value after mutation': \
                _default_value_after_mutation('radius of procreation')
        },
        'attack capacity': {
            'initial value': {
                'uniform': [0, 20]
            },
            'value after mutation': \
                _default_value_after_mutation('attack capacity')
        },
        'defense capacity': {
            'initial value': {
                'uniform': [0, 20]
            },
            'value after mutation': \
                _default_value_after_mutation('defense capacity')
        },
        'aggressiveness': {
            'initial value': {
                'uniform': [0, 1]
            },
            'value after mutation': \
                _default_value_after_mutation('aggressiveness')
        },
        'indicator gene A': {
            'initial value': 1.0,
            'value after mutation': \
                _default_value_after_mutation('indicator gene A')
        }
        'indicator gene B': {
            'initial value': 1.0,
            'value after mutation': \
                _default_value_after_mutation('indicator gene B')
        }
        'energy reserve': {
            'initial value': 10000.0,  # Energy reserve at birth right?
            'value in next cycle': {
                '+': ('energy reserve',
                      'photosynthesis capacity')
            },
            'allowed interval': [0, 'energy storage capacity']
        }
        'mutation frequency': {
            'initial value': {
                'uniform': [0, 1]
            },
            'value after mutation': \
                _default_value_after_mutation('mutation frequency')
        },
        'moving frequency': {
            'initial value': {
                'uniform': [0, 1]
            },
            'value after mutation': \
                _default_value_after_mutation('moving frequency')
        },
        'procreation frequency': {
            'initial value': {
                'uniform': [0, 1]
            }
        },
        'actions sequence': {
            'initial value': ['move',
                              'hunt',
                              'do internal changes',
                              'stay alive',
                              'procreate'],
            'value after mutation': {
                'if': ({'true with probability': 'mutation frequency'},
                       {'shuffle': 'actions sequence'})
            }
        },

    }
}
"""
ecosystem_settings = {
    'biotope': {'size': (100, 100)},
                
    'organisms': {
        'number of organisms': 200,
        'genes': {
            'age': {
                'initial value': 0,
                'variability': {'new value': {'+': ('age', 1)}},
                'mutability': {
                    '&will mutate?': {'>': ('age', 1000)},
                    'new value': 0} },
            'photosynthesis capacity': {'initial value': {'uniform': [0, 3000]}},
            'energy storage capacity': {'initial value': {'uniform': [0, 20000]}},
            'energy reserve procreating threshold': {'initial value': {'uniform': [0, 3000]}},
            'energy reserve at birth': {'initial value': {'uniform': [0, 1000]}},
            'speed': {'initial value': {'uniform': [0, 4]}},
            'hunt radius': {'new value': 1.1},
            'radius of procreation': 1.5,
            'attack capacity': {'initial value': {'uniform': [0, 20]}},
            'defense capacity': {'initial value': {'uniform': [0, 20]}},
            'aggressiveness': {'initial value': {'uniform': [0, 1]}},
            'indicator gene A': 1.0,
            'indicator gene B': 1.0,
            'energy reserve': {
                'initial value': 10000.0,
                'variability': {
                    'new value': {'+': ('energy reserve',
                                        'photosynthesis capacity')},
                    'allowed interval': [0, 'energy storage capacity']
                    }},
            'mutation frequency': {'initial value': {'uniform': [0, 1]}},
            'moving frequency': {'initial value': {'uniform': [0, 1]}},
            'procreating frequency': {'initial value': {'uniform': [0, 1]}},
            '&actions sequence': {
                'initial value': [
                    'move',
                    'hunt',
                    'do internal changes',
                    'stay alive',
                    'procreate'],
                'mutability': {
                    'will change?': {'randbool': 'mutate frequency'},
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
                    'will change?': {'randbool': 'mutation frequency'},
                    'percentage variation': {'uniform': [-0.05, 0.05]},
                    'allowed interval': [0, 'infinity'] }},            
            
            'color': [
                {'comment': 'RED component',
                '+': (
                    20, {
                    'roundint': {
                        '*': (
                            200,
                            {'function': 'sigmoid',
                             'parameter': 'attack capacity',
                             'translation': -5.0,
                             'homothety':  0.5
                    })}})},

                {'comment': 'GREEN component',
                '+': (
                    20, {
                    'roundint': {
                         '*': (
                             200,
                             {'function': 'sigmoid',
                              'parameter': 'photosynthesis capacity',
                              'translation': -5.0,
                              'homothety':  0.005
                    })}})},

                {'comment': 'BLUE component',
                '+': (
                    20, {
                    'roundint': {
                        '*': (
                             200,
                             {'function': 'sigmoid',
                              'parameter': 'mutation frequency',
                              'translation': -3.0,
                              'homothety':  3
                    })}})}]},

        'decisions': {
            'procreate?': {'and': (
                    {'>': ('energy reserve', 'energy reserve procreating threshold')}, 
                    {'randbool': 'procreating frequency'})},
            'move?': {'randbool': 'moving frequency'},
            'hunt?': {'randbool': 'aggressiveness'}
            
                
            }},

     'constraints': {
        'can kill?': {'number of organisms': 2,
                '>': (
                    {'predator': 'attack capacity'}, 
                    {'prey': 'defense capacity'} )},         
        'die?': {'or': (
                {'<': ('energy reserve', 100.0)},
                {'randbool': 0.0005} )},
        'procreate?': {'>': (
                'energy reserve',
                {'+': (
                    'energy reserve at birth',
                    {'outlay': 'procreate'},
                    {'outlay': 'stay alive'}                    
                    )})}},
            
    'outlays': {
        'hunt': {'energy reserve': {
            '+': (
                {'*': (0.2, 'attack capacity', 'defense capacity', 'hunt radius')}, 
                {'*': (0.2, 'speed')},
                0.1)}},         
        'move': {'energy reserve': {
            '+': (
                {'*': ('photosynthesis capacity', 'defense capacity', 0.005)}, 
                {'*': ('speed', 0.8)}, 
                {'*': ('energy reserve', 0.005)},
                {'*': ('energy storage capacity', 0.002)}, 
                0.1)}},
        'procreate': {'energy reserve': {
            '+': (
                'energy reserve at birth',
                {'*': ('attack capacity', 'defense capacity', 8.0)}, 
                {'*': ('photosynthesis capacity', 0.8)}, 
                {'*': ('speed', 'radius of procreation', 10.0)}, 
                200)}},
        'stay alive': {'energy reserve': {
            '+': (
                {'*': ('attack capacity', 0.1)}, 
                {'*': ('attack capacity', 'photosynthesis capacity', 0.003)}, 
                {'*': ('defense capacity', 'photosynthesis capacity', 0.03)}, 
                {'*': ('photosynthesis capacity', 'photosynthesis capacity', 0.0004)},
                {'*': ('energy storage capacity', 0.005)}, 
                {'*': ('energy reserve', 0.05)},
                {'*': ('speed', 0.2)}, 
                100)}}}       
}
"""