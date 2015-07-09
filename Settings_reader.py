from SYNTAX import *
from Basic_tools import *
from Settings import *



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
    'minus': lambda x: -x,
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


def get_gene_value(organism, gene):
    if is_function(organism[gene]):
        return organism[gene](organism)
    else:
        return organism[gene]

def get_gene_value_or_string(organism, possible_gene):
    if possible_gene in organism:
        # if it's a gene:
        return get_gene_value(organism, possible_gene)
    else:
        # if it's not a gene, then it's a string value:
        return possible_gene

def evaluate_string(function_settings, tags_list):
    if function_settings in tags_list:
        tag_position = tags_list.index(function_settings)
        return lambda *arguments: arguments[tag_position]
    else:
        hash_position = function_settings.find('#')
        if hash_position == 0:
            # it's an expression like '#prey defense capacity'
            length = function_settings.find(' ')
            tag = function_settings[:length]
            if tag in tags_list:
                tag_position = tags_list.index(tag)
            else:
                error_maker = 1/0
                return 'Syntax error'
            gene_name = function_settings[length+1:]
            return lambda *arguments: get_gene_value_or_string(arguments[tag_position], gene_name)
        elif hash_position == -1:
            return lambda *arguments: \
                get_gene_value_or_string(arguments[0], function_settings) if is_tuple(arguments) \
                else get_gene_value_or_string(arguments, function_settings)
        else:
            error_maker = 1/0
            return 'Syntax error'

def evaluate_built_function(function_settings, tags_list):
    function_and_parameters = function_settings['function']
    if is_tuple_or_list(function_and_parameters) and len(function_and_parameters) > 0:
        function = function_and_parameters[0]
        if is_function(function):
            parameters = [make_function(item, tags_list) for item in function_and_parameters[1:]]
            return lambda *arguments: function(*[item(*arguments) for item in parameters])
        else:
            "Error"
            error_maker = 1/0
    elif is_function(function_and_parameters):
        return lambda *arguments: function_and_parameters() # Call without arguments

def apply_associative_operator(main_operation, inputs):
    return reduce(main_operation, inputs[1:], inputs[0])

def evaluate_dict(function_settings, tags_list, error_messenger):

    command = main_command(function_settings, error_messenger)
    inputs = function_settings[command]

    if command == 'literal':
        return lambda *arguments: inputs # 'literal' operator returns its input without evaluate it
    elif command in All_operators:
        inputs_function = make_function(inputs, tags_list, error_messenger)
        main_operation = Operator_definition[command]['output function']
        if command in Associative_operators:          
            return lambda *arguments: apply_associative_operator(main_operation, inputs_function(*arguments))
        else:
            return lambda *arguments: main_operation(inputs_function(*arguments))
    
    elif command == 'if':
        (condition, value_if_true, value_if_false) = \
            [make_function(item, tags_list, error_messenger) for item in function_settings['if']]
        return lambda *arguments: \
            value_if_true(*arguments) \
            if condition(*arguments) \
            else value_if_false(*arguments)
    
    elif 'function' in function_settings:
        return evaluate_built_function(function_settings, tags_list)
    elif 'discrete distribution' in function_settings:
        def choice_value(values_list, r, *arguments):
            i = 0
            while (i < len(values_list) - 1) and (r > values_list[i][0](*arguments)):
                i += 1
                r -= values_list[i][0](*arguments)
            return values_list[i][1](*arguments)
        values_list = [(make_function(pair['probability'], tags_list), make_function(
            pair['value'], tags_list)) for pair in function_settings['discrete distribution']]
        return lambda *arguments: choice_value(values_list, random(), *arguments)

    print "Hey, dude! We shouldn't be here!"
    #print_dictionary( function_settings )
    print function_settings
    error_maker = 1/0

def constrain_function_to_allowed_interval(function_to_return, interval_settings):
    if hasattr(interval_settings, '__iter__') and not is_dictionary(interval_settings):
        lower_bound = make_function(
            interval_settings[0], tags_list)
        upper_bound = make_function(
            interval_settings[1], tags_list)
    else:
        interval = make_function(interval_settings, tags_list)
    bounded_value = lambda value, a, b: a if value < a else b if value > b else value
    if number_of_organisms == 0:
        return lambda *arguments: bounded_value(
            function_to_return(*arguments), 
            lower_bound(*arguments), 
            upper_bound(*arguments))

def make_function(function_settings, tags_list):
    
    if is_number(function_settings):
        return lambda *arguments: function_settings
    elif is_string(function_settings):
        return evaluate_string(function_settings, tags_list)
    elif is_tuple_or_list(function_settings):
        terms = [make_function(item, tags_list)
                 for item in function_settings]
        return lambda *arguments: [item(*arguments) for item in terms] # This is necessary for 'shuffle' operator
    elif is_dict(function_settings):
        function_to_return = evaluate_dict(function_settings, tags_list)
        if 'allowed interval' in function_settings:
            return constrain_function_to_allowed_interval(
                function_to_return, 
                function_settings['allowed interval'])
        else:
            return function_to_return

def get_tags_list(function_name):
    tags_list = []
    end_position = 0
    keep_looping = True
    while keep_looping:
        hash_position = function_name.find('#', end_position)
        if hash_position > -1:
            end_position = function_name.find(' ', hash_position)
            if end_position > -1:
                tags_list.append(function_name[hash_position: end_position])
            else:
                tags_list.append(function_name[hash_position:])                
        else:
            keep_looping = False
    return tags_list

def remove_tags(function_name):
    hash_position = function_name.find('#')
    if hash_position < 0:
        return function_name
    else:
        while (hash_position > 0) and (function_name[hash_position - 1] == ' '):
            hash_position -= 1
        return function_name[:hash_position]

def read_function_settings(function_name, function_settings):
    return make_function(function_settings, get_tags_list(function_name))



