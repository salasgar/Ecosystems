from Basic_tools import *

No_effect_commands = ['help', 'comment', 'label']

"""
    'help': ''' This text is visible from GUI and from the settings generator''',
    'comment': ''' This text is visible from the settings generator ''',
    'label': ''' This text is for debuging purpose '''
"""

ecosystem_settings_syntaxis = {

    '$ ALLOWED COMMANDS': ['biotope', 'organisms', 'constraints', 'costs', 'help', 'comment', 'label'],
    '$ MANDATORY COMMANDS': ['biotope', 'organisms'],

    'biotope': { 

        '$ ALLOWED COMMANDS': ['size', 'help', 'comment', 'label'],
        '$ MANDATORY COMMANDS': ['size'],

        'size': '<expression>'
    },

    'organisms': {

        # All commands are allowed, because any string could be the name of a category

        '<category name>': { 

            '$ ALLOWED COMMANDS': ['initial number of organisms', 'genes', 'decisions', 'help', 'comment', 'label'],
            '$ MANDATORY COMMANDS': ['initial number of organisms', 'genes'],

            'initial number of organisms': '<expression>',

            'genes': {

                '$ MANDATORY COMMANDS': ['actions sequence'],
                # All commands are allowed, because any string could be the name of a gene

                '<gene name>': { 

                    '$ ALLOWED COMMANDS': ['initial value', 'value after cycle', 'value after mutation', 'allowed interval', 'help', 'comment', 'label'],
                    '$ MANDATORY COMMANDS': ['initial value'],

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


# EXPRESSIONS:

Operator_definition = {

    # BINARY / N-ARY OPERATORS:

    '+': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda x, y: x + y
    },

    '-': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda x, y: x - y
    },

    '*': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda x, y: x * y
    },

    '/': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda x, y: x / y
    },

    '**': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda x, y: x ** y
    },

    '//': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda x, y: x // y
    },

    '%': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda x, y: x % y
    },

    'mod': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda x, y: x % y
    },


    # BOOLEAN OPERATORS:

    '>': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Boolean',
        'output function': lambda x, y: x > y
    },

    '<': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Boolean',
        'output function': lambda x, y: x < y
    },

    '>=': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Boolean',
        'output function': lambda x, y: x >= y
    },

    '<=': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Boolean',
        'output function': lambda x, y: x <= y
    },

    '==': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Boolean',
        'output function': lambda x, y: x == y
    },

    '!=': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Any type',
        'type of output': 'Boolean',
        'output function': lambda x, y: x != y
    },

    'in': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Any type',
        'type of output': 'Boolean',
        'output function': lambda x, y: x in y
    },

    'and': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x, y: x and y
    },

    'AND': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x, y: x and y
    },

    '&': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x, y: x and y
    },

    '&&': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x, y: x and y
    },

    'or': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x, y: x or y
    },

    'OR': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x, y: x or y
    },

    '|': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x, y: x or y
    },

    '||': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x, y: x or y
    },

    'xor': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x, y: (x and not y) or (y and not x)
    },

    'XOR': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x, y: (x and not y) or (y and not x)
    },

    'not': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x: not x
    },

    'NOT': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x: not x
    },


# UNARY OPERATORS:

    'abs': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': abs
    },

    'minus': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda x: -x
    },

    'sqrt': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': sqrt
    },

    'log': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': log
    },

    'exp': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': exp
    },

    'sigmoid': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': sigmoid
    },

    'sin': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': sin
    },

    'cos': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': cos
    },

    'tan': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': tan
    },

    'tg': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': tan
    },

    'round': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda x: round(x, 0)
    },

    'int': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda x: int(x)
    },

    'roundint': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda x: int(round(x, 0))
    },


# RANDOM OPERATORS:

    'random integer': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': randint
    },

    'randint': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': randint
    },

    'random boolean': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Number',
        'type of output': 'Boolean',
        'output function': random_boolean
    },

    'randbool': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Number',
        'type of output': 'Boolean',
        'output function': random_boolean
    },

    'random true': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Number',
        'type of output': 'Boolean',
        'output function': random_boolean
    },

    'uniform': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': uniform
    },

    'gauss': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': gauss
    },

    'chi-squared': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': chi_squared
    },

    'shuffle': {
        'check number of inputs': lambda inputs: is_list(inputs),
        'type of inputs': 'List',
        'type of output': 'List',
        'output function': shuffle_function
    },

    # OTHER OPERATORS:

    'literal': {
        'check number of inputs': lambda inputs: True,
        'type of inputs': 'Any type',
        'type of output': 'Any type',
        'output function': lambda x: x
    },

    'choice': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and len(inputs) > 1,
        'type of inputs': 'Any type',
        'type of output': 'Any type',
        'output function': choice_function
    }

}


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
    'xor', 'XOR', # logical operator 'exclusive or'
    'not', 'NOT', # logical operator 'not'

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
    'uniform', # random value, uniform distribution in given interval [a, b]
    'gauss', # random value, normal distribution with given mean and variance
    'chi-squared', # random value, chi-squared distribution with given degree of freedom k
    'shuffle', # randomly shuffles a list

    # LITERAL:
    'literal', # Literal operator returns its input without evaluate it

    # CHOICE:
    'choice',
]

All_function_names = [
    'choice',
    'if',
    'tuple',
    'cost',
    'constraint',
    'function',
    'discrete distribution'
]

Auxiliar_commands = ['allowed interval', 'substance'] 
 # 'allowed interval' can be used in operators expressions
 # 'substance' can be used in 'cost' expressions

All_allowed_commands_in_expression = (
    All_operators 
    + All_function_names 
    + No_effect_commands 
    + Auxiliar_commands)

Unary_operators = [
    # Boolean:
    'not', 'NOT', # logical operator 'not'

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
    'xor', 'XOR', # logical operator 'exclusive or'

    # RANDOM OPERATORS:
    'random integer', 'randint',  # random integer between given boundaries a and b
    'random boolean', 'randbool', 'random true', # returns True with a given probability, otherwise, False
    'uniform', # random value, uniform distribution in given interval [a, b]
    'gauss' # random value, normal distribution with given mean and variance
]

Associative_operators = [
    '+',
    '*',
    'and', 'AND', '&', '&&', # logical operator 'and'
    'or', 'OR', '|', '||', # logical operator 'or'
    'xor', 'XOR', # logical operator 'exclusive or'
]

Operators_with_boolean_output = [
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
    'xor', 'XOR', # logical operator 'exclusive or'
    'not', 'NOT', # logical operator 'not'
]

Operators_with_numeric_output = [
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
    'uniform', # random value, uniform distribution in given interval [a, b]
    'gauss', # random value, normal distribution with given mean and variance
    'chi-squared', # random value, chi-squared distribution with given degree of freedom k
]

Operators_with_list_output = [
    'shuffle'
]

Operators_with_output_of_any_type = [
    'literal',
    'choice',
]

Operators_with_numeric_inputs = [
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
    'random integer', 'randint',  # random integer between given boundaries a and b
    'uniform', # random value, uniform distribution in given interval [a, b]
    'gauss', # random value, normal distribution with given mean and variance
]

Operators_with_boolean_inputs = [
    'and', 'AND', '&', '&&', # logical operator 'and'
    'or', 'OR', '|', '||', # logical operator 'or'
    'xor', 'XOR', # logical operator 'exclusive or'
    'not', 'NOT', # logical operator 'not'
]

Operators_with_list_inputs = [
    'shuffle'
] # do not put + Associative_operators here

Operators_with_inputs_of_any_type = [
    '!=',
    'in',
    'literal',
    'choice',
]

Commands_with_numeric_output = Operators_with_numeric_inputs + ['cost']

Commands_with_boolean_output = Operators_with_boolean_inputs + ['constraint']

Commands_with_list_output = Operators_with_list_inputs

Commands_with_string_output = [ # Commands that COULD have a string output
    'choice',
    'if',
    'function',
    'discrete distribution'
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
    {'if': ('<boolean expression>', '<expression>', '<expression>')},
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


# GENES, ACTIONS AND DECISIONS:

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

