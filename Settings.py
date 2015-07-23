from Basic_tools import *

""" ******************************************************* """
"""                                                         """
"""                     E X A M P L E                       """
"""                                                         """
""" ******************************************************* """



_sunlight = {
    'matrix size': (25, 25),
    # No matters the size of the ecosystem (it might be changed later for further experiments), 
    # we will store 25x25 = 625 values of sunlight in any giving moment. Each value correspond
    # to a rectangular region of the ecosystem. If the size of the ecosystem is 200x100, then
    # the size of each region must be 8x4. 

    'initial value #x y#': {'+': (1.0, '#x', '#y')},
    # No matters the size of the ecosystem nor the size of the matrix of sunlight values, the
    # function that gives the value of each point is defined in the square [0, 1] x [0, 1],
    # i.e. the function initial_value(x, y) of any substance is defined for 0 <= x <= 1 and
    # 0 <= y <= 1
    # This way, we can change the number of values we store without having to change any function
    # definition.
    
    'value after updating #x #y #time': {
    # Each time the substance evolves, the whole matrix change its values, calling this 
    # function. But this function is defined for 0 <= x <= 1 and 0 <= y <= 1. Thus, for each
    # entry (i, j) of the matrix, we call this function with x = i / size_x   and   y = j /size_y
    # where (size_x, size_y) is the size of the matrix of this substance. #time is the number
    # of cycles since the experiment started.
        'help':
        """
            Sunlight leads the climate, providing food for autotrophs and powering the 
            rise of temperatures.
            This feature varies from 0 to 4. In the poles is much lower than in the equator.
            But globally varies from winter to summer. Winters occur in the north and in the
            south at the same time (as summers do), because both poles are the same place.
        """
        '+': (
            2,
            {'*': (
                -1, 
                {'cos': {'*': (2, pi, '#y')}}
            )},
            {'sin': {'*': ('seasons speed', '#time')}}
        )},

    'update once every': 1 # The values of the matrix of sunlight is updated every 1 cycle.
} 

_temperature = {
    'matrix size': (20, 20),
    'initial value #x y#': 10.0,
    'value after updating #x #y #time': {
        'help':
        """
            Each cycle the temperature is increased by sunlight, but the 10 per cent of
            the accumulated heat is lost in every cycle.
        """
        '*': (
            0.9, # this is the percentage (90 per cent) of the heat that remains in the biotope
            {'+': (
                {'feature value': ('temperature', '#x', '#y')}, # the new value depends on the previous value
                {'feature value': ('sunlight', '#x', '#y')}
            )}
        )},
    'update once every': 1 # The values of the matrix of sunlight is updated every 1 cycle.
}

_biotope = {
    'size': (200, 100),
    'biotope features': {
        'sunlight': _sunlight,
        'temperature': _temperature,
        'seasons speed': {
            'initial value': 0.2,
            'value after updating': {
                '+': (
                    {'feature value': 'seasons speed'},
                    {'uniform': [-0.05, 0.05]}
                )
            },
            'update once every': 100
        }
    }
}

def _default_value_after_mutation_A(gene):
    """
        Since this module is common to many genes,
        we define it as an independent function 
    """
    return make_variation(
        gene = gene, 
        relative_variation = {'uniform': [-0.05, 0.05]}, 
        # "relative variation" means that the gene will be increased or decreased proportionally 
        # to its current value. For example: relative_variation = -0.034 means that the gene will 
        # lose the 3.4 per cent of its value
        probability_of_change = 'mutation frequency')

def _default_value_after_mutation_B(gene):
    """
        Since this module is common to many genes,
        we define it as an independent function 
    """
    return make_variation(
        gene = gene, 
        absolute_variation = {'uniform': [-0.05, 0.05]}, 
        # Example: if absolute_variation = -0.034 means that the gene will be 0.034 units less
        # than before
        probability_of_change = 'mutation frequency')

def _default_value_after_mutation_C(gene):
    """
        Since this module is common to many genes,
        we define it as an independent function.
        This is an example of the use of 'function' operator
    """

    def _value(gene_value, mutation_frequency):
        if random_true(mutation_frequency):
            # This is the random function of a 'cubic' distribution of probability:
            return gene_value * (1 + uniform(-0.5, 0.5)**3)
        else:
            return gene_value

    # This means that the function _value will be called and two parameters will be passed
    # to it: The values of gene and 'mutation frequency'
    return {'function': (_value, gene, 'mutation frequency')}

_ecosystem_features = {
    'autotrophs productivity': {
        'initial value': 10000.0  
    # Each organism has a different photosynthesis capacity, but this capacity is multiplied
    # by the value of 'autotrophs productivity', that is a variable of the experiment the
    # user can change at any time.
}


# genes:

_gene_energy_reserve = {
            # This is the definition of the gene 'energy reserve'
            'initial value': 10000.0,
            'value in next cycle': {
                'help': 
                """
                    The increasement of the energy reserve depends both on the amount of sunlight
                    and the photosynthesis capacity of the organism.

                    'extract feature' returns certain amount of sunlight and also decreased the 
                    available amount of sunlight for other organisms that act after this one.

                    'normalized location' returns the location of the current organisms but
                    in these terms:
                        If the location of the organism is (i, j) and the size of the ecosystem 
                        is (size_x, size_y), then:
                            'normalized location x' returns  i / size_x
                            and
                            'normalized location y' returns j / size_y
                """
                '+': (
                    'energy reserve',
                    {'*': (
                        {'feature value': 'autotrophs productivity'},
                        {'extract feature (percentage)': (
                            '@sunlight',
                            'normalized location x',
                            'normalized location y',
                            {'+': (
                                -1,
                                {'*': (
                                    2,
                                    {'sigmoid': 'photosynthesis capacity'}
                                )}
                            )}
                        )}                       
                    )}
                )},
            'value after mutation': 'energy reserve at birth',
            'allowed interval': [0, 'energy storage capacity']
        }
        
_gene_optimal_temperature = {
            # This is the definition of the gene 'optimal temperature'
            'help':
            """
                All organisms have a probability of dying at any given moment. But every 
                organism will have an optimal environmental temperature that minimizes that 
                probability.
            """
            'initial value': {
                'uniform': [0, 40]
            },
            'value after mutation': \
            _default_value_after_mutation_B('optimal temperature')
        }

_gene_temperature_adaptation_level = {
            # This is the definition of the gene 'temperature adaptation level'
            'help':
            """
                Each organism have a different tolerance to too high or too low temperatures.
                If the gene 'temperature adaptation level' has a high value, then the organism
                may survive in a wider range of temperatures than otherwise.
            """
            'initial value': {
                'uniform': [0, 2]
            },
            'value after mutation': \
            _default_value_after_mutation_C('temperature adaptation level')
        }
}

_constraint_die = {
        # This is the definition of the constraint 'die'
        'help':
        """
            If an organism isn't killed by a predator, it has 3 different ways of dying:
                - BY CHANCE: It can be an illness or an accident. Every organism has a 
                        chance of 0.05 percent of dying because of this reason.
                - BY STARVATION: If the energy reserve of an organism is less than 1000 units, 
                        it dies.
                - BY HEAT OR COLD: If the temperature of the environment is very different 
                        from the 'optimal temperature' of the organism, it has a high 
                        probability of dying. But if the organism has a high
                        'temperature adaptation level', it will lower that probability.
                - BY OLD AGE: As an organism get old it increases its chance of dying.
        """
        'or': (
            # RANDOM CAUSE OF DETH:
            {'random true': 0.0005},
            # DEATH BY STARVATION:
            {'<': ('energy reserve', 1000.0)},
            # DEATH BY TEMPERATURE:
            {'>': (
                {'gauss': (
                    {'/': (
                        {'**': (
                            {'-': (
                                'optimal temperature',
                                {'feature value': ('@temperature', 'normalized location x', 'normalized location y') }
                            )},
                            2
                        )},
                        'temperature adaptation level'
                    )},
                    0.1
                )},
                {'chi-squared': 2}
            )},
            # DEATH BY OLD AGE:
            {'>': (
                {'gauss': ('age', 'age')},
                '$longevity'
                )}
        )
    }

_organisms_category_a = {
    # Define initial number of organisms:
    'initial number of organisms': 200,
    'genes': {
        'species': {
            # An organism will never attack any other organism of the same species. It only
            # attacks organisms of other species.
            'initial value': {'random integer': [0, 9999]},
            'value after mutation': {
                'if': (
                    # Condition:
                    {'random true': 'species identity mutation frequency'},
                    # Value if condition == True:
                    {'random integer': [0, 9999]},
                    # Value if condition == False:
                    'species'
                    )
            }
        },
        'species identity mutation frequency': {
            'initial value': 0.01,
            'value after mutation': \
            _default_value_after_mutation_A('species identity mutation frequency'),
            'allowed interval': [0, 1]
        },
        'age': {
            'help': 
            """ 
                Age of organism (increase +1 every time cycle).
            """, 
            'initial value': 0,
            'value in next cycle': {
                '+': ('age', 1)
            },
            'value after mutation': 0,
            'allowed interval': [0, 'infinity']
        },
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
            'initial value': 0.0,
            'value in next cycle': {
                '+': (
                    'photosynthesis capacity',
                    'photosynthesis capacity growth'
                    )
            },
            'value after mutation': 0.0,
            'allowed interval': [0, 'infinity']
        },
        'photosynthesis capacity growth': {
            'initial value': {
                'uniform': [0, 0.2]
            },
            'value after mutation': {
                'triangular': (
                    {'*': (0.9, 'photosynthesis capacity growth')},
                    {'*': (1.1, 'photosynthesis capacity growth')},
                    'photosynthesis capacity growth'
                    )
            }
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
                '+': (
                    'energy reserve',
                    {'*': (
                        10000.0,
                        {'extract feature': (
                            '#f sunlight',
                            'percentage',
                            {'+': (
                                -1,
                                {'*': (
                                    2,
                                    {'sigmoid': 'photosynthesis capacity'}
                                )}
                            )}
                        )}                       
                    )}
                )},
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
        'optimal temperature': {
            'initial value': {
                'uniform': [0, 40]
            },
            'value after mutation': \
            _default_value_after_mutation_B('optimal temperature')
        },
        'temperature adaptation level': {
            'initial value': {
                'uniform': [0, 2]
            },
            'value after mutation': \
            _default_value_after_mutation_B('temperature adaptation level')
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
            {'>': (
                {'gauss': (
                    {'/': (
                        {'**': (
                            {'-': (
                                'optimal temperature',
                                '#f temperature'
                            )},
                            2
                        )},
                        'temperature adaptation level'
                    )},
                    0.1
                )},
                {'chi-squared': 2}
            )},
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
            {'*': (2, 'speed')},
            {'*': (10.0, 'photosynthesis capacity')},
            0.1
        )
    }
}

_costs = {
    'move': _cost_move,
    'procreate': {
        'energy reserve': {'+': (
            1000,
            'energy reserve at birth'
        )}
    },
    'stay alive': {
        'energy reserve': {'+': (
            100.0,
            {'*': (50.0, 'temperature adaptation level')},
            {'*': (500.0, 'photosynthesis capacity growth')},
            {'*': (5.0, 'photosynthesis capacity')},
            {'*': (1.0, 'indicator gene A')},
            {'*': (1.0, 'defense capacity')},
            {'*': (1.0, 'attack capacity')},
            {'*': (10.0, 'speed')},
            {'*': (50.0, 'hunt radius')},
            {'*': (0.002, 'energy storage capacity')},
            {'*': (500.0, 'procreation frequency')},
            {'*': (50.0, 'radius of procreation')},
            {'*': (50.0, 'mutation frequency')}
        )}
    }
}

from Basic_tools import *

_organisms_category_b = deep_copy_of_a_dictionary(_organisms_category_a)

_organisms_category_b['genes']['speed'] = {'initial value': 0}

my_example_of_ecosystem_settings = {
    'help': ''' This is an example of ecosystem settings ''',
    'biotope': _biotope,
    'ecosystem features': _ecosystem_features,
    'organisms': 
        {
            'category A': _organisms_category_a,
            'category B': _organisms_category_b,
        },
    'constraints': _constraints,
    'costs': _costs
}






