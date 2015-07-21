from Basic_tools import *

""" ******************************************************* """
"""                                                         """
"""                     E X A M P L E                       """
"""                                                         """
""" ******************************************************* """



_sunlight = {
    'matrix size': (25, 25),
    'get new value #x #y #time': {
        '+': (
            2,
            {'*': (
                -1, 
                {'cos': {'*': (2, pi, '#y')}}
            )},
            {'sin': {'*': (0.2, '#time')}}
        )}
} 

_temperature = {
    'matrix size': (20, 20),
    'get new value #x #y #time': {
        '*': (
            0.9,
            {'+': (
                {'temperature': ('#x', '#y')},
                {'sunlight': ('#x', '#y')}
            )}
        )}
}
"""
_biotope = {
    'size': (100, 100),
    'feature maps': {
        'sunlight': _sunlight,
        'temperature': _temperature
    }
}
"""
_biotope = {
    'size': (100, 100),
}

def _default_value_after_mutation_A(gene):
    """
        Since this module is common to many genes,
        we define it as an independent function 
    """
    return make_variation(
        gene = gene, 
        relative_variation = {'uniform': [-0.05, 0.05]}, 
        probability_of_change = 'mutation frequency')

def _default_value_after_mutation_B(gene):
    """
        Since this module is common to many genes,
        we define it as an independent function.
        This is an example of the use of 'call function' operator
    """
    def _value(gene_value, mutation_frequency):
        if random_true(mutation_frequency):
            return gene_value * (1 + uniform(-0.5, 0.5)**3)
        else:
            return gene_value
    return {'function': (_value, gene, 'mutation frequency')}

default_value_after_mutation = _default_value_after_mutation_B

# genes
_gene_age_category_a = {
    'help': 
        """ 
            Age of organism (increase +1 every time cycle)
        """, 
    'initial value': 0,
    'value in next cycle': {
        '+': ('age', 1)
    },
    'value after mutation': 0,
    'allowed interval': [0, 'infinity']
}

_organisms_category_a = {
    # Define initial number of organisms:
    'initial number of organisms': 200,
    'genes': {
        'species': {
            'initial value': {'random integer': [0, 9999]},
            'value after mutation': {
                'if': (
                    # Condition:
                    {'random true': 0.00001},
                    # Value if condition == True:
                    {'random integer': [0, 9999]},
                    # Value if condition == False:
                    'species'
                    )
            }
        },
        'age': _gene_age_category_a,
        'generation': {
            'help':
            """
                Indicates the number of direct ancestors the organism has
            """,
            'initial value': 0,
            'value after mutation': {'+': ('generation', 1)}
        },
        'photosynthesis capacity': {
            'help':
            """
                Capacity to transform sunlight into energy reserve
            """,
            'initial value': {
                'uniform': [0, 3000]
            },
            'value after mutation': \
            _default_value_after_mutation_A('photosynthesis capacity'),
            'allowed interval': [0, 'infinity']
        },
        'energy storage capacity': {
            'help':
            """
                Maximum possible energy reserve
            """,
            'initial value': {
                'uniform': [0, 20000]
            },
            'value after mutation': \
            _default_value_after_mutation_B('energy storage capacity')
            ,
            'allowed interval': [0, 'infinity']
        },
        'minimum energy reserve for procreating': {
            'help':
            """
                Minimum energy reserve for procreating
            """,
            'initial value': {
                'uniform': [0, 3000]
            }
        },
        'speed': {
            'help':
            """
                Number of positions that moves every time cycle
            """,
            'initial value': {
                'uniform': [0, 4]
            },
            'value after mutation': \
            make_variation(
                gene = 'speed',
                absolute_variation = {'uniform': [-0.2, 0.2]},
                probability_of_change = 'mutation frequency'
                )
        },
        'hunt radius': {
            'help':
            """
                The radius whitin a prey must be in order to be hunted
            """,
            'initial value': 1.1,
            'value after mutation': \
            _default_value_after_mutation_A('hunt radius')
        },
        'radius of procreation': {
            'initial value': 1.5,
            'value after mutation': \
            _default_value_after_mutation_A('radius of procreation')
        },
        'attack capacity': {
            'initial value': {
                'uniform': [0, 20]
            },
            'value after mutation': \
            make_variation('attack capacity', absolute_variation = {'gauss': (0, 1)})
        },
        'defense capacity': {
            'initial value': {
                'uniform': [0, 20]
            },
            'value after mutation': \
            _default_value_after_mutation_A('defense capacity')
        },
        'mean aggressiveness': {
            'initial value': {
                'uniform': [0, 1]
            },
            'value after mutation': \
            _default_value_after_mutation_A('aggressiveness')
        },        
        'aggressiveness': {
            'initial value': 0,
            'value in next cycle': {
                'gauss': ('mean aggressiveness', 0.1)
            }
        },
        'indicator gene A': {
            'initial value': 1.0,
            'value after mutation': \
            _default_value_after_mutation_A('indicator gene A')
        },
        'indicator gene B': {
            'initial value': 1.0,
            'value after mutation': \
            _default_value_after_mutation_A('indicator gene B')
        },
        'energy reserve at birth': {
            'initial value': 10000.0
        },
        'energy reserve': {
            'initial value': 10000.0,
            'value in next cycle': {
                '+': ('energy reserve',
                      #{'feature': 'sunlight'} 
                      'photosynthesis capacity')
            },
            'allowed interval': [0, 'energy storage capacity']
        },
        'mutation frequency': {
            'initial value': {
                'uniform': [0, 1]
            },
            'value after mutation': \
            _default_value_after_mutation_A('mutation frequency')
        },
        'moving frequency': {
            'initial value': {
                'uniform': [0, 1]
            },
            'value after mutation': \
            _default_value_after_mutation_A('moving frequency')
        },
        'procreation frequency': {
            'initial value': {
                'uniform': [0, 1]
            }
        },
        'actions sequence': {
            'initial value': {
                'literal': [
                    'move',
                    'hunt',
                    'do internal changes',
                    'stay alive',
                    'procreate']},
            'value after mutation': {
                'if': ({'true with probability': 'mutation frequency'},
                       {'shuffle': 'actions sequence'},
                       'actions sequence')
            }
        }

    }
}

_decisions = {
    'decide procreate': {
        'and': ({'>': (
            'energy reserve',
            'minimum energy reserve for procreating')
            },
            {'random true': 'procreation frequency'}
        )
    },
    'decide move': {
        'random true': 'moving frequency'
    },
    'decide hunt': {
        'random true': 'aggressiveness'
    },
    'decide attack #predator #prey': {
        '!=': ('#predator species', '#prey species')
    },
}

_organisms_category_a['decisions'] = _decisions

_constraints = {
    'can kill #predator #prey': {
        '>': (
            '#predator attack capacity',
            '#prey defense capacity'
        ) 
    },
    'can procreate': {
        '>': (
            'energy reserve',
            {'+': (
                'energy reserve at birth',
                {'cost': 'procreate'},
                {'cost': 'stay alive'}
            )}
        )
    },
    'die': {
        'or': (
            {'<': ('energy reserve', 100.0)},
            {'random true': 0.0005}

        )
    }
}

_cost_move = {
    'energy reserve': {
        '+': (
            {'*': (0.2,
                   'attack capacity',
                   'defense capacity',
                   'hunt radius')
            },
            {'*': (0.2, 'speed')},
            0.1
        )
    }
}

_costs = {
    'move': _cost_move,
    'procreate': {'energy reserve': 'energy reserve at birth'},
    'stay alive': {'energy reserve': 100.0}
}

from Basic_tools import *

_organisms_category_b = deep_copy_of_a_dictionary(_organisms_category_a)

_organisms_category_b['genes']['speed'] = {'initial value': 0}

my_example_of_ecosystem_settings = {
    'help': ''' This is an example of ecosystem settings ''',
    'biotope': _biotope,
    'organisms': 
        {
            'category A': _organisms_category_a,
            'category B': _organisms_category_b,
        },
    'constraints': _constraints,
    'costs': _costs
}






""" ******************************************************* """
"""                                                         """
"""                O T H E R    E X A M P L E               """
"""                                                         """
""" ******************************************************* """


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











