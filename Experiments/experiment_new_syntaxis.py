common_allowed_terms = ['help', 'comment', 'label']

LIST_OF_ALLOWED_TERMS = {
    'settings': ['biotope', 'organisms', 'costs', 'constraints'] + common_allowed_terms,
    'biotope': ['size'] + common_allowed_terms,
    'organisms': ['category name', 'initial number of organisms', 'genes', 'decisions'] + common_allowed_terms,
    'costs': [{'<action name>': '<cost>'}] + common_allowed_terms,
    '<cost>': [{'<substance name>' + ' reserve': '<function>'}]
    'constraints': ['help'] + common_allowed_terms
        },
    'organisms category': ['help', 'initial number of organisms', 'genes', 'decisions'] + common_allowed_terms,

}


biotope = {
    # Mandatory atributes
    'size': (100, 100)
}

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
    value_after_mutation = {
        'if': ({'random true': 'mutation frequency'},
               new_value)}
    return value_after_mutation

# genes

# metabolism types:

_metabolic_speed = {
    'help': 
        """
            Indicates de average number of times the organism acts each time it's its turn
        """,
    'initial value': {
        'uniform': [0, 2]
    },
    'value_after_mutation': _default_value_after_mutation('metabolic speed')
}

_metabolic_time_category_a = {
    'help':
        """
            Indicates the amount of subjective time since the last time the organism did 
            something. An organism can act again only if its metabolic time is greater than 0.
            Each time the organism acts, its metabolic time decreases in one unit. And in 
            each cycle, its metabolic time increases as much as indicates its metabolic speed.
        """
    'initial value': 0,
    'value after time cycle': {
        '+': ('metabolic time', 'metabolic speed')
    }
}

_metabolic_time_category_b = {
    'help':
        """
            Indicates the amount of subjective time since the last time the organism did 
            something. An organism can act again only if its metabolic time is greater than 0.
            Each time the organism acts, its metabolic time decreases in one unit. And in 
            each cycle, its metabolic time increases as much as indicates its metabolic speed.
        """
    'initial value': 0,
    'value after time cycle': {
        '+': (
            'metabolic time', 
            {'uniform': [0, 'metabolic speed']}
        )
    }
}

_gene_age_category_a = {
    'help': 
        """ 
            Age of organism (increase +1 every time cycle)
        """, 
    'initial value': 0,
    'value after time cycle': {
        '+': ('age', 1)
    },
    'value after mutation': {
        'if': (
            # Condition:
            {'>': ('age', 1000)},
            # Then:
            0,
            # Else:
            'age')  
    },
    'allowed interval': [0, 'inf']
}

organisms_category_a = {
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
        }
        'age': _gene_age_category_a,
        'photosynthesis capacity': {
            'help':
            """
                Capacity to transform sunlight into energy reserve
            """,
            'initial value': {
                'uniform': [0, 3000]
            },
            'value after mutation': \
            _default_value_after_mutation('photosynthesis capacity'),
            'allowed interval': [0, 'inf']
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
            _default_value_after_mutation('energy storage capacity'),
            'allowed interval': [0, 'inf']
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
            _default_value_after_mutation('speed')
        },
        'hunt radius': {
            'help':
            """
                The radius whitin a prey must be in order to be hunted
            """,
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
        },
        'indicator gene B': {
            'initial value': 1.0,
            'value after mutation': \
            _default_value_after_mutation('indicator gene B')
        },
        'energy reserve at birth': {
            'initial value': 10000.0
        },
        'energy reserve': {
            'initial value': 'energy reserve at birth',
            'value in next cycle': {
                '+': ('energy reserve',
                      'photosynthesis capacity')
            },
            'allowed interval': [0, 'energy storage capacity']
        },
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

decisions = {
    'decide procreate': {
        'and': ({'>': (
            'energy reserve',
            'minimum energy for procreating')
            },
            {'random true': 'procreating frequency'}
        )
    },
    'decide move': {
        'random true': 'moving frequency'
    },
    'decide hunt': {
        'random true': 'aggressiveness'
    },
    'decide attack': {
        '!=': ({'predator': 'species'}, {'prey': 'species'})
    }
}

constraints = {
    'can kill #prey': {
        '>': (
            {''}
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

cost_move = {
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

costs = {
    'move': cost_move
}