from Basic_tools import *

No_effect_commands = ['help', 'comment', 'label']

"""
    'help': ''' This text is visible from GUI and from the settings generator''',
    'comment': ''' This text is visible from the settings generator ''',
    'label': ''' This text is for debuging purpose '''
"""

ecosystem_settings_syntax = {

    '$ ALLOWED COMMANDS': ['biotope', 'organisms', 'constraints', 'costs', 'help', 'comment', 'label'],
    '$ MANDATORY COMMANDS': ['biotope', 'organisms'],

    'biotope': { 

        '$ ALLOWED COMMANDS': ['size', 'biotope features', 'help', 'comment', 'label'],
        '$ MANDATORY COMMANDS': ['size'],

        'size': '<expression>',

        'biotope features': {

            '<feature name or feature map name>': {

                '$ ALLOWED COMMANDS': [
                    'matrix size', 
                    'initial value #x #y', 
                    'initial value', 
                    'value after updating #x #y #time', 
                    'value after updating #time', 
                    'update once every', 
                    'help'
                ],

                # for a simple feature:
                'initial value': '<expression>',

                'value after updating #time': '<expression>',

                'update once every': '<expression>',

                # for a feature map:
                'matrix size': '<expression>',

                'initial value #x y#': '<expression>',

                'value after updating #x #y #time': '<expression>',

                'update once every': '<expression>'
            }
        }
    },

    'ecosystem features': {

            '<feature name>': {

                '$ ALLOWED COMMANDS': ['initial value', 'get new value #time', 'update once every', 'help', 'comment', 'label'],
                '$ MANDATORY COMMANDS': ['initial value'],

                'initial value': '<expression>',

                'value after updating #time': '<expression>',

                'update once every': '<expression>'
            }
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

                    '$ ALLOWED COMMANDS': ['initial value', 'value in next cycle', 'value after mutation', 'allowed interval', 'help', 'comment', 'label'],
                    '$ MANDATORY COMMANDS': ['initial value'],

                    'initial value': '<expression>',
                    'value in next cycle': '<expression>',
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

def output_function_of_choice(inputs):
    key_value = inputs[0]
    for pair in inputs[1:]:
        if pair[0] == key_value:
            return pair[1]
    return None

def check_inputs_of_discrete_distribution(inputs):
    if not is_tuple_or_list(inputs):
        return False
    total = 0
    for pair in inputs:
        if is_tuple_or_list(pair) and len(pair) == 2 and is_number(pair[1]):
            total += pair[1]
        else: 
            return False
    if total == 1:
        return True
    else:
        return False

def output_function_of_discrete_distribution(inputs):
    r = random()
    for (value, probability) in inputs:
        if r <= probability:
            return value
        else:
            r -= probability

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
        'output function': random_true
    },

    'randbool': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Number',
        'type of output': 'Boolean',
        'output function': random_true
    },

    'random true': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Number',
        'type of output': 'Boolean',
        'output function': random_true
    },

    'true with probability': {
        'check number of inputs': lambda inputs: not is_tuple_or_list(inputs),
        'type of inputs': 'Number',
        'type of output': 'Boolean',
        'output function': random_true
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

    #'literal': {      # This can't be an operator, because in this case inputs musn't be evaluated
    #    'check number of inputs': lambda inputs: True,
    #    'type of inputs': 'Any type',
    #    'type of output': 'Any type',
    #    'output function': lambda x: x
    #},

    'choice': {
        'check number of inputs': lambda inputs: is_tuple_or_list(inputs) and len(inputs) > 1,
        'type of inputs': 'Any type',
        'type of output': 'Any type',
        'output function': output_function_of_choice
    },

    'if': {
        'check inputs': lambda inputs: is_tuple_or_list(inputs) and len(inputs) == 3,
        'type of output': 'Any type',
        'output function': lambda condition, value_if_true, value_if_false: value_if_true if condition else value_if_false
    },

    'tuple': {
        'check inputs': lambda inputs, error_messenger: True,
        'type of output': 'Tuple',
        'output function': lambda inputs: tuple(inputs)
    },

    'function': {
        'check inputs': lambda inputs: 
            is_function(inputs) or (
                is_tuple_or_list(inputs) and 
                (len(inputs) > 1) and
                is_function(inputs[0])
            ),
        'type of output': 'Any type',
        'output function': lambda *inputs: inputs[0](*(inputs[1:]))
    },

    'discrete distribution': {
        'check inputs': check_inputs_of_discrete_distribution,
        'type of output': 'Any type',
        'output function': output_function_of_discrete_distribution
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
    'random boolean', 'randbool', 'random true', 'true with probability', # returns True with a given probability, otherwise, False
    'uniform', # random value, uniform distribution in given interval [a, b]
    'gauss', # random value, normal distribution with given mean and variance
    'chi-squared', # random value, chi-squared distribution with given degree of freedom k
    'shuffle', # randomly shuffles a list

    # LITERAL:
    'literal', # Literal operator returns its input without evaluate it

    # OTHER OPERATORS:
    'choice',
    'if',
    'tuple',
    'function',
    'discrete distribution'
]

Auxiliar_commands = ['allowed interval', 'substance'] 
 # 'allowed interval' can be used in all numeric operators expressions
 # 'substance' can be used in 'cost' expressions

Commands_that_comunicate_an_organism_with_the_environment = [
    'cost',
    'constraint',
    'feature value',
    'extract feature (percentage)',
    'extract feature',
    'normalized location x',
    'normalized location y',
    ]


All_allowed_commands_in_expression = (
    All_operators 
    + No_effect_commands 
    + Auxiliar_commands + ['cost', 'constraint', 'literal', 'infinity'])

All_allowed_commands = extract_from_dict('$ ALLOWED COMMANDS', ecosystem_settings_syntax) + All_allowed_commands_in_expression

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
    'random boolean', 'randbool', 'random true', 'true with probability', # returns True with a given probability, otherwise, False
    'chi-squared',

    # Others:
    'constraint',
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
    'uniform', # random value, uniform distribution in given interval [a, b]
    'gauss' # random value, normal distribution with given mean and variance
]

Ternary_operators = [
    'if'
]

Associative_operators = [
    '+',
    '*',
    'and', 'AND', '&', '&&', # logical operator 'and'
    'or', 'OR', '|', '||', # logical operator 'or'
    'xor', 'XOR', # logical operator 'exclusive or'
]

Operators_with_boolean_output = [
    'random boolean', 'randbool', 'random true', 'true with probability', # returns True with a given probability, otherwise, False
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
    'random boolean', 'randbool', 'random true', 'true with probability',
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

All_main_command_names = All_operators + ['cost', 'constraint', 'literal']


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

All_action_names = [
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


# *********************************************************************************
#                                   CHECK SYNTAX:
# *********************************************************************************

def default_error_messenger(*error_messages):
    for message in error_messages:
        print message

def check_settings_syntax(settings, syntax, all_gene_names, all_feature_names, error_messenger = default_error_messenger):

    if '$ ALLOWED COMMANDS' in syntax:
        allowed = syntax['$ ALLOWED COMMANDS']
    else:
        allowed = []
        
    if '$ MANDATORY COMMANDS' in syntax:
        mandatory = syntax['$ MANDATORY COMMANDS']
    else:
        mandatory = []
        
    if '$ NO-EFFECT COMMANDS' in syntax:
        no_effect = syntax['$ NO-EFFECT COMMANDS'] + No_effect_commands
    else:
        no_effect = No_effect_commands
        
    for item in mandatory:
        if not item in settings:
            error_messenger("Syntax error. Attribute missing:", item)
            return False

    for item in settings:
        if not (allowed == []) and \
            not (item in allowed) and \
            not (item in mandatory) and \
            not (item in no_effect):
            error_messenger('Syntax error. Unknown attribute', item)
            return False
        elif is_dict(syntax) and item in syntax:
            if syntax[item] == '<expression>' and not check_expression(settings[item], all_gene_names, all_feature_names, error_messenger):
                error_messenger('Error in expression', settings[item])
                return False
            elif syntax[item] == '<boolean expression>' and not (
                        check_expression(settings[item], all_gene_names, all_feature_names, error_messenger) and
                        check_type_of_expression('boolean', settings[item], all_gene_names, all_feature_names, error_messenger)
                    ):
                error_messenger('Error in boolean expression', settings[item])
                return False
            elif is_dict(syntax[item]) and not check_settings_syntax(settings[item], syntax[item], all_gene_names, all_feature_names):
                error_messenger('Syntax error in', settings)
                return False

    for syntax_item in syntax:
        if syntax_item[0] == "<" and syntax_item[-1] == ">":
            for settings_item in settings:
                if not settings_item in allowed + mandatory + no_effect and \
                    not check_settings_syntax(settings[settings_item], syntax[syntax_item], all_gene_names, all_feature_names):
                    return False
    
    if not check_gene_names(settings, all_gene_names, all_feature_names, error_messenger):
        return False
    else:
        return True


def main_command(expression, error_messenger):
    if is_dict(expression):
        for command in expression:
            if command in All_main_command_names: # not all commands can be the main command. For example 'allowed interval' of 'help' can't be main commands
                return command
    error_messenger('Syntax error. Command not found in', expression)
    return None

def check_type_of_expression(type_to_check, expression, all_gene_names, all_feature_names, error_messenger):
    if type_to_check == 'Any type':
        return True
    elif (
        (type_to_check == 'Number' and is_number(expression)) or
        (type_to_check == 'Boolean' and is_boolean(expression)) or
        (type_to_check == 'List' and is_tuple_or_list(expression)) or
        (type_to_check == 'Function' and is_function(expression)) or  # 'Function', but not 'String'
        (type_to_check == 'String' and is_string(expression)) or
        (is_string(expression) and expression in all_gene_names) or # A string could be the name of a gene of any type
        (is_string(expression) and expression in all_feature_names) # A string could be the name of a feature
        ): 
        return True
    elif is_string(expression) and not (
        expression in all_gene_names or
        expression in all_feature_names or
        expression in All_action_names or
        expression in All_allowed_commands
        ):
        error_messenger(expression, 'is not a fucking gene name')
        return False
    elif is_dict(expression):
        if not check_expression(expression, all_gene_names, all_feature_names, error_messenger):
            return False
        command = main_command(expression, error_messenger)
        if (
            (type_to_check == "Number" and command in Operators_with_numeric_output) or
            (type_to_check == "Boolean" and command in Operators_with_boolean_output) or
            (type_to_check == "List" and command in Operators_with_list_output) or
            (type_to_check == "String" and command in Operators_with_string_output)): # 'String', but not 'Function'
            return True
    error_messenger("Syntax error. ", command, "doesn't return a", type_to_check)
    return False

def check_operator_input_types(operator, expression, all_gene_names, all_feature_names, error_messenger):
    inputs = expression[operator]
    if 'check inputs' in Operator_definition[operator]:
        if not Operator_definition[operator]['check inputs'](inputs):
            error_messenger("Syntax error in operator", operator, "Inputs:", inputs)
            return False
        else:
            return True
    elif 'type of inputs' in Operator_definition[operator]:        
        input_type = Operator_definition[operator]['type of inputs']
    else:
        error_messenger("Error in operator definition:", operator, Operator_definition[operator])
        error_maker = 1/0
    if operator == 'in':
        return (
            is_tuple_or_list(inputs) and 
            (len(inputs) == 2) and 
            check_type_of_expression('List', inputs[1], all_gene_names, all_feature_names, error_messenger))
    elif input_type == 'Any type':
        return True
    elif is_tuple_or_list(inputs):
        for item in inputs:
            if not check_type_of_expression(input_type, item, all_gene_names, all_feature_names, error_messenger):
                error_messenger('Type error in', expression)
                error_messenger(input_type, 'expected')
                return False
    else:   
        if not check_type_of_expression(input_type, inputs, all_gene_names, all_feature_names, error_messenger):
            error_messenger('Type error in', expression)
            error_messenger(input_type, 'expected')
            return False
    return True


def check_operator_expression(operator, expression, all_gene_names, all_feature_names, error_messenger):
    inputs = expression[operator]
    if 'check inputs' in Operator_definition[operator]:
        if not Operator_definition[operator]['check inputs'](inputs):
            error_messenger("Syntax error in operator", operator, "Inputs:", inputs)
            return False
    if 'check number of inputs' in Operator_definition[operator]:
        if not Operator_definition[operator]['check number of inputs'](inputs):
            error_messenger("Syntax error in operator", operator, "Incorrect number of inputs in:", inputs)
            return False
    if not check_operator_input_types(operator, expression, all_gene_names, all_feature_names, error_messenger):
        error_messenger("Syntax error in operator", operator, "Incorrect type of inputs in:", inputs)
        return False
    if 'allowed interval' in expression:
        interval = expression['allowed interval']
        if not (
            is_tuple_or_list(interval) and 
            (len(interval) == 2) and
            check_type_of_expression('Number', interval[0], all_gene_names, all_feature_names, error_messenger) and
            check_type_of_expression('Number', interval[1], all_gene_names, all_feature_names, error_messenger)):
            error_messenger('Error in interval', interval, 'defined in', expression)
            return False
    if operator == 'choice':
        if not ( # Conditions that "inputs" has to match:
            is_tuple_or_list(inputs) and 
            len(inputs) >= 3 and 
            check_expression(inputs, all_gene_names, all_feature_names, error_messenger)
        ):
            error_messenger('Syntax error in', expression)
            return False
        input_type = get_type_of_expression(inputs[0], error_messenger)
        for item in inputs[1:]:
            if not ( # Conditions that "item" has to match:
                is_tuple_or_list(item) and 
                len(item) == 2 and
                check_type_of_expression(input_type, item, all_gene_names, all_feature_names, error_messenger)
            ):
                error_messenger('Syntax error in', item)
                error_messenger('Syntax error in', expression)
                return False
    for instruction in expression:
        if not instruction in [operator, 'allowed interval'] + No_effect_commands:
            error_messenger('Syntax error. Unexpected command', instruction, 'in', expression)
            return False
    return True

def check_commands_in_expression(expression, error_messenger):
    count = count_elements(
        expression, 
        No_effect_commands, 
        Auxiliar_commands, 
        All_allowed_commands_in_expression)
    
    (n_No_effect_commands, n_Auxiliar_commands, n_All_allowed_commands, n_Unknown_commands) = count

    if n_Unknown_commands > 0:
        error_messenger('Syntax error. Unexpected command in', expression)
        return False
    elif n_All_allowed_commands - n_Auxiliar_commands - n_No_effect_commands != 1:
        error_messenger('Error in number of commands in', expression)
        return False
    elif n_Auxiliar_commands > 1:
        error_messenger('Error in number of commands in', expression)
        return False
    else:
        return True

def get_type_of_expression(expression, error_messenger):
    if not check_expression(expression, error_messenger):
        return 'Error in expression'
    elif is_number(expression):
        return 'Number'
    elif is_boolean(expression):
        return 'Boolean'
    elif is_tuple_or_list(expression):
        return 'List'
    elif is_string(expression):
        return 'Any type' # It could be the name of a gene of any type
    elif is_function(expression):
        return 'Function'
    elif is_dict(expression):
        command = main_command(expression)
        if command in Commands_with_numeric_output:
            return 'Number'
        elif command in Commands_with_boolean_output:
            return 'Boolean'
        elif command in Commands_with_list_output:
            return 'List'
        else:
            return 'Any type'

def check_function_expression(command, expression, all_gene_names, all_feature_names, error_messenger):
    inputs = expression[command]
    if not check_expression(inputs, all_gene_names, all_feature_names, error_messenger):
        error_messenger('Syntax error in', expression)
        return False

    elif command == 'if':
        if (is_tuple_or_list(inputs) 
            and len(inputs) == 3
            and check_type_of_expression('Boolean', inputs[0], error_messenger)
            and check_expression(inputs[1], all_gene_names, all_feature_names, error_messenger)
            and check_expression(inputs[2], all_gene_names, all_feature_names, error_messenger)):
            return True
        else:
            error_messenger('Syntax error in', expression)
            return False

    elif command in ['cost', 'constraint']:
        if not check_type_of_expression('String', inputs, all_gene_names, all_feature_names, error_messenger):
            error_messenger('Action name expected in', inputs)
            error_messenger('Syntax error in', expression)
            return False
        if 'substance' in expression and not check_type_of_expression('String', expression['substance'], all_gene_names, all_feature_names, error_messenger):
            error_messenger('Substance name expected in', expression['substance'])
            error_messenger('Syntax error in', expression)
            return False

    elif command == 'function':
        if is_function(inputs):
                    return True
        elif (check_expression(inputs, all_gene_names, all_feature_names, error_messenger) and 
            is_tuple_or_list(inputs) and
            (len(inputs) > 0) and 
            is_function(inputs[0])):
                return True
        else:
            error_messenger('Syntax error. Function expected in', expression)
            return False

    elif command == 'discrete distribution':
        if not (
            is_tuple_or_list(inputs) and 
            check_expression(inputs, all_gene_names, all_feature_names, error_messenger)
        ):
            error_messenger('Syntax error in', expression)
            return False
        for pair in inputs:
            if not (
                is_dict(pair)
                and 'value' in pair
                and check_expression(pair['value'], all_gene_names, all_feature_names, error_messenger)
                and 'probability' in pair
                and check_type_of_expression('Number', pair['probability'], all_gene_names, all_feature_names, error_messenger)
            ):
                error_messenger('Syntax error in', expression)
                return False
        return True

    else:
        error_messenger('Syntax error. Unknown command', command, 'in', expression)

def check_names(expression, all_gene_names, all_feature_names, error_messenger):
    if is_string(expression):
        if len(expression) > 0 and expression[0] == '#': # Example: '#predator attack capacity'
            return True
        name = remove_tags(expression)
        if (
            name in all_gene_names or 
            name in all_feature_names or
            name in All_action_names or
            name in All_allowed_commands
            ):
            return True
        else:
            error_messenger(expression, 'is not a gene name nor a shit', name)
            return False
    elif is_dict(expression):
        for item in expression:
            if (
                not item in No_effect_commands
                and not check_names(expression[item], all_gene_names, all_feature_names, error_messenger)
                ):
                return False
        return True
    if is_iterable(expression): # Do not use "elif" here in steed of "if" !!!
        for item in expression:
            if not check_names(item, all_gene_names, all_feature_names, error_messenger):
                return False
        return True
    else:
        return True


def check_expression(expression, all_gene_names, all_feature_names, error_messenger = default_error_messenger):
    if not check_names(expression, all_gene_names, all_feature_names, error_messenger):
        return False
    elif is_number(expression) or is_boolean(expression):
        return True
    elif is_string(expression):
        if not expression in all_gene_names and expression != 'infinity':
            error_messenger('Warning. Not a gene name:', expression) # It could be a string value or a misspelled gene name
        return True
    elif is_tuple_or_list(expression):
        for item in expression:
            if not check_expression(item, all_gene_names, all_feature_names, error_messenger):
                error_messenger('Syntax error in', expression)
                return False
        return True
    elif is_dict(expression):
        if not check_commands_in_expression(expression, error_messenger):
            return False
        command = main_command(expression, error_messenger)
        if command in All_operators:
            return check_operator_expression(command, expression, all_gene_names, all_feature_names, error_messenger)
        else:
            return check_function_expression(command, expression, all_gene_names, all_feature_names, error_messenger)
    else:
        error_messenger('Syntax error in', expression)
        return False


"""
expression = {
    'mod': [4]
}
print check_operator_expression('mod', expression)


"""




































