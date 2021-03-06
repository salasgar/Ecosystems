from Basic_tools import *

""" ******************************************************* """
"""                                                         """
"""                     E X A M P L E                       """
"""                                                         """
""" ******************************************************* """



Store_data = False

Elements_to_store = {

    """
        In this dictionary we indicate what and how often to store:

            'Once'  means that this data is stored only once at the begining of the file
            200     means that this data is stored once every 200 cycles
            None    means that this data is never stored

    """

    'genes': {
        'nutrient B reserve at birth': None,
        'photosynthesis capacity growth': None,
        'nutrient B storage capacity': None,
        'generation': 200,
        'energy reserve': 100,
        'nutrient A reserve': None,
        'temperature adaptation level': 40,
        'aggressiveness': 20,
        'indicator gene B': 1000,
        'indicator gene A': 1000,
        'moving frequency': None,
        'photosynthesis capacity': None,
        'defense capacity': None,
        'minimum energy reserve for procreating': None,
        'speed': None,
        'minimum nutrient B reserve for procreating': None,
        'species': None,
        'actions sequence': None,
        'nutrient B reserve': None,
        'energy reserve at birth': None,
        'hunt radius': None,
        'optimal temperature': None,
        'nutrient A reserve at birth': None,
        'energy storage capacity': None,
        'attack capacity': None,
        'mean aggressiveness': None,
        'procreation frequency': None,
        'species identity mutation frequency': None,
        'basal defense capacity': None,
        'age': 20,
        'minimum nutrient A reserve for procreating': None,
        'nutrient A storage capacity': None,
        'radius of procreation': None,
        'mutation frequency': None
    },
    'biotope': {
        'biotope features': {
            'nutrient B': 'Once',
            'nutrient A': 'Once',
            'sunlight': 'Once',
            'temperature': 'Once',
            'seasons speed': 'Once'
            },
        'size': 'Once'
        },
    'ecosystem features': {
        'maximum population allowed': 100,
        'time': 20,
        'autotrophs productivity': 'Once',
        'population': 20
        }
    }

def my_operator(a, b):
    return gauss(
        (a+b)/2,
        abs(a-b)/5
        )

# User-defined operators:

_operator_definitions = {
    'my operator': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) == 2),    
        'output function': my_operator
    },

    'curve from 0 to 1': {
        'type of inputs': 'Number',
        'type of outputs': 'Number',        
        'output function #input': {'+': (
            -1,
            {'*': (
                2,
                {'sigmoid': '#input'}
            )}
        )}
    },

    'gauss variation': {
        'output function #value': {
            'gauss': (
                '#value',
                {'/': ('#value', 4)}
            )}
    },

    'variate': {
        'output function #value #probability_of_change': {
            'if': (
                {'random true': '#probability_of_change'},
                {'gauss variation': '#value'},
                '#value'
            )}
    }
}

_sunlight = {
    'matrix size': (25, 25),
    # No matters the size of the ecosystem (it might be changed later for further experiments), 
    # we will store 25x25 = 625 values of sunlight in any giving moment. Each value correspond
    # to a rectangular region of the ecosystem. If the size of the ecosystem is 200x100, then
    # the size of each region must be 8x4. 

    'initial value #x #y': {'+': (10.0, '#x', '#y')},
    # No matters the size of the ecosystem nor the size of the matrix of sunlight values, the
    # function that gives the value of each point is defined in the square [0, 1] x [0, 1],
    # i.e. the function initial_value(x, y) of any substance is defined for 0 <= x <= 1 and
    # 0 <= y <= 1
    # This way, we can change the number of values we store without having to change any function
    # definition.
    
    'value after updating #x #y': {
    # Each time the substance evolves, the whole matrix change its values, calling this 
    # function. But this function is defined for 0 <= x <= 1 and 0 <= y <= 1. Thus, for each
    # entry (i, j) of the matrix, we call this function with x = i / size_x   and   y = j /size_y
    # where (size_x, size_y) is the size of the matrix of this substance. 'time' is the number
    # of cycles since the experiment started.
        'help':
        """
            Sunlight leads the climate, providing food for autotrophs and powering the 
            rise of temperatures.
            This feature varies from 0 to 4. In the poles is much lower than in the equator.
            But globally varies from winter to summer. Winters occur in the north and in the
            south at the same time (as summers do), because both poles are the same place.
        """,
        '+': (
            10,
            {'*': (
                -1, 
                {'cos': {'*': (2, pi, '#y')}}
            )},
            {'sin': {'*': ('seasons speed', 'time')}}
        )},

    'update once every': 1 # The values of the matrix of sunlight is updated every 1 cycle.
} 

_temperature = {
    'matrix size': (20, 20),
    'initial value #x #y': 10.0,
    'value after updating #x #y': {
        'help':
        """
            Each cycle the temperature is increased by sunlight, but the 10 per cent of
            the accumulated heat is lost in every cycle.
        """,
        '*': (
            0.9, # this is the percentage (90 per cent) of the heat that remains in the biotope
            {'+': (
                {'#biotope temperature': ('#x', '#y')}, # the new value depends on the previous value
                {'#biotope sunlight': ('#x', '#y')}
            )}
        )},
    'update once every': 1 # The values of the matrix of sunlight is updated every 1 cycle.
}

_nutrient_A = {
    'matrix size': (50, 50),
    'initial value #x #y': {
        'if': (
            {'random true': 0.03},
            {'uniform': [0, 10000]},
            {'*': (2000.5, '#x', '#y')}
        )},
    'value after updating #x #y': {
        '+': (
            # Generating:
            500,
            # Spreading:
            {'*': (
                0.80,  # the location (#x, #y) keeps the 80 per cent of its amount of nutrient A
                {'#biotope nutrient A': ('#x', '#y')}
            )},
            {'*': (
                0.05,  # the location (#x, #y) gets the 5 per cent from each of the adjacent locations:
                {'+': (
                    {'#biotope nutrient A': ( 
                        {'+': ('#x', 1)},
                        '#y'
                    )},
                    {'#biotope nutrient A': ( 
                        {'-': ('#x', 1)},
                        '#y'
                    )},
                    {'#biotope nutrient A': ( 
                        '#x',
                        {'+': ('#y', 1)},
                    )},
                    {'#biotope nutrient A': ( 
                        '#x',
                        {'-': ('#y', 1)}
                    )}
                )}
            )}
        )},
    'update once every': 2 # The values of the matrix of nutrient A is updated once every 20 cycles.
}

_nutrient_B = {
    'matrix size': (50, 50),
    'initial value #x #y': {
        'if': (
            {'random true': 0.04},
            {'uniform': [0, 2000]},
            {'+': (
                1000.0,
                {'-': ('#x', '#y')}
            )}
        )},
    'value after updating #x #y': {
        '+': (
            # Generating:
            7.5,
            # Spreading:
            {'*': (
                0.90,  # the location (#x, #y) keeps the 90 per cent of its amount of nutrient B
                {'#biotope nutrient A': ('#x', '#y')}
            )},
            {'*': (
                0.025,  # the location (#x, #y) gets the 2,5 per cent from each of the adjacent locations:
                {'+': (
                    {'#biotope nutrient A': ( 
                        {'+': ('#x', 1)},
                        '#y'
                    )},
                    {'#biotope nutrient A': ( 
                        {'-': ('#x', 1)},
                        '#y'
                    )},
                    {'#biotope nutrient A': ( 
                        '#x',
                        {'+': ('#y', 1)},
                    )},
                    {'#biotope nutrient A': ( 
                        '#x',
                        {'-': ('#y', 1)}
                    )}
                )}
            )}
        )},
    'update once every': 5 # The values of the matrix of nutrient B is updated once every 15 cycles.
}

_biotope = {
    'size': (200, 100),
    'biotope features': {
        'sunlight': _sunlight,
        'temperature': _temperature,
        'nutrient A': _nutrient_A,
        'nutrient B': _nutrient_B,
        'seasons speed': {
            'initial value': 0.237,
            'value after updating': {
                '+': (
                    'seasons speed',
                    {'uniform': [-0.05, 0.05]}
                )
            },
            'allowed interval': [0, 'infinity'],
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

    'population': {
        'initial value': lambda ecosystem: (
                    len(ecosystem.organisms_list) +
                    len(ecosystem.newborns)
                    ),
        
        'value after updating': lambda ecosystem: (
            len(ecosystem.organisms_list) +
            len(ecosystem.newborns)
            )
    },

    'maximum population allowed': {
        'initial value': 5000,

        '+': (
            5000,
            {'*': (
                10000,
                {'curve from 0 to 1': 
                    {'*': (0.01, 'time')}
                }
            )}
    )},

    'global longevity': {
        'initial value': 200 # At this age all organisms must die
    },

    'autotrophs productivity': {
        'initial value': 100000.1  
    # Each organism has a different photosynthesis capacity, but this capacity is multiplied
    # by the value of 'autotrophs productivity', that is a variable of the experiment that 
    # remains always the same, although the user can change it at any time.
    }
}


# genes:

_gene_energy_reserve = {
            # This is the definition of the gene 'energy reserve'
            'initial value': 10000.2,
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
                """,
                '+': (
                    'energy reserve',
                    {'*': (
                        '#ecosystem autotrophs productivity',
                        {'extract #biotope sunlight (percentage)': (
                            'normalized location x',
                            'normalized location y',
                            0.2
                        )}                       
                    )}
                )},
            'value after mutation': 'energy reserve at birth',
            'allowed interval': [0, 'energy storage capacity']
        }

_gene_nutrient_A_reserve = {
    'initial value': 500.0,
    'value in next cycle': {
        '+': (
            'nutrient A reserve',
            {'extract #biotope nutrient A (percentage)': (
                'normalized location x',
                'normalized location y',
                {'uniform': [0, 0.105]}  # Every organism can extract at most the 25 per cent of nutrient A from its biotope location
            )}
        )},
    'value after mutation': 'nutrient A reserve at birth'
}

_gene_nutrient_B_reserve = {
    'initial value': 1000.5,
    'value in next cycle': {
        '+': (
            'nutrient B reserve',
            {'extract #biotope nutrient B (percentage)': (
                'normalized location x',
                'normalized location y',
                {'uniform': [0, 0.105]}  # Every organism can extract at most the 25 per cent of nutrient A from its biotope location
            )}
        )},
    'value after mutation': 'nutrient A reserve at birth'
}

_gene_optimal_temperature = {
            # This is the definition of the gene 'optimal temperature'
            'help':
            """
                All organisms have a probability of dying at any given moment. But every 
                organism will have an optimal environmental temperature that minimizes that 
                probability.
            """,
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
            """,
            'initial value': {
                'uniform': [0, 2000]
            },
            'value after mutation': {
                'gauss': (
                    'temperature adaptation level',
                    '#biotope seasons speed'
                )},
            'allowed interval': [0.00001, 'infinity']
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
        """,
        'or': (
            # RANDOM CAUSE OF DETH:
            {'random true': 0.0005},
            # DEATH BY STARVATION:
            {'<': ('energy reserve', 100.0)},
            {'<': ('nutrient A reserve', 1.0)},
            {'<': ('nutrient B reserve', 0.3)},
            # DEATH BY TEMPERATURE:
            {'>': (
                {'gauss': (
                    {'/': (
                        {'**': (
                            {'-': (
                                'optimal temperature',
                                {'#biotope temperature': ('normalized location x', 'normalized location y') }
                            )},
                            2
                        )},
                        'temperature adaptation level'
                    )},
                    0.1
                )},
                {'chi-squared': 4}
            )},
            # DEATH BY OLD AGE:
            {'>': (
                {'gauss': ('age', 'age')},
                '#ecosystem global longevity'
                )}
        )
    }

_organisms_category_a = {
    # Define initial number of organisms:
    'initial number of organisms': 200,
    'genes': {
        'category': {
            'initial value': 'A'
            },
        'species': {
            # An organism will never attack any other organism of the same species. It only
            # attacks organisms of other species.
            'initial value': {'random integer': [0, 999999]},
            'value after mutation': {
                'if': (
                    # Condition:
                    {'random true': 'species identity mutation frequency'},
                    # Value if condition == True:
                    {'random integer': [0, 999999]},
                    # Value if condition == False:
                    'species'
                    )
            }
        },
        'species identity mutation frequency': {
            'initial value': 1.0,
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
        'energy reserve at birth': {
            'initial value': 1000.3
        },
        'nutrient A reserve at birth': {
            'initial value': 100.4
        },
        'nutrient B reserve at birth': {
            'initial value': 100.5
        },        
        'energy reserve': _gene_energy_reserve,
        'nutrient A reserve': _gene_nutrient_A_reserve,
        'nutrient B reserve': _gene_nutrient_B_reserve,
        'energy storage capacity': {
            'help':
            """
                Maximum possible energy reserve
            """,
            'initial value': {
                'uniform': [20000, 200000]
            },
            'value after mutation': \
            _default_value_after_mutation_B('energy storage capacity')
            ,
            'allowed interval': [0, 'infinity']
        },
        'nutrient A storage capacity': {
            'help':
            """
                Maximum possible nutrient A reserve
            """,
            'initial value': {
                'uniform': [20000, 200000]
            },
            'value after mutation': \
            _default_value_after_mutation_A('nutrient A storage capacity')
            ,
            'allowed interval': [0, 'infinity']
        },
        'nutrient B storage capacity': {
            'help':
            """
                Maximum possible nutrient B reserve
            """,
            'initial value': {
                'uniform': [20000, 200000]
            },
            'value after mutation': \
            _default_value_after_mutation_B('nutrient B storage capacity')
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
        'minimum nutrient A reserve for procreating': {
            'help':
            """
                Minimum nutrient A reserve for procreating
            """,
            'initial value': {
                'uniform': [0, 30]
            }
        },
        'minimum nutrient B reserve for procreating': {
            'help':
            """
                Minimum nutrient B reserve for procreating
            """,
            'initial value': {
                'uniform': [0, 30]
            }
        },
        'speed': {
            'help':
            """
                Number of positions that moves every time cycle
            """,
            'initial value': {
                'uniform': [0, 14]
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
            'initial value': 3.5,
            'value after mutation': \
            _default_value_after_mutation_A('radius of procreation')
        },
        'attack capacity': {
            'initial value': {
                'uniform': [0, 20000]
            },
            'value after mutation': \
            make_variation('attack capacity', absolute_variation = {'gauss': (0, 1)})
        },
        'basal defense capacity': {
            'initial value': {
                'uniform': [0, 20]
            },
            'value after mutation': \
            _default_value_after_mutation_A('defense capacity')
        },
        'defense capacity': {
            'initial value': {
                'uniform': [0, 20]
            },
            'value in next cycle': {
                '+': (
                    'basal defense capacity',
                    'nutrient B reserve'
                    )
            },
            'value after mutation': 'basal defense capacity'
        },
        'mean aggressiveness': {
            'initial value': {
                'uniform': [0.5, 1]
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
                'uniform': [0.5, 1]
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
    'decide procreate': True,
#        'and': (
#            {'random true': 'procreation frequency'},
#            {'>': (
#                'energy reserve',
#                'minimum energy reserve for procreating'
#            )},
#            {'>': (
#                'nutrient A reserve',
#                'minimum nutrient A reserve for procreating'
#            )},
#            {'>': (
#                'nutrient B reserve',
#                'minimum nutrient B reserve for procreating'
#            )}
#    )},
    'decide move': {
        'random true': 'moving frequency'
    },
    'decide hunt': {
        'random true': 'aggressiveness'
    },
    'decide attack #prey': {
        '!=': ('species', '#prey species')
    },
}

_organisms_category_a['decisions'] = _decisions

_constraints = {
    'can kill #prey': {
        '>': (
            'attack capacity',
            '#prey defense capacity'
        ) 
    },
    'can procreate': {
        'and': (
            {'<': (
                lambda organism: organism.parent_ecosystem.population(),
                '#ecosystem maximum population allowed'
            )},
            {'>': (
                'energy reserve',
                {'+': (
                    'energy reserve at birth',
                    {'cost': 'procreate'},
                    {'cost': 'stay alive'},
                    100.1
                )}
            )},
            {'>': (
                'nutrient A reserve',
                {'+': (
                    'nutrient A reserve at birth',
                    {'cost': ('procreate', 'nutrient A reserve')},
                    {'cost': ('stay alive', 'nutrient A reserve')}
                )}
            )},
            {'>': (
                'nutrient B reserve',
                {'+': (
                    'nutrient B reserve at birth',
                    {'cost': ('procreate', 'nutrient B reserve')},
                    {'cost': ('stay alive', 'nutrient B reserve')}
                )}
            )}
    )},
    'die': _constraint_die
}

_cost_move = {
    'energy reserve': {
        '+': (
            {'*': (0.000002,
                   'attack capacity',
                   'defense capacity',
                   'hunt radius')
            },
            {'*': (0.02, 'speed')},
            {'*': (0.01, 'photosynthesis capacity')},
            0.001
        )},
    'nutrient A reserve': {
        '+': (
            {'*': (0.00000002,
                   'attack capacity',
                   'basal defense capacity',
                   'radius of procreation')
            },
            {'*': (0.002, 'speed')},
            {'*': (0.0001, 'photosynthesis capacity')},
            0.001
        )},
    'nutrient B reserve': {
        '+': (
            {'*': (0.00000002,
                   'attack capacity',
                   'basal defense capacity',
                   'radius of procreation')
            },
            {'*': (0.002, 'speed')},
            {'*': (0.0001, 'photosynthesis capacity')},
            0.001
        )}
}

_costs = {
    'move': _cost_move,
    'procreate': {
        'energy reserve': {'*': (
            0.00001,
            'energy reserve at birth'
        )},
        'nutrient A reserve': {'+': (
            0.0012,
            'nutrient A reserve at birth'
        )},
        'nutrient B reserve': {'+': (
            0.0005,
            'nutrient B reserve at birth'
        )}

    },

    'stay alive': {
        'energy reserve': {'+': (
            0.1,
            {'*': (0.0001, 'temperature adaptation level')},
            {'*': (0.0001, 'photosynthesis capacity growth')},
            {'*': (0.00001, 'photosynthesis capacity')},
            {'*': (0.0001, 'indicator gene A')},
            {'*': (0.0001, 'basal defense capacity')},
            {'*': (0.0001, 'attack capacity')},
            {'*': (0.01, 'speed')},
            {'*': (0.2, 'hunt radius')},
            {'*': (0.00001, 'energy storage capacity')},
            {'*': (0.0001, 'nutrient A storage capacity')},
            {'*': (0.0002, 'nutrient B storage capacity')},
            {'*': (5.0, 'procreation frequency')},
            {'*': (5.0, 'radius of procreation')},
            {'*': (0.01, 'mutation frequency')}
        )},
        'nutrient A reserve': {'+': (
            0.005,
            {'*': (0.0001, 'temperature adaptation level')},
            {'*': (0.00001, 'photosynthesis capacity growth')},
            {'*': (0.0001, 'basal defense capacity')},
            {'*': (0.000005, 'attack capacity')},
            {'*': (0.003, 'speed')},
            {'*': (0.003, 'hunt radius')},
            {'*': (0.000002, 'energy storage capacity')},
            {'*': (0.002, 'nutrient A storage capacity')},
            {'*': (0.00005, 'nutrient B storage capacity')},
            {'*': (0.002, 'radius of procreation')},
            {'*': (0.0001, 'mutation frequency')}
        )},
        'nutrient B reserve': {'+': (
            0.002,
            {'*': (0.00001, 'temperature adaptation level')},
            {'*': (0.00001, 'photosynthesis capacity growth')},
            {'*': (0.0001, 'basal defense capacity')},
            {'*': (0.000005, 'attack capacity')},
            {'*': (0.03, 'speed')},
            {'*': (0.03, 'hunt radius')},
            {'*': (0.0000002, 'energy storage capacity')},
            {'*': (0.0002, 'nutrient A storage capacity')},
            {'*': (0.00005, 'nutrient B storage capacity')},
            {'*': (0.0002, 'radius of procreation')},
            {'*': (0.0001, 'mutation frequency')}
        )}
    }
}

from Basic_tools import *

_organisms_category_b = deep_copy_of_a_dictionary(_organisms_category_a)

_organisms_category_b['genes']['category'] = {'initial value': 'B'}
_organisms_category_b['genes']['speed'] = {'initial value': 0}





my_example_of_ecosystem_settings = {
    'help': ''' This is an example of ecosystem settings ''',
    'new operators': _operator_definitions,
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






