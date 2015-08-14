from Basic_tools import *

No_effect_directives = ['help', 'comment', 'label']

ecosystem_settings_syntax = {

    '$ ALLOWED DIRECTIVES': [
        'new operators',
        'biotope',
        'ecosystem features',
        'organisms',
        'constraints',
        'costs'
    ],

    '$ MANDATORY DIRECTIVES': ['biotope', 'organisms'],

    'new operators': {
        '<operator name>': {
            '$ ALLOWED DIRECTIVES': [
                'is associative',
                'check inputs'
                'chec number of inputs',
                'type of inputs',
                'type of outputs',
                'output function [#<tag name>, #<tag name>, ...]'
            ]
        }
    },

    'biotope': {

        '$ ALLOWED DIRECTIVES': [
            'size',
            'biotope features'
        ],

        '$ MANDATORY DIRECTIVES': ['size'],

        'size': '<expression>',

        'biotope features': {

            '<feature name or feature map name>': {

                '$ ALLOWED DIRECTIVES': [
                    'matrix size',
                    'initial value #x #y',  # for a feature map
                    'initial value',  # for a simple feature
                    'value after updating #x #y',  # for a feature map
                    'value after updating',  # for a simple feature
                    'update once every'
                ]
            }
        }
    },

    'ecosystem features': {

            '<feature name>': {

                '$ ALLOWED DIRECTIVES': [
                    'matrix size',
                    'initial value',
                    'value after updating',
                    'update once every'
                ],

                '$ MANDATORY DIRECTIVES': ['initial value'],

                'initial value': '<expression>',

                'value after updating #time': '<expression>',

                'update once every': '<expression>'
            }
        },

    'organisms': {

        '<category name>': {

            '$ ALLOWED DIRECTIVES': [
                'initial number of organisms',
                'genes',
                'decisions'
            ],

            '$ MANDATORY DIRECTIVES': [
                'initial number of organisms',
                'genes'
            ],

            'genes': {

                '$ MANDATORY DIRECTIVES': ['actions sequence'],

                '<gene name>': {

                    '$ ALLOWED DIRECTIVES': [
                        'initial value',
                        'value in next cycle',
                        'value after mutation',
                        'allowed interval',
                        'offer to sell'
                        ],

                    '$ MANDATORY DIRECTIVES': ['initial value'],

                    'offer to sell': {
                        '$ ALLOWED DIRECTIVES': [
                            'amount',
                            'prices'
                        ],

                        '$ MANDATORY DIRECTIVES': [
                            'amount',
                            'prices'
                        ],

                        'prices': {}
                    }
                }
            },

            'decisions': {}
        }
    },

    'constraints': {

        'can <action name> #<tag> #<tag> ...': '<boolean expression>',
        # if an organism 'can' do an action, it may do it or it may not.
        # It's up to it.
        'will <action name>': '<boolean expression>'
        # if an organism 'will' do an action, it'll do it. It can't avoid
        # doing it.
    },

    'costs': {

        '<action name> #<tag> #<tag> ...': {
            '<substance name> reserve': '<expression>'
        }
    }
}


def output_function_of_choice(*inputs):
    key_value = inputs[0]
    for pair in inputs[1:]:
        if pair[0] == key_value:
            return pair[1]
    return None


def check_inputs_of_discrete_distribution(*inputs):
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


def output_function_of_discrete_distribution(*inputs):
    r = random()
    for (value, probability) in inputs:
        if r <= probability:
            return value
        else:
            r -= probability

# EXPRESSIONS:

Operators_definitions = {

    # BINARY / N-ARY OPERATORS:

    '+': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (en(inputs) > 1),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda x, y: x + y
    },

    '-': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda x, y: x - y
    },

    '*': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda x, y: x * y
        # if default_error_messenger(x, y) else x * y # ***
    },

    '/': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda x, y: x / y
    },

    '**': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda x, y: x ** y
    },

    '//': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda x, y: x // y
    },

    '%': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda x, y: x % y
    },

    'mod': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda x, y: x % y
    },

    'min': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) > 2),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda *inputs: min(*inputs)
    },

    'max': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) > 2),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': lambda *inputs: max(*inputs)
    },

    # BOOLEAN OPERATORS:

    '>': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Boolean',
        'output function': lambda x, y: x > y
    },

    '<': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Boolean',
        'output function': lambda x, y: x < y
    },

    '>=': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Boolean',
        'output function': lambda x, y: x >= y
    },

    '<=': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Boolean',
        'output function': lambda x, y: x <= y
    },

    '==': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Boolean',
        'output function': lambda x, y: x == y
    },

    '!=': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Any type',
        'type of output': 'Boolean',
        'output function': lambda x, y: x != y
    },

    'in': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Any type',
        'type of output': 'Boolean',
        'output function': lambda x, y: x in y
    },

    'and': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x, y: x and y
    },

    'AND': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x, y: x and y
    },

    '&': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x, y: x and y
    },

    '&&': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x, y: x and y
    },

    'or': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x, y: x or y
    },

    'OR': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x, y: x or y
    },

    '|': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x, y: x or y
    },

    '||': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x, y: x or y
    },

    'xor': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x, y: (x and not y) or (y and not x)
    },

    'XOR': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) > 1),
        'type of inputs': 'Boolean',
        'type of output': 'Boolean',
        'output function': lambda x, y: (x and not y) or (y and not x)
    },

    # UNARY OPERATORS:

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
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': randint
    },

    'randint': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 2),
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
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 2),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': uniform
    },

    'gauss': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 2),
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

    'triangular': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 3),
        'type of inputs': 'Number',
        'type of output': 'Number',
        'output function': triangular
    },

    'shuffle': {
        'check number of inputs': lambda inputs: is_list(inputs),
        'type of inputs': 'List',
        'type of output': 'List',
        'output function': shuffle_function
    },

    # OTHER OPERATORS:

    # 'literal': {      # This can't be an operator, because in this
    #                   # case inputs musn't be evaluated
    #    'check number of inputs': lambda inputs: True,
    #    'type of inputs': 'Any type',
    #    'type of output': 'Any type',
    #    'output function': lambda x: x
    # },

    'choice': {
        'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and len(inputs) > 1,
        'type of inputs': 'Any type',
        'type of output': 'Any type',
        'output function': output_function_of_choice
    },

    'if': {
        'check inputs': lambda inputs:
            is_tuple_or_list(inputs) and len(inputs) == 3,
        'type of output': 'Any type',
        'output function': lambda condition, value_if_true, value_if_false:
            value_if_true if condition else value_if_false
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
        # if default_error_messenger(inputs) else 0
    },

    'discrete distribution': {
        'check inputs': check_inputs_of_discrete_distribution,
        'type of output': 'Any type',
        'output function': output_function_of_discrete_distribution
    }

}


All_operator_names = [

    # BINARY / N-ARY OPERATORS:
    '+',
    '-',
    '*',
    '/',
    '**',
    '//',
    '%',
    'mod',
    'max',
    'min',

    # BOOLEAN OPERATORS:
    '>',
    '<',
    '>=',
    '<=',
    '==',
    '!=',
    'in',
    'and', 'AND', '&', '&&',  # logical operator 'and'
    'or', 'OR', '|', '||',  # logical operator 'or'
    'xor', 'XOR',  # logical operator 'exclusive or'
    'not', 'NOT',  # logical operator 'not'

    # UNARY OPERATORS:
    'abs',
    'minus',
    'sqrt',
    'log',
    'exp',
    'sigmoid',  # e^x / (1 + e^x)
    'sin',
    'cos',
    'tan',
    'tg',
    'round',
    'int',
    'roundint',

    # RANDOM OPERATORS:
    # random integer between given boundaries a and b:
    'random integer', 'randint',
    # returns True with a given probability, otherwise, False:
    'random boolean', 'randbool', 'random true', 'true with probability',
    # random value, uniform distribution in given interval [a, b]:
    'uniform',
    # random value, normal distribution with given mean and variance:
    'gauss',
    # random value, chi-squared distribution with given degree f freedom k:
    'chi-squared',
    # random value, triangular distribution with given lower and upper bounds
    # and mode:
    'triangular',
    # randomly shuffles a list:
    'shuffle',

    # LITERAL:
    # If 'literal' was an operator, it'd return its input without evaluating it
    # But we can't treat it as an operator because we always evaluate
    # operator's inputs:
    # 'literal',

    # OTHER OPERATORS:
    'choice',
    'if',
    'tuple',
    'function',
    'discrete distribution'
]

Auxiliar_directives = ['allowed interval', 'substance']
# 'allowed interval' can be used in all numeric operators expressions
# 'substance' can be used in 'cost' expressions

Directives_that_comunicate_an_organism_with_its_environment = [
    'cost',
    'constraint',
    'extract feature (percentage)',
    'extract feature',
    'normalized location x',
    'normalized location y'
    ]

All_allowed_directives_in_expression = (
    All_operator_names
    + No_effect_directives
    + Auxiliar_directives
    + Directives_that_comunicate_an_organism_with_its_environment
    + ['literal', 'infinity'])

All_allowed_directives = \
    extract_from_dict(
        '$ ALLOWED DIRECTIVES',
        ecosystem_settings_syntax
    ) + \
    All_allowed_directives_in_expression

Unary_operators = [
    # Boolean:
    'not', 'NOT',  # logical operator 'not'

    # Numeric:
    'abs',
    'minus',
    'sqrt',
    'log',
    'exp',
    'sigmoid',  # e^x / (1 + e^x)
    'sin',
    'cos',
    'tan',
    'tg',
    'round',
    'int',
    'roundint',

    # Random:
    'random boolean', 'randbool', 'random true', 'true with probability',
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
    'min',
    'max',  # 'min' and 'max' can be binary, ternary, etc...

    # BOOLEAN OPERATORS:
    '>',
    '<',
    '>=',
    '<=',
    '==',
    '!=',
    'in',
    'and', 'AND', '&', '&&',
    'or', 'OR', '|', '||',
    'xor', 'XOR',

    # RANDOM OPERATORS:
    'random integer', 'randint',
    'uniform',
    'gauss'
]

Ternary_operators = [
    'if',
    'min',
    'max'  # 'max' can be binary, ternary, etc...
]

Associative_operators = [
    '+',
    '*',
    'and', 'AND', '&', '&&',
    'or', 'OR', '|', '||',
    'xor', 'XOR',
    # despite 'max' is associative, we don't need to calculate it this way
]

Operators_with_boolean_output = [
    'random boolean', 'randbool', 'random true', 'true with probability',
    '>',
    '<',
    '>=',
    '<=',
    '==',
    '!=',
    'in',
    'and', 'AND', '&', '&&',
    'or', 'OR', '|', '||',
    'xor', 'XOR',
    'not', 'NOT',
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
    'min',
    'max',

    # UNARY OPERATORS:
    'abs',
    'minus',
    'sqrt',
    'log',
    'exp',
    'sigmoid',  # e^x / (1 + e^x)
    'sin',
    'cos',
    'tan',
    'tg',
    'round',
    'int',
    'roundint',

    # RANDOM OPERATORS:
    'random integer', 'randint',
    'uniform',
    'gauss',
    'chi-squared',
]

Operators_with_list_output = [
    'shuffle'
]

Operators_with_output_of_any_type = [
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
    'chi-squared',

    # Binary:
    '+',
    '-',
    '*',
    '/',
    '**',
    '//',
    '%',
    'mod',
    'min',
    'max',
    '>',
    '<',
    '>=',
    '<=',
    '==',
    '!=',
    'random integer', 'randint',
    'uniform',
    'gauss',
]

Operators_with_boolean_inputs = [
    'and', 'AND', '&', '&&',
    'or', 'OR', '|', '||',
    'xor', 'XOR',
    'not', 'NOT',
]

Operators_with_list_inputs = [
    'shuffle',
    'min',
    'max'  # 'max' can be binary, ternary, etc...
]  # do not put + Associative_operators here

Operators_with_inputs_of_any_type = [
    '!=',
    'in',
    'choice',
]

Directives_with_numeric_output = Operators_with_numeric_inputs + ['cost']

Directives_with_boolean_output = Operators_with_boolean_inputs + ['constraint']

Directives_with_list_output = Operators_with_list_inputs

Directives_with_string_output = [  # Directives that COULD have a string output
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
    {'<binary operator>': ('<expression>', '<expression>', '<etc...>')},
    {
        'choice': '<key expression>',
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
    {'discrete distribution': [
        {'value': '<expression>', 'probability': '<expression>'},
        {'value': '<expression>', 'probability': '<expression>'},
        {'etc..': '<expression>', 'probability': '<expression>'}
    ]
    }
]


# GENES, ACTIONS AND DECISIONS:

Gene_names = [
    # Indicates the actions it will perform and in which order:
    'actions sequence',
    # It stores a certain amount of substance:
    '<substance name> reserve',
    # Indicates the maximum amount of this substance that the organism can
    # store:
    '<substance name> storage capacity',
    # Indicates the amount of substance reserve at birth:
    '<substance name> reserve at birth',
    # An example of next case:
    # 'energy reserve threshold to move' indicates that the organism will
    # decide to move only if its 'energy reserve' is greater than its
    # 'energy reserve threshold to move':
    '<substance name> reserve threshold to <action name>',
    # radius of procreation, of hunt, of searching for predators to run away
    # from, of looking for other organisms to trade with, etc...
    'radius of <action name>',
    '<action name>ing frequency'
]

All_action_names = [
    'move',
        #  If the decision 'decide move' returns True:
        #       Look for a place to go (there are many different ways of doing
        #       this)
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
    'stay alive',
    'move',
    'procreate',
    'fertilize',
    'hunt'
    'interchange substances with the other organisms',
    # 'age', mutate', attack', 'defend', 'eat' and 'die' are "secundary
    # actions", called by other actions
]

Actions_that_have_to_appear_in_actions_sequence = [
    'do internal changes'
    'stay alive'
]

Actions_that_can_appear_in_a_boolean_decision = [
    'decide move',
    'procreate',
    'fertilize',
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
    # Decide weather to accept or not the attempt of fertilization by other
    # organism:
    'decide being fertilized': '',
    # The organism can decide spend energy and other substances in order to
    # improve its capacities
    'decide grow': ''
}


