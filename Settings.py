from Basic_tools import *

""" ******************************************************* """
"""                                                         """
"""                     E X A M P L E                       """
"""                                                         """
""" ******************************************************* """

_biotope_size = (400, 200)

Store_data = False

Elements_to_store = {
    'help':

    """
        In this dictionary we indicate what and how often to store:

            'Once'  means that this data is stored only once at the
                    begining of the file
            200     means that this data is stored once every 200 cycles
            None    means that this data is never stored

    """,

    'genes': {
        'nutrient B reserve at birth': None,
        'photosynthesis capacity growth': None,
        'nutrient B storage capacity': None,
        'generation': 20000,
        'energy reserve': 10000,
        'nutrient A reserve': None,
        'temperature adaptation level': 4000,
        'aggressiveness': 2000,
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
        'age': 2000,
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
        'general costs level': None,
        'maximum population allowed': 100,
        'autotrophs productivity': 'Once',
        'population': 2000
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
        # You can prevent any binary operator from being associative:
        'is associative': False,
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 2),
        'output function #a #b': my_operator
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

    'random amount': {
        'output function #factor': {'*': (
            '#factor',
            {'chi-squared': 1}
            )
        }
    },

    'gauss variation': {
        'output function #value': {
            'gauss': (
                '#value',
                {'/': ('#value', 4)}
            )}
    },

    'variate': {
        # You can prevent any binary operator from being associative
        'is associative': False,
        'output function #value #probability_of_change': {
            'if': (
                {'random true': '#probability_of_change'},
                {'gauss variation': '#value'},
                '#value'
            )}
    }
}

# FEATURES:

_sunlight = {
    'matrix size': (50, 50),
    # No matters the size of the ecosystem (it might be changed later for
    # further experiments), we will store 25x25 = 625 values of sunlight in any
    # giving moment. Each value correspond to a rectangular region of the
    # ecosystem. If the size of the ecosystem is 200x100, then
    # the size of each region must be 8x4.

    'initial value #x #y': {'+': (5.0, '#x', '#y')},
    # No matters the size of the ecosystem nor the size of the matrix of
    # sunlight values, the function that gives the value of each point is
    # defined in the square [0, 1] x [0, 1], i.e. the function
    # initial_value(x, y) of any substance is defined for 0 <= x <= 1 and
    # 0 <= y <= 1
    # This way, we can change the number of values we store without having to
    # change any function definition.

    'value after updating #x #y': {
        # Each time the substance evolves, the whole matrix change its values,
        # calling this function. But this function is defined for 0 <= x <= 1
        # and 0 <= y <= 1. Thus, for each entry (i, j) of the matrix, we call
        # this function with x = i / size_x   and   y = j /size_y
        # where (size_x, size_y) is the size of the matrix of this substance.
        # 'time' is the number of cycles since the experiment started.
        'help':
        """
            Sunlight leads the climate, providing food for autotrophs and
            powering the rise of temperatures.
            This feature varies from 0 to 4. In the poles is much lower than in
            the equator. But globally varies from winter to summer. Winters
            occur in the north and in the south at the same time (as summers
            do), because both poles are the same place.
        """,
        '+': (
            9,
            {'*': (
                -1,
                {'cos': {'*': (2, pi, '#y')}}
            )},
            {'*': (
                5,
                {'sin': {'*': ('seasons speed', 'time')}}
            )}
        )},

    # The values of the matrix of sunlight is updated every 1 cycle.
    'update once every': 1
}

_temperature = {
    'matrix size': (50, 50),
    'initial value #x #y': 10.0,
    'value after updating #x #y': {
        'help':
        """
            Each cycle the temperature is increased by sunlight, but the 10 per
            cent of the accumulated heat is lost in every cycle.
        """,
        '*': (
            # this is the proportion (85 per cent) of the heat that remains in
            # the biotope:
            0.75,
            {'+': (
                # the new value depends on the previous value:
                {'#biotope temperature': ('#x', '#y')},
                {'#biotope sunlight': ('#x', '#y')}
            )}
        )},
    # The values of the matrix of sunlight is updated every 1 cycle.
    'update once every': 1
}

_nutrient_A = {
    'matrix size': (75, 50),
    'initial value #x #y': {
        'if': (
            {'random true': 0.03},
            {'uniform': [0, 100]},
            {'*': (20.5, '#x', '#y')}
        )},
    'value after updating #x #y': {
        '+': (
            # Generating:
            {'*': (200, '#x', chi_squared(2))},
            # Spreading:
            {'*': (
                # the location (#x, #y) keeps the 80 per cent of its amount
                # of nutrient A:
                0.80,
                {'#biotope nutrient A': ('#x', '#y')}
            )},
            {'*': (
                # the location (#x, #y) gets the 5 per cent from each
                # of the adjacent locations:
                0.05,
                {'+': (
                    {'#biotope nutrient A': (
                        {'+': ('#x', 'normalized abcissa unit')},
                        '#y'
                    )},
                    {'#biotope nutrient A': (
                        {'-': ('#x', 'normalized abcissa unit')},
                        '#y'
                    )},
                    {'#biotope nutrient A': (
                        '#x',
                        {'+': ('#y', 'normalized ordinate unit')},
                    )},
                    {'#biotope nutrient A': (
                        '#x',
                        {'-': ('#y', 'normalized ordinate unit')}
                    )}
                )}
            )}
        )},
    # The values of the matrix of nutrient A is updated once every 20 cycles:
    'update once every': 2
}

_nutrient_B = {
    'matrix size': (80, 40),
    'initial value #x #y': {
        'if': (
            {'random true': 0.04},
            {'uniform': [0, 2000]},
            {'+': (
                200.0,
                {'-': ('#x', '#y')}
            )}
        )},
    'value after updating #x #y': {
        '+': (
            # Generating:
            {'*': (90, '#y', chi_squared(2))},
            # Spreading:
            {'*': (
                # the location (#x, #y) keeps the 90 per cent of its amount
                # of nutrient B:
                0.90,
                {'#biotope nutrient B': ('#x', '#y')}
            )},
            {'*': (
                # the location (#x, #y) gets the 2,5 per cent from each
                # of the adjacent locations:
                0.025,
                {'+': (
                    {'#biotope nutrient B': (
                        {'+': ('#x', 'normalized abcissa unit')},
                        '#y'
                    )},
                    {'#biotope nutrient B': (
                        {'-': ('#x', 'normalized abcissa unit')},
                        '#y'
                    )},
                    {'#biotope nutrient B': (
                        '#x',
                        {'+': ('#y', 'normalized ordinate unit')},
                    )},
                    {'#biotope nutrient B': (
                        '#x',
                        {'-': ('#y', 'normalized ordinate unit')}
                    )}
                )}
            )}
        )},
    # The values of the matrix of nutrient B is updated once every 15 cycles:
    'update once every': 5
}

nutrient_C_matrix = Matrix()

nutrient_C_matrix.copy_matrix([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 5, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 5, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

nutrient_D_matrix = Matrix()

nutrient_D_matrix.copy_matrix([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 6, 0, 0, 0, 0, 0, 0],
    [0, 0, 6, 6, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])


def _calculate_value_nutrien_C(x, y):
    return nutrient_C_matrix.get_value_from_normalized_x_y(x, y)


def _calculate_value_nutrien_D(x, y):
    return nutrient_C_matrix.get_value_from_normalized_x_y(x, y)

_nutrient_C = {
    'matrix size': (10, 10),
    'initial value #x #y': _calculate_value_nutrien_C,
    'value after updating #x #y': _calculate_value_nutrien_C,
    'update once every': 4
}

_nutrient_D = {
    'matrix size': (10, 10),
    'initial value #x #y': _calculate_value_nutrien_D,
    'value after updating #x #y': _calculate_value_nutrien_D,
    'update once every': 4
}

_biotope = {
    'size': _biotope_size,
    'biotope features': {
        'sunlight': _sunlight,
        'temperature': _temperature,
        'nutrient A': _nutrient_A,
        'nutrient B': _nutrient_B,
        'seasons speed': {
            'initial value': 0.37,
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
        gene=gene,
        relative_variation={'uniform': [-0.05, 0.05]},
        # "relative variation" means that the gene will
        # be increased or decreased proportionally
        # to its current value. For example:
        # relative_variation = -0.034 means that the gene
        # will lose the 3.4 per cent of its value
        probability_of_change='mutation frequency')


def _default_value_after_mutation_B(gene):
    """
        Since this module is common to many genes,
        we define it as an independent function
    """
    return make_variation(
        gene=gene,
        absolute_variation={'uniform': [-0.05, 0.05]},
        # Example: if absolute_variation = -0.034 means that
        # the gene will be 0.034 units less than before
        probability_of_change='mutation frequency')


def _default_value_after_mutation_C(gene):
    """
        Since this module is common to many genes,
        we define it as an independent function.
        This is an example of the use of 'function' operator
    """

    def _value(gene_value, mutation_frequency):
        if random_true(mutation_frequency):
            # This is the random function of a 'cubic'
            # distribution of probability:
            return gene_value * (1 + uniform(-0.5, 0.5)**3)
        else:
            return gene_value

    # This means that the function _value will be
    # called and two parameters will be passed
    # to it: The values of gene and 'mutation frequency':
    return {'function': (_value, gene, 'mutation frequency')}

_ecosystem_features = {

    'general costs level': {
        'initial value': 0.5
    },

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
        'initial value': 200000,

        '+':
            (
                200000,
                {'*': (
                    10000,
                    {
                        'curve from 0 to 1':
                        {'*': (0.01, 'time')}
                    }
                )}
            )
    },

    'global longevity': {
        'initial value': 200  # At this age all organisms must die
    },

    'autotrophs productivity': {
        'initial value': 15000
        # Each organism has a different photosynthesis capacity,
        # but this capacity is multiplied
        # by the value of 'autotrophs productivity', that
        # is a variable of the experiment that
        # remains always the same, although the user
        # can change it at any time.
    }
}


# genes:

_gene_energy_reserve = {
    # This is the definition of the gene 'energy reserve'
    'initial value': 20000.2,
    'value in next cycle': {
        'help':
        """
            The increasement of the energy reserve depends
            both on the amount of sunlight
            and the photosynthesis capacity of the organism.

            'extract feature' returns certain amount of sunlight
            and also decreased the
            available amount of sunlight for other organisms that
            act after this one.

            'normalized location' returns the location of the current
            organisms but in these terms:
                If the location of the organism is (i, j) and the size
                of the ecosystem is (size_x, size_y), then:
                    'normalized location x' returns  i / size_x
                    and
                    'normalized location y' returns j / size_y
        """,
        '+': (
            'energy reserve',
            {'*': (
                '#ecosystem autotrophs productivity',
                {'extract #biotope sunlight (proportion)': (
                    'normalized location x',
                    'normalized location y',
                    {'curve from 0 to 1': 'photosynthesis capacity'}
                )}
            )}
        )},
    'value after mutation': 'energy reserve at birth',
    'allowed interval': [0, 'energy storage capacity'],
    'offer to sell': {
        'amount': {
            'if': (
                {
                    '<': (
                        'energy reserve',
                        'minimum energy reserve for procreating'
                        )
                    },
                0,
                {'*': (0.1, 'energy reserve')}
            )},
        'prices': {
            'nutrient A reserve': 'price nutr A / energy',
            'nutrient B reserve': 'price nutr B / energy',
        }
    }
    }

_gene_nutrient_A_reserve = {
    'initial value': 5000.0,
    'value in next cycle': {
        '+': (
            'nutrient A reserve',
            {'extract #biotope nutrient A (proportion)': (
                'normalized location x',
                'normalized location y',
                {'curve from 0 to 1': 'nutrient A extraction capacity'}
            )}
        )},
    'value after mutation': 'nutrient A reserve at birth',
    'offer to sell': {
        'amount': 'nutrient A surplus',
        'prices': {
            'nutrient B reserve': 'price nutr B / nutr A',
            'energy reserve': 'price energy / nutr A'
        }
    }
}

_gene_nutrient_B_reserve = {
    'initial value': 10000.5,
    'value in next cycle': {
        '+': (
            'nutrient B reserve',
            {'extract #biotope nutrient B (proportion)': (
                'normalized location x',
                'normalized location y',
                {'curve from 0 to 1': 'nutrient B extraction capacity'}
            )}
        )},
    'value after mutation': 'nutrient B reserve at birth',
    'offer to sell': {
        'amount': 'nutrient B surplus',
        'prices': {
            'nutrient A reserve': 'price nutr A / nutr B',
            'energy reserve': 'price energy / nutr B'
        }

    }
}

_gene_optimal_temperature = {
            # This is the definition of the gene 'optimal temperature'
            'help':
            """
                All organisms have a probability of dying at any given moment.
                But every organism will have an optimal environmental
                temperature that minimizes that probability.
            """,
            'initial value': {
                'uniform': [0, 4000]
            },
            'value after mutation':
            _default_value_after_mutation_B('optimal temperature')
        }

_gene_temperature_adaptation_level = {
            # This is the definition of the gene 'temperature adaptation level'
            'help':
            """
                Each organism have a different tolerance to too high or too
                low temperatures.
                If the gene 'temperature adaptation level' has a high value,
                then the organism may survive in a wider range of temperatures
                than otherwise.
            """,
            'initial value': {
                'uniform': [0, 20000]
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
            If an organism isn't killed by a predator, it has 3 different
            ways of dying:
                - BY CHANCE: It can be an illness or an accident. Every
                        organism has a chance of 0.05 percent of dying
                        because of this reason. It could be an illness,
                        an accident, ...
                - BY STARVATION: If the energy reserve of an organism is
                        less than 1000 units, it dies.
                - BY HEAT OR COLD: If the temperature of the environment
                        is very different
                        from the 'optimal temperature' of the organism,
                        it has a high
                        probability of dying. But if the organism has a
                        high 'temperature adaptation level', it will lower
                        that probability.
                - BY OLD AGE: As an organism get old it increases its
                        chance of dying.
        """,
        'or': (
            # RANDOM CAUSE OF DETH:
            {'random true': 0.0005},

            # """
            # Resultado experimental:

            # Si aumentamos esta probabilidad de muerte aleatoria,
            # favorecemos que los organismos evolucionen para tener
            # un metabolismo mas rapido 'metabolic speed'.

            # Posible explicacion:

            # Los organismos con metabolismo veloz son muy buenos repoblando
            # zonas despobladas, ya que se reproducen mas rapido.
            # Sin embargo, los de metabolismo lento son capaces de vivir
            # con muy poco, sobreviviendo a largo plazo en una zona
            # superpoblada.
            # """

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
                                {
                                    '#biotope temperature':
                                        (
                                            'normalized location x',
                                            'normalized location y'
                                        )
                                }
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


def _gene_creator(gene_name, mean=1):
    return {
        'initial value': {
            'gauss': (mean, 0.2 * mean),
            'allowed interval': [0.00001, 'infinity']
            },
        'value after mutation': {
            'triangular': (
                {'*': (0.8, gene_name)},
                {'*': (1.25, gene_name)},
                gene_name
                )
            }
        }

_organisms_category_a = {
    # Define initial number of organisms:
    'initial number of organisms': 100,
    'genes': {
        'category': {
            'initial value': 'A'
            },
        'species': {
            # An organism will never attack any other organism
            # of the same species. It only
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
            'initial value': {'uniform': [0, 1.0]},
            'value after mutation':
            _default_value_after_mutation_B(
                'species identity mutation frequency'
            ),
            'allowed interval': [0, 1]
        },
        'red': {
            'initial value': {'uniform': [0, 255]},
            'value after mutation': {
                '+': (
                    'red',
                    {'gauss': (0, 4.5)}
                    )
            },
            'allowed interval': [0, 255]
        },
        'green': {
            'initial value': {'uniform': [0, 255]},
            'value after mutation': {
                '+': (
                    'green',
                    {'gauss': (0, 4.5)}
                    )
            },
            'allowed interval': [0, 255]
        },
        'blue': {
            'initial value': {'uniform': [0, 255]},
            'value after mutation': {
                '+': (
                    'blue',
                    {'gauss': (0, 4.5)}
                    )
            },
            'allowed interval': [0, 255]
        },
        'color 1': {
            'initial value': [
                {'round': 'red'},
                {'round': 'green'},
                {'round': 'blue'},
                ],
            'value after mutation': [
                {'round': 'red'},
                {'round': 'green'},
                {'round': 'blue'},
                ]
        },
        'color 2': {
            'initial value': [
                {'round': 'red'},
                {'round': 'green'},
                {'round': 'blue'},
                ],
            'value after mutation': [
                {  # RED:
                    'round': {
                        '*': (
                            255,
                            {
                                'curve from 0 to 1': {
                                    '*': (
                                        0.5,
                                        {
                                            '+': (
                                                'price energy / nutr A',
                                                'price energy / nutr B')
                                        }
                                        )
                                    }
                            }
                            )
                    }
                },
                {  # GREEN:
                    'round': {
                        '*': (
                            255,
                            {
                                'curve from 0 to 1': {
                                    '*': (
                                        0.5,
                                        {
                                            '+': (
                                                'price nutr A / energy',
                                                'price nutr A / nutr B')
                                        }
                                        )
                                    }
                            }
                            )
                    }
                },
                {  # BLUE:
                    'round': {
                        '*': (
                            255,
                            {
                                'curve from 0 to 1': {
                                    '*': (
                                        0.5,
                                        {
                                            '+': (
                                                'price nutr B / nutr A',
                                                'price nutr B / energy')
                                        }
                                        )
                                    }
                            }
                            )
                    }
                },
            ]
        },
        'color 3': {
            'initial value': [
                {'round': 'red'},
                {'round': 'green'},
                {'round': 'blue'},
                ],
            'value after mutation': [
                {  # RED:
                    'round': {
                        '*': (
                            255,
                            {
                                'curve from 0 to 1': {
                                    '*': (
                                        1.2,
                                        'metabolic speed'
                                        )
                                    }
                            }
                            )
                    }
                },
                {  # GREEN:
                    'round': {
                        '*': (
                            255,
                            {
                                'curve from 0 to 1': {
                                    '*': (
                                        1.2,
                                        'metabolic speed'
                                        )
                                    }
                            }
                            )
                    }
                },
                {  # BLUE:
                    'round': {
                        '*': (
                            255,
                            {
                                'curve from 0 to 1': {
                                    '*': (
                                        1.2,
                                        'metabolic speed'
                                        )
                                    }
                            }
                            )
                    }
                },
            ]
        },
        'color': {
            'initial value': 'color 1',
            'value in next cycle': {
                'choice': (
                    {
                        '%': (
                            {'/': ('time', 20)},
                            3
                            )
                        },
                    (0, 'color 1'),
                    (1, 'color 2'),
                    (2, 'color 3')
                )
            }
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
            'initial value': 0.5,
            'value in next cycle': {
                '+': (
                    'photosynthesis capacity',
                    'photosynthesis capacity growth'
                    )
            },
            'value after mutation': 0.5,
            'allowed interval': [0, 'infinity']
        },
        'photosynthesis capacity growth':
            _gene_creator('photosynthesis capacity growth', mean=0.5),
        'nutrient A extraction capacity': {
            'initial value': {'uniform': (0, 5)},
            'value after mutation': {
                'gauss': (
                    'nutrient A extraction capacity',
                    0.3
                    )
            },
            'allowed interval': [0, 'infinity']
        },
        'nutrient B extraction capacity': {
            'initial value': {'uniform': (0, 5)},
            'value after mutation': {
                'gauss': (
                    'nutrient B extraction capacity',
                    0.3
                    )
            },
            'allowed interval': [0, 'infinity']
        },
        'energy reserve at birth': {
            'initial value': {'uniform': [0, 3000]},
            'value after mutation':
            _default_value_after_mutation_A('energy reserve at birth')
        },
        'nutrient A reserve at birth': {
            'initial value': {'uniform': [0, 200]},
            'value after mutation':
            _default_value_after_mutation_A('nutrient A reserve at birth')
        },
        'nutrient B reserve at birth': {
            'initial value': {'uniform': [0, 200]},
            'value after mutation':
            _default_value_after_mutation_A('nutrient B reserve at birth')
        },
        'energy reserve': _gene_energy_reserve,
        'nutrient A reserve': _gene_nutrient_A_reserve,
        'nutrient B reserve': _gene_nutrient_B_reserve,
        'price nutr A / energy': _gene_creator('price nutr A / energy'),
        'price nutr B / energy': _gene_creator('price nutr B / energy'),
        'price nutr A / nutr B': _gene_creator('price nutr A / nutr B'),
        'price nutr B / nutr A': _gene_creator('price nutr B / nutr A'),
        'price energy / nutr A': _gene_creator('price energy / nutr A'),
        'price energy / nutr B': _gene_creator('price energy / nutr B'),
        'energy storage capacity': {
            'help':
            """
                Maximum possible energy reserve
            """,
            'initial value': {'random amount': 20000},
            'value after mutation':
            _default_value_after_mutation_A('energy storage capacity'),
            'allowed interval': [0, 'infinity']
        },
        'nutrient A storage capacity': {
            'help':
            """
                Maximum possible nutrient A reserve
            """,
            'initial value': {'random amount': 2000},
            'value after mutation':
            _default_value_after_mutation_A('nutrient A storage capacity'),
            'allowed interval': [0, 'infinity']
        },
        'nutrient B storage capacity': {
            'help':
            """
                Maximum possible nutrient B reserve
            """,
            'initial value': {'random amount': 2000},
            'value after mutation':
            _default_value_after_mutation_A('nutrient B storage capacity'),
            'allowed interval': [0, 'infinity']
        },
        'minimum energy reserve for procreating': {
            'help':
            """
                Minimum energy reserve for procreating
            """,
            'initial value': {
                'uniform': [0, 3000]
            },
            'value after mutation':
            _default_value_after_mutation_A(
                'minimum energy reserve for procreating'
                )
        },
        'minimum nutrient A reserve for procreating': {
            'help':
            """
                Minimum nutrient A reserve for procreating
            """,
            'initial value': {
                'uniform': [0, 200]
            },
            'value after mutation':
            _default_value_after_mutation_A(
                'minimum nutrient A reserve for procreating'
                )
        },
        'minimum nutrient B reserve for procreating': {
            'help':
            """
                Minimum nutrient B reserve for procreating
            """,
            'initial value': {
                'uniform': [0, 200]
            },
            'value after mutation':
            _default_value_after_mutation_A(
                'minimum nutrient B reserve for procreating'
                )
        },
        'nutrient A surplus': {
            'help':
            """
                The amount of nutrient A reserve that is
                available for being spent in trade
            """,
            'initial value': 0,
            'value in next cycle': {
                '-': (
                    'nutrient A reserve',
                    {
                        '+': (
                            10.5,
                            'minimum nutrient A reserve for procreating'
                        )
                    }
                )
            },
            'value after mutation': 0,
            'allowed interval': [0, 'infinity']
        },
        'nutrient B surplus': {
            'help':
            """
                The amount of nutrient B reserve that is
                available for being spent in trade
            """,
            'initial value': 0,
            'value in next cycle': {
                '-': (
                    'nutrient B reserve',
                    {
                        '+': (
                            8.5,
                            'minimum nutrient B reserve for procreating'
                        )
                    }
                )
            },
            'value after mutation': 0,
            'allowed interval': [0, 'infinity']
        },
        'speed': {
            'help':
            """
                Number of positions that moves every time cycle
            """,
            'initial value': {
                'uniform': [0, 1.2]
            },
            'value after mutation':
            make_variation(
                gene='speed',
                absolute_variation={'uniform': [-0.2, 0.2]},
                probability_of_change='mutation frequency'
                ),
            'allowed interval': [0, 'infinity']
        },
        'hunt radius': {
            'help':
            """
                The radius whitin a prey must be in order to be hunted
            """,
            'initial value': {'uniform': [0, 1.5]},
            'value after mutation':
            _default_value_after_mutation_A('hunt radius')
        },
        'radius of procreation': {
            'initial value': {'uniform': [0, 3.5]},
            'value after mutation':
            _default_value_after_mutation_A('radius of procreation')
        },
        'attack capacity': {
            'initial value': {
                'uniform': [0, 20]
            },
            'value after mutation':
            make_variation(
                'attack capacity',
                relative_variation={'gauss': (0, 0.1)}
                )
        },
        'basal defense capacity': {
            'initial value': {
                'uniform': [0, 200]
            },
            'value after mutation':
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
                'uniform': [0, 1]
            },
            'value after mutation':
            _default_value_after_mutation_B('aggressiveness'),
        },
        'aggressiveness': {
            'initial value': 0,
            'value in next cycle': {
                'gauss': ('mean aggressiveness', 0.1)
            },
            'allowed interval': [0, 1]
        },
        'digestion capacity': _gene_creator('digestion capacity', mean=20),
        'poison level': _gene_creator('poison level', mean=0.3),
        'mutation frequency': {
            'initial value': {
                'uniform': [0, 1]
            },
            'value after mutation':
            _default_value_after_mutation_A('mutation frequency')
        },
        'moving frequency': {
            'initial value': {
                'uniform': [0, 1]
            },
            'value after mutation':
            _default_value_after_mutation_A('moving frequency')
        },
        'procreation frequency': {
            'initial value': {
                'uniform': [0, 1]
            },
            'value after mutation':
            _default_value_after_mutation_A('procreation frequency')
        },
        'optimal temperature': _gene_optimal_temperature,
        'temperature adaptation level': _gene_temperature_adaptation_level,
        'actions sequence': {
            'initial value': {
                'literal': [
                    'move',
                    'hunt',
                    'do internal changes',
                    'stay alive',
                    'interchange substances with other organisms',
                    'procreate']},
            'value after mutation': {
                'if': ({'true with probability': 'mutation frequency'},
                       {'shuffle': 'actions sequence'},
                       'actions sequence')
            }
        },
        'metabolic time': {
            'initial value': 0,
            'value in next cycle': {'+': (
                'metabolic time',
                {'random amount': 'metabolic speed'}
                )}
        },
        'metabolic speed': {
            'initial value': 1.0,
            'value after mutation': {
                'triangular': (
                    {'*': (0.8, 'metabolic speed')},
                    {'*': (1.25, 'metabolic speed')},
                    'metabolic speed'
                )},
            'allowed interval': [0.1, 10]
        }

    }
}

_decisions_category_a = {
    'decide procreate': {
        'and': (
            {'random true': 'procreation frequency'},
            {'>': (
                'energy reserve',
                'minimum energy reserve for procreating'
            )},
            {'>': (
                'nutrient A reserve',
                'minimum nutrient A reserve for procreating'
            )},
            {'>': (
                'nutrient B reserve',
                'minimum nutrient B reserve for procreating'
            )}
            )
        },
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

_organisms_category_a['decisions'] = _decisions_category_a

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
                    {
                        'cost': ('procreate', 'energy reserve'),
                        '#distance': 'speed'
                    },
                    {'cost': ('stay alive', 'energy reserve')},
                    100.1
                )}
            )},
            {'>': (
                'nutrient A reserve',
                {'+': (
                    'nutrient A reserve at birth',
                    {
                        'cost': ('procreate', 'nutrient A reserve'),
                        '#distance': 0
                    },
                    {'cost': ('stay alive', 'nutrient A reserve')}
                )}
            )},
            {'>': (
                'nutrient B reserve',
                {'+': (
                    'nutrient B reserve at birth',
                    {
                        'cost': ('procreate', 'nutrient B reserve'),
                        '#distance': 0
                    },
                    {'cost': ('stay alive', 'nutrient B reserve')}
                )}
            )},
        )},
    'die': _constraint_die
}

_cost_move = {
    'energy reserve': {
        '+': (
            {
                '*': (
                    0.0002,
                    'attack capacity',
                    'defense capacity',
                    '#distance'
                    )
            },
            {'*': (
                0.2,
                'speed',
                'radius of procreation',
                'procreation frequency'
                )},
            {'*': (0.01, 'photosynthesis capacity')},
            0.001,
            {'secrete #biotope temperature': (
                'normalized location x',
                'normalized location y',
                'speed'
            )}
        )},
    'nutrient A reserve': {
        '+': (
            {
                '*': (
                    0.0002,
                    'attack capacity',
                    'basal defense capacity',
                    'radius of procreation',
                    '#distance'
                )
            },
            {'*': (
                0.092,
                'speed',
                'radius of procreation',
                'procreation frequency',
                '#distance'
                )},
            {'*': (
                0.01,
                'photosynthesis capacity',
                '#distance'
                )},
            0.5
        )},
    'nutrient B reserve': {
        '+': (
            {
                '*': (
                    0.00003,
                    'attack capacity',
                    'basal defense capacity',
                    'radius of procreation'
                    )
            },
            {'*': (0.02, 'speed')},
            {'*': (0.002, 'photosynthesis capacity')},
            0.1
        )}
}

_cost_stay_alive = {
        'energy reserve': {'*': (
            '#ecosystem general costs level',
            {'+': (
                0.2,
                {'secrete #biotope temperature': (
                    'normalized location x',
                    'normalized location y',
                    'metabolic speed'
                )},
                {'*': (
                    0.01,
                    'temperature adaptation level',
                    'radius of procreation')},
                {'*': (0.01, 'photosynthesis capacity growth', 'hunt radius')},
                {'*': (0.01, 'photosynthesis capacity', 'attack capacity')},
                {'*': (
                    0.01,
                    'basal defense capacity',
                    'nutrient B extraction capacity')},
                {'*': (
                    0.01,
                    'attack capacity',
                    'nutrient A extraction capacity')},
                {'*': (2.0, 'speed', 'photosynthesis capacity')},
                {'*': (0.2, 'hunt radius')},
                {'*': (0.00001, 'energy storage capacity')},
                {'*': (0.0001, 'nutrient A storage capacity')},
                {'*': (0.0002, 'nutrient B storage capacity')},
                {'*': (1.2, 'procreation frequency')},
                {'*': (1.1, 'radius of procreation')},
                {'*': (0.01, 'mutation frequency')}
            )}
        )},
        'nutrient A reserve': {'*': (
            '#ecosystem general costs level',
            {'+': (
                0.5,
                {'*': (0.0001, 'temperature adaptation level')},
                {'*': (0.00001, 'photosynthesis capacity growth')},
                {'*': (0.0001, 'basal defense capacity')},
                {'*': (0.005, 'attack capacity')},
                {'*': (0.1, 'speed', 'photosynthesis capacity growth')},
                {'*': (0.003, 'hunt radius')},
                {'*': (0.000002, 'energy storage capacity')},
                {'*': (0.002, 'nutrient A storage capacity')},
                {'*': (0.00005, 'nutrient B storage capacity')},
                {'*': (0.002, 'radius of procreation')},
                {'*': (0.0001, 'mutation frequency')}
            )}
        )},
        'nutrient B reserve': {'*': (
            '#ecosystem general costs level',
            {'+': (
                0.2,
                {'*': (0.00001, 'temperature adaptation level')},
                {'*': (0.00001, 'photosynthesis capacity growth')},
                {'*': (0.0001, 'basal defense capacity')},
                {'*': (0.000005, 'attack capacity')},
                {'*': (
                    0.1,
                    'speed',
                    'nutrient A extraction capacity',
                    'nutrient B extraction capacity')},
                {'*': (0.03, 'hunt radius')},
                {'*': (0.000002, 'energy storage capacity')},
                {'*': (0.0002, 'nutrient A storage capacity')},
                {'*': (0.00005, 'nutrient B storage capacity')},
                {'*': (0.0002, 'radius of procreation')},
                {'*': (0.0001, 'mutation frequency')}
            )}
        )}
    }


_costs = {

    'move #distance': _cost_move,

    'hunt #prey #distance': {
        'energy reserve': {'*': (
            '#prey defense capacity',
            '#distance',
            0.002
            )
        }
    },

    'eat #prey': {
        'energy reserve': {'*': (
            '#prey defense capacity',
            0.02
            )
        },
        'nutrient B reserve': {'/': (
            '#prey poison level',
            'digestion capacity'
            )
        }
    },

    'procreate #distance': {
        'energy reserve': {'*': (
            0.01,
            'energy reserve at birth',
            '#distance'
        )},
        'nutrient A reserve': {'+': (
            0.02,
            'nutrient A reserve at birth',
            'digestion capacity'
        )},
        'nutrient B reserve': {'+': (
            0.015,
            'nutrient B reserve at birth',
            'poison level'
        )},
    },

    'stay alive': _cost_stay_alive,

    'interchange substances with other organisms #amount #substance_to_sell': {
        'energy reserve': {
            'if': (
                {'==': ('#substance_to_sell', 'energy reserve')},
                {'*': (0.015, '#amount')},
                0
            )
        },
        'nutrient A reserve': {
            'if': (
                {'==': ('#substance_to_sell', 'nutrient A reserve')},
                {'*': (0.05, '#amount')},
                0
            )
        },
        'nutrient B reserve': {
            'if': (
                {'==': ('#substance_to_sell', 'nutrient B reserve')},
                {'*': (0.05, '#amount')},
                0
            )
        }
    },
    'die #cause': {
        'nutrient A reserve': {
            'if': (
                {'==': ('#cause', 'Natural deth')},
                {'secrete #biotope nutrient A': (
                    'normalized location x',
                    'normalized location y',
                    'nutrient A reserve'
                )},
                0
            )},
        'nutrient B reserve': {
            'if': (
                {'==': ('#cause', 'Natural deth')},
                {'secrete #biotope nutrient B': (
                    'normalized location x',
                    'normalized location y',
                    'nutrient B reserve'
                )},
                0
            )},
        'energy reserve': {
            'secrete #biotope temperature': (
                'normalized location x',
                'normalized location y',
                {'*': (0.0001, 'energy reserve')}
            )}
    }
}


_organisms_category_b = deep_copy_of_a_dictionary(_organisms_category_a)

_organisms_category_b['genes']['category'] = {'initial value': 'B'}
_organisms_category_b['genes']['speed'] = {'initial value': 0}
# _organisms_category_b['genes']['metabolic speed'] = {'initial value': 1}

my_example_of_ecosystem_settings = {
    'name': 'experiment_template',
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



