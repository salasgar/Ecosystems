from SYNTAXIS import *
from Basic_tools import *
from Settings import *


def shuffle_function(list_object):
    shuffle(list_object)
    return list_object

Binary_operators_dictionary = {
    'op': lambda x, y: 'op(' + x + ', ' + y + ')', #formal operator for debugging purpose
    'op_': lambda x, y: '(' + x + ' op ' + y + ')', #formal operator for debugging purpose
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '**': lambda x, y: x ** y,
    '//': lambda x, y: x // y,
    '%': lambda x, y: x % y,
    'mod': lambda x, y: x % y,
    '>': lambda x, y: x > y,
    '<': lambda x, y: x < y,
    '>=': lambda x, y: x >= y,
    '<=': lambda x, y: x <= y,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
    'in': lambda x, y: x in y,
    'random integer': randint,  # random integer between x and y
    'randint': randint,  # random integer between x and y
    'gauss': gauss, # random value, normal distribution with mean x and variance y
    'uniform': uniform, # random value, uniform distribution in [x, y]
    
    # Logic operators:
    'and': lambda x, y: x and y,
    'AND': lambda x, y: x and y,
    '&': lambda x, y: x and y,
    '&&': lambda x, y: x and y,
    'or': lambda x, y: x or y,
    'OR': lambda x, y: x or y,
    '|': lambda x, y: x or y,
    '||': lambda x, y: x or y,
    'xor': lambda x, y: (x and not y) or (y and not x),
    'XOR': lambda x, y: (x and not y) or (y and not x)}

Unary_operators_dictionary = {
    'abs': abs,
    'sqrt': sqrt,
    'log': log,
    'exp': exp,
    'sigmoid': sigmoid,
    'sin': sin,
    'cos': cos,
    'tan': tan,
    'tg':  tan,
    'round': lambda x: round(x, 0),
    'int': lambda x: int(x),
    'roundint': lambda x: int(round(x, 0)),
    'random boolean': random_boolean,
    'randbool': random_boolean,
    'random true': random_boolean,
    'chi-squared': chi_squared, # random value, chi-squared distribution with given degree of freedom k
    'shuffle': shuffle_function,
    'not': lambda x: not x}


def get_tags(function_settings):
    return [tag, tag, tag,...]

def remove_tags(function_settings):
    return string_without_tags

def get_gene_value(organism, gene):
    if is_function(organism[gene]):
        return organism[gene](organism)
    else:
        return organism[gene]

def get_gene_value_or_string(organism, possible_gene):
    if possible_gene in organism:
        return get_gene_value(organism, possible_gene)
    else:
        return possible_gene

def evaluate_string(function_settings):
    tag_pos = find('#', function_settings)
    if tag_pos < 0:
        return lambda *arguments: get_gene_value_or_string(arguments, function_settings)

def make_function(function_settings):
    
    if is_number(function_settings):
        return lambda *arguments: function_settings
    elif is_string(function_settings):
        return evaluate_string(function_settings)
    elif hasattr(function_settings, '__iter__') and not is_dict(function_settings):
        terms = [make_function(item)
                 for item in function_settings]
        return lambda *arguments: [item(arguments) for item in terms]
    elif is_dict(function_settings):
        function_to_return = None

    if function_to_return == None:
        print "Hey, dude! We shouldn't be here!"
        #print_dictionary( function_settings )
        print function_settings
        error_maker = 1/0
        return lambda *arguments: 'Error: unknown function'

    if is_dict(function_settings) and 'allowed interval' in function_settings:
        interval_settings = function_settings['interval']
        if hasattr(interval_settings, '__iter__') and not is_dictionary(interval_settings):
            lower_bound = make_function(
                interval_settings[0])
            upper_bound = make_function(
                interval_settings[1])
        else:
            interval = make_function(interval_settings)
        bounded_value = lambda value, a, b: a if value < a else b if value > b else value
        if number_of_organisms == 0:
            return lambda *arguments: bounded_value(function_to_return(arguments), lower_bound(arguments), upper_bound(arguments))
    else:
        return function_to_return










