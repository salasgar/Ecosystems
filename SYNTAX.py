
No_effect_attributes = ['help', 'comment', 'label']

ecosystem_settings_syntaxis = {

    '$ ALLOWED ATTRIBUTES': ['biotope', 'organisms', 'constraints', 'costs', 'help', 'comment', 'label'],
    '$ MANDATORY ATTRIBUTES': ['biotope', 'organisms'],

    'biotope': { 

        '$ ALLOWED ATTRIBUTES': ['size', 'help', 'comment', 'label'],
        '$ MANDATORY ATTRIBUTES': ['size'],

        'size': '<expression>'
    },

    'organisms': {

        # all strings can be the name of a category

        '<category name>': { 

            '$ ALLOWED ATTRIBUTES': ['initial number of organisms', 'genes', 'decisions', 'help', 'comment', 'label'],
            '$ MANDATORY ATTRIBUTES': ['initial number of organisms', 'genes'],

            'initial number of organisms': '<expression>',

            'genes': {

                '$ MANDATORY ATTRIBUTES': ['actions sequence'],

                '<gene name>': { 

                    '$ ALLOWED ATTRIBUTES': ['initial value', 'value after cycle', 'value after mutation', 'allowed interval', 'help', 'comment', 'label'],
                    '$ MANDATORY ATTRIBUTES': ['initial value'],

                    'initial value': '<expression>',
                    'value after cycle': '<expression>',
                    'value after mutation': '<expression>',
                    'allowed interval': '<expression>'
                }
            },

            'decisions': { 

                'decide <action name>': '<boolean expression>'
            }
        }
    },

    'constraints': { 

        'can <action name> #<tag> #<tag> ...': '<boolean expression>',
        # if an organism 'can' do an action, it may do it or it may not. It's up to it.
        'will <action name>': '<boolean expression>' 
        # if an organism 'will' do an action, it'll do it. It can't avoid doing it.
    },

    'costs': {

        '<action name> #<tag> #<tag> ...': {
            '<substance name> reserve': '<expression>'
        }
    }
}

Gene_names = [
    'actions sequence', # Indicates the actions it will perform and in which order
    '<substance name> reserve', # It stores a certain amount of substance
    '<substance name> storage capacity', # Indicates the maximum amount of this substance that the organism can store
    '<substance name> reserve at birth', # Indicates the amount of substance reserve at birth
    '<substance name> reserve threshold to <action name>', 
        # For example, 'energy reserve threshold to move' indicates that the organism will 
        # decide to move only if its 'energy reserve' is greater than its 'energy reserve threshold to move'
    'radius of <action name>', # radius of procreation, of hunt, of searching for predators to run away from, of looking for other organisms to trade with, etc...
    '<action name>ing frequency'
]

All_actions = [
    'move',
        #  If the decision 'decide move' returns True: 
        #       Look for a place to go (there are many different ways of doing this)
        #       If the place is found:
        #           Go to that place
    'procreate',
        #   If both the decision 'decide procreate' and the constraint 'can procreate' return True:
        #       Look for a place to allocate the newborn (there are many different ways of doing this)
        #       If the place is found:
        #           Create a new organism,
        #           The parent gives a fraction of its own reserves to the newborn. Different options:
        #               If it exist the gene 'energy reserve at birth' (or any other substance reserve at birth):
        #                   Decide the amount of reserve substances that the newborn will have
        #           The newborn do the action 'mutate'       
    'fertilize', 
        #   If the decision 'decide fertilize' returns True: 
        #       The organism gives its genetic information to another, in order to mix both
        #       genetic informations and produce the next generation
    'do internal changes', # This action updates gene values with 'value after cycle'
    'do photosynthesis', # This could be done as a part of the action 'do internal changes' or 'interchange substances with the biotope'
    'age', # This could be done as a part of the action 'do internal changes'
    'interchange substances with the biotope', # TODO
    'interchange substances with the other organisms', # TODO
    'mutate', # This action updates gene values with 'value after mutation'
    'stay alive', # (The main reason why this action exist is that it can be named in 'costs')
        #   If the constraint 'will die' returns true:
        #       Do the action 'die'
    'hunt', 
        #   Look for a possible prey (there are many different ways of doing this)
        #   If a possible prey is found:
        #       if the decision 'decide attack' returns true:
        #           Do the action 'attack'
    'attack',
        #   If the constraint 'can kill' returns true:
        #       Do the action 'eat'
        #       The prey do the action 'die'
    'defend',
        #   The constraint 'can kill' calls the action 'defend' (if it exist) and gives the 
        #   prey a chance of chosing the kind of defense it will perform (running away, build a shield)
        #   and deciding how much energy the prey will invest in order to defend itself
    'eat',
        #   For each substance reserve of the prey:
        #       If the predator has this substance reserve:
        #           The predator adds the substance reserve of the prey to its own one
    'die'
        #   The organism disappears. 
        #   Optionally, it can:
        #       a) Become a fossil with certain probability (for further researches)
        #       b) Add its reserves of substances to the biotope.
]

Actions_that_can_appear_in_actions_sequence = [
    'do internal changes'
    'do photosynthesis', # This could be done as a part of the action 'do internal changes' or 'interchange substances with the biotope'
    'stay alive',
    'move',
    'procreate',
    'fertilize',
    'hunt'
    'interchange substances with the biotope', # TODO
    'interchange substances with the other organisms', # TODO
    # 'age', mutate', attack', 'defend', 'eat' and 'die' are "secundary actions", called by other actions
]

Actions_that_have_to_appear_in_actions_sequence = [
    'do internal changes'
    'stay alive'
    # 'procreate' puede no aparecer. Por ejemplo, las hormigas obreras y las soldado son esteriles
]

Actions_that_can_appear_in_a_boolean_decision = [
    'decide move',
    'procreate',
    'fertilize', 
    'do photosynthesis', # This could be done as a part of the action 'do internal changes' or 'interchange substances with the biotope'
    'interchange substances with the biotope',
    'interchange substances with the other organisms',
    'hunt', 
    'attack',
    'eat'
]

Other_decisions = {
    'move decisions': [
        'decide move', 
        'in which direction to move',
        'how far to move',
        'how precise the movement is',
        'how exhaustive is the search for an empty place to move to'],
    'attack decisions': [
        'decide attack',
        'the amount of energy to invest in the attack',
        'the weapon to use for the attack'],
    'decide being fertilized': '', # Decide weather to accept or not the attempt of fertilization by other organism
    'decide grow': '' # The organism can decide spend energy and other substances in order to 
                      # improve its capacities
}

# EXPRESSIONS:

All_operators = [

    # BINARY / N-ARY OPERATORS:
    '+',
    '-',
    '*',
    '/',
    '**',
    '//',
    '%',
    'mod',

    # BOOLEAN OPERATORS:
    '>',
    '<',
    '>=',
    '<=',
    '==',
    '!=',
    'in',
    'and', 'AND', '&', '&&', # logical operator 'and'
    'or', 'OR', '|', '||', # logical operator 'or'
    'xor', 'XOR' # logical operator 'exclusive or'
    'not', # logical operator 'not'

    # UNARY OPERATORS:
    'abs',
    'minus',
    'sqrt',
    'log',
    'exp',
    'sigmoid',  #   e^x / (1 + e^x)
    'sin',
    'cos',
    'tan',
    'tg',
    'round',
    'int',
    'roundint',

    # RANDOM OPERATORS:
    'random integer', 'randint',  # random integer between given boundaries a and b
    'random boolean', 'randbool', 'random true', # returns True with a given probability, otherwise, False
    'uniform' # random value, uniform distribution in given interval [a, b]
    'gauss', # random value, normal distribution with given mean and variance
    'chi-squared', # random value, chi-squared distribution with given degree of freedom k
    'shuffle' # randomly shuffles a list
]

Unary_operators = [
    # Boolean:
    'not', # logical operator 'not'

    # Numeric:
    'abs',
    'minus',
    'sqrt',
    'log',
    'exp',
    'sigmoid',  #   e^x / (1 + e^x)
    'sin',
    'cos',
    'tan',
    'tg',
    'round',
    'int',
    'roundint',

    # Random:
    'random boolean', 'randbool', 'random true', # returns True with a given probability, otherwise, False
    'chi-squared'
]

Binary_operators = [
    # NUMERIC OPERATORS:
    '+',
    '-',
    '*',
    '/',
    '**',
    '//',
    '%',
    'mod',

    # BOOLEAN OPERATORS:
    '>',
    '<',
    '>=',
    '<=',
    '==',
    '!=',
    'in',
    'and', 'AND', '&', '&&', # logical operator 'and'
    'or', 'OR', '|', '||', # logical operator 'or'
    'xor', 'XOR' # logical operator 'exclusive or'

    # RANDOM OPERATORS:
    'random integer', 'randint',  # random integer between given boundaries a and b
    'random boolean', 'randbool', 'random true', # returns True with a given probability, otherwise, False
    'uniform' # random value, uniform distribution in given interval [a, b]
    'gauss' # random value, normal distribution with given mean and variance
]

Associative_operators = [
    '+',
    '*',
    'and', 'AND', '&', '&&', # logical operator 'and'
    'or', 'OR', '|', '||', # logical operator 'or'
    'xor', 'XOR' # logical operator 'exclusive or'
]

Operators_with_boolean_result = [
    'random boolean', 'randbool', 'random true', # returns True with a given probability, otherwise, False
    '>',
    '<',
    '>=',
    '<=',
    '==',
    '!=',
    'in',
    'and', 'AND', '&', '&&', # logical operator 'and'
    'or', 'OR', '|', '||', # logical operator 'or'
    'xor', 'XOR' # logical operator 'exclusive or'
    'not', # logical operator 'not'
]

Operators_with_numeric_result = [
    # BINARY / N-ARY OPERATORS:
    '+',
    '-',
    '*',
    '/',
    '**',
    '//',
    '%',
    'mod',

    # UNARY OPERATORS:
    'abs',
    'minus',
    'sqrt',
    'log',
    'exp',
    'sigmoid',  #   e^x / (1 + e^x)
    'sin',
    'cos',
    'tan',
    'tg',
    'round',
    'int',
    'roundint',

    # RANDOM OPERATORS:
    'random integer', 'randint',  # random integer between given boundaries a and b
    'uniform' # random value, uniform distribution in given interval [a, b]
    'gauss', # random value, normal distribution with given mean and variance
    'chi-squared', # random value, chi-squared distribution with given degree of freedom k
]

Operators_with_numeric_input = [
    # Unary:
    'abs',
    'minus',
    'sqrt',
    'log',
    'exp',
    'sigmoid',
    'sin',
    'cos',
    'tan',
    'tg',
    'round',
    'int',
    'roundint',
    'random boolean', 'randbool', 'random true',
    'chi-squared', # random value, chi-squared distribution with given degree of freedom k

    # Binary:
    '+',
    '-',
    '*',
    '/',
    '**',
    '//',
    '%',
    'mod',
    '>',
    '<',
    '>=',
    '<=',
    '==',
    '!=',
    'in',
    'and', 'AND', '&', '&&', # logical operator 'and'
    'or', 'OR', '|', '||', # logical operator 'or'
    'xor', 'XOR' # logical operator 'exclusive or'
    'random integer', 'randint',  # random integer between given boundaries a and b
    'uniform' # random value, uniform distribution in given interval [a, b]
    'gauss', # random value, normal distribution with given mean and variance
]

Operators_with_boolean_inputs = [
    'and', 'AND', '&', '&&', # logical operator 'and'
    'or', 'OR', '|', '||', # logical operator 'or'
    'xor', 'XOR' # logical operator 'exclusive or'
    'not', # logical operator 'not'
]

Operators_with_list_inputs = [
    'shuffle'
] + Associative_operators

Operators_with_inputs_of_many_types = [
    '!=',
    'in'
]


Expressions = [
    '<numeric value>',
    '<string value>',
    '<gene name>',
    {'<unary operator>': '<expression>'},
    {'<binary operator>': ('<expression>', '<expression>', '<expression>', '<etc...>')},
    {'choice': '<key expression>',
        '<value 1>': '<expression 1>',
        '<value 2>': '<expression 2>',
        '<value 3>': '<expression 3>',
        '<etc...>':  '<etc...>'
    },
    {'if': ('<boolean expression>', '<expression>', '<expression>', '<expression>')},
    {'tuple', ('item', 'item', 'etc...')},
    {'cost': '<action name>', 'substance': '<substance name>'},
    {'cost': '<action name>'},
    {'constraint': '<action name>'},
    {'function': ('<function>', '<expression>', '<expression>', '<etc...>')},
    {'discrete distribution':[
            {'value': '<expression>', 'probability': '<expression>'},
            {'value': '<expression>', 'probability': '<expression>'},
            {'etc..': '<expression>', 'probability': '<expression>'}]
    }
]

def default_error_messenger(error_text):
    print error_text

def check_operator_number_of_inputs(operator, expression, error_messenger = default_error_messenger):
    if not operator in All_operators:
        error_messenger("Unknown operator " + operator + " in " + str(expression))
        return False
    elif operator in Unary_operators:
        if is_iterable(expression[operator]):
            error_messenger("Syntax error. Error in number of arguments " + operator + " in " + str(expression))
            return False
        else:
            return True
    elif operator in Binary_operators and not operator in Associative_operators:
        if is_iterable(expression[operator]) and len(expression[operator]) == 2:
            return True
        else:
            error_messenger("Syntax error. Error in number of arguments " + operator + " in " + str(expression))
            return False
    elif operator in Associative_operators:
        if is_iterable(expression[operator]) and len(expression[operator]) > 1:
            return True
        else:
            error_messenger("Syntax error. Error in number of arguments " + operator + " in " + str(expression))
            return False
    return True

def is_boolean_expression(expression, error_messenger = default_error_messenger):
    if is_boolean(expression):
        return True
    elif is_string(expression):
        return True # If it's a string, it could be the name of a boolean gene
    elif is_dictionary(expression):
        (n_of_boolean, n_of_no_effect, n_of_unknown) = count_elements(expression, Operators_with_boolean_inputs, No_effect_attributes)
        if n_of_boolean != 1 or n_of_unknown > 0:
            error_messenger('Syntax error in ' + str(expression))
            return False
        for operator in expression:
            if operator in Operators_with_boolean_inputs
        return True                
    else:
        error_messenger('Not a boolean expression: ' + str(expression))
        False

def is_expression(expression, error_messenger = default_error_messenger):
    if is_number(expression):
        return True
    elif is_string(expression):
        return True
    elif is_dictionary(expression):
        if 'choice' in expression:
            for item in expression:
                if not is_expression(expression[item]):
                    error_messenger("'" + str(item) + "': <expression> expected in " + str(expression))
                    return False
            return True
        for instruction in expression:
            if instruction in All_operators:
                return evaluate_operator_expression(instruction, expression, error_messenger)
            elif instruction == 'if':
                param_list = expression[instruction]
                if (is_tuple_or_list(param_list) 
                    and len(param_list) == 3
                    and is_boolean_expression(param_list[0])
                    and is_expression(param_list[1])
                    and is_expression(param_list[2])):
                    return True
                else:
                    error_messenger('Syntax error in ' + str(expression))
                    return False
            elif instruction in ['cost', 'substance']:
                for item in expression:
                    if not item in ['cost', 'substance']:
                        error_messenger(str(item) + ' unexpected in ' + str(expression))
                        return False
                    if not is_string(expression[iten]):
                        error_messenger('<action name> or <substance name> expected in ' + str(expression) )
                        return False
                return True
            elif instruction == 'constraint':
                if is_string(expression[instruction]):
                    return True
                else:
                    error_messenger('<action name> expected in ' + str(expression))
                    return False
            elif instruction == 'function':
                if is_function(expression[instruction]):
                    return True
                elif is_tuple_or_list(expression[instruction]):
                    if (len(expression[instruction]) > 0) and 
                        is_function(expression[instruction][0]):
                        for item in expression[instruction][1:]:
                            if not is_expression(item):
                                return False
                        return True
                error_messenger(str(expression[instruction][0]) + ' Function expected in ' + str(expression) )
                return False
            elif instruction == 'discrete distribution':
                pairs_list = expression[instruction]
                if is_tuple_or_list(pairs_list):
                    for pair in pairs_list:
                        if not (
                            is_dictionary(pair)
                            and 'value' in pair
                            and is_expression(pair['value'])
                            and 'probability' in pair
                            and is_expression(pair['probability'])):
                            error_messenger('Syntax error in ' + str(expression))
                            return False
                    return True
                else:
                    error_messenger('Syntax error in ' + str(expression))
                    return False
            elif not instruction in No_effect_attributes:
                error_messenger('Unknown command ' + str(instruction) + ' in ' + str(expression))
                return False
    else:
        error_messenger('Syntax error in ' + str(expression))
        return False

def check_syntax(settings, syntax):

    if '$ ALLOWED ATTRIBUTES' in syntax:
        allowed = syntax['$ ALLOWED ATTRIBUTES']
    else:
        allowed = []
        
    if '$ MANDATORY ATTRIBUTES' in syntax:
        mandatory = syntax['$ MANDATORY ATTRIBUTES']
    else:
        mandatory = []
        
    if '$ NO-EFFECT ATTRIBUTES' in syntax:
        no_effect = syntax['$ NO-EFFECT ATTRIBUTES'] + No_effect_attributes
    else:
        no_effect = No_effect_attributes
        
    for item in mandatory:
        if not item in settings:
            return item + ' attribute missing'

    for item in settings:
        if not (allowed == []) and \
            not (item in allowed) and \
            not (item in mandatory) and \
            not (item in no_effect):
            return 'unknown attribute ' + item

    for item in settings:
        if item in syntax:
            result = check_syntax(settings[item], syntax[item])
            if result != 'OK':
                return result

    return 'OK'




def make_variation(gene, relative_variation = 0, absolute_variation = 0, probability_of_change = 1):
    if relative_variation == 0:
        new_value = gene
    else:
        new_value = {'*': (
            gene,
            {'+': (1, relative_variation)}
        )}
    if absolute_variation != 0:
        new_value = {'+': (new_value, absolute_variation)}
    if probability_of_change == 1:
        return new_value
    else:
        return {
            'if': (
                # condition:
                {'random true': probability_of_change},
                # then:
                new_value,
                # else:
                gene
            )
        }






# Abstract example:

ecosystem_settings = {
    'help': ''' This text is visible from GUI and from the settings generator''',
    'comment': ''' This text is visible from the settings generator ''',
    'label': ''' This text is for debuging purpose ''',
    'biotope': { 
        'size': '<expression>'
    },
    'organisms': {
        '<category name>': { # 'help': '''  ''', 'comment': '''  ''', 'label': '''  ''',
            'initial number of organisms': '<expression>',
            'genes': { # 'help': '''  ''', 'comment': '''  ''', 'label': '''  ''',
                '<gene name>': { # 'help': '''  ''', 'comment': '''  ''', 'label': '''  ''',
                    'initial value': '<expression>',
                    'value after cycle': '<expression>',
                    'value after mutation': '<expression>',
                    'allowed interval': '<expression>'
                }
                # '<another gene name>': { ... idem ... },
                # etc...
            },
            'decisions': { # 'help': '''  ''', 'comment': '''  ''', 'label': '''  ''',
                'decide <action name>': '<boolean expression>'
                # 'decide <another action name>': '<boolean expression>'
                # etc...
            }
        }
        # '<another category name>': { }
        # etc...
    },
    'constraints': { # 'help': '''  ''', 'comment': '''  ''', 'label': '''  ''',
        'can <action name> #<tag> #<tag> ...': '<boolean expression>',
        # if an organism 'can' do an action, it may do it or it may not. It's up to it.
        'will <action name>': '<boolean expression>' 
        # if an organism 'will' do an action, it'll do it. It can't avoid doing it.
    },
    'costs': {
        '<action name> #<tag> #<tag> ...': {
            '<substance name> reserve': '<expression>'
            # '<another substance name> reserve': '<expression>'
            # etc...
        }
        # '<another action name>': { },
        # etc...
    }
}



""" ******************************************************* """
"""                                                         """
"""                     E X A M P L E                       """
"""                                                         """
""" ******************************************************* """

_biotope = {
    'size': (100, 100)
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
            return gene_value * (1 + uniform(-0.05, 0.05)**3)
        else:
            return gene_value
    return {'function': (_value, gene, 'mutation_frequency')}

# genes
_gene_age_category_a = {
    'help': 
        """ 
            Age of organism (increase +1 every time cycle)
        """, 
    'initial value': 0,
    'value after time cycle': {
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
                probability_of_change = 'mutation_frequency'
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
        'aggressiveness': {
            'initial value': {
                'uniform': [0, 1]
            },
            'value after mutation': \
            _default_value_after_mutation_A('aggressiveness')
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
            'initial value': ['move',
                              'hunt',
                              'do internal changes',
                              'stay alive',
                              'procreate'],
            'value after mutation': {
                'if': ({'true with probability': 'mutation frequency'},
                       {'shuffle': 'actions sequence'})
            }
        }

    }
}

_decisions = {
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
    'move': _cost_move
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




