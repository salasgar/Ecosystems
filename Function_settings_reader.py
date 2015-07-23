from SYNTAX import *
from Basic_tools import *

def get_gene_value(organism, gene):
    if is_function(organism[gene]):
        return organism[gene](organism)
    else:
        return organism[gene]

def make_function_from_string(function_settings, all_gene_names, tags_list, error_messenger):
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
                error_messenger('Syntax error in ', function_settings, tag, 'not in tags list', tags_list)
                error_maker = 1/0
            gene_name = function_settings[length+1:]
            return lambda *arguments: arguments[tag_position][gene_name]
        elif hash_position == -1:
            if function_settings in all_gene_names:
                return lambda *arguments: arguments[0][function_settings] if is_tuple_or_list(arguments) else arguments[function_settings]
            else:
                return lambda *arguments: function_settings
        else:
            error_messenger('Syntax error. ', function_settings)
            error_maker = 1/0

def make_function_from_built_function(function_settings, tags_list):
    error_maker = 1/0
    """ This will be erased if it is no longer used """
    function_and_parameters = function_settings['function']
    if is_tuple_or_list(function_and_parameters) and len(function_and_parameters) > 0:
        function = function_and_parameters[0]
        if is_function(function):
            parameters = [make_function(item, tags_list, error_messenger) for item in function_and_parameters[1:]]
            return lambda *arguments: function(*[item(*arguments) for item in parameters])
        else:
            "Error"
            error_maker = 1/0
    elif is_function(function_and_parameters):
        return lambda *arguments: function_and_parameters() # Call without arguments

def apply_associative_operator(main_operation, inputs):
    return reduce(main_operation, inputs[1:], inputs[0])

def make_function_from_dict(function_settings, all_gene_names, tags_list, error_messenger):

    command = main_command(function_settings, error_messenger)
    inputs = function_settings[command]

    if command == 'literal':
        return lambda *arguments: inputs # 'literal' operator returns its input without evaluate it
    
        """ This will be erased, because it may not be necessary:

    elif command == 'if':
        (condition, value_if_true, value_if_false) = \
            [make_function(item, tags_list, error_messenger) for item in function_settings['if']]
        return lambda *arguments: \
            value_if_true(*arguments) \
            if condition(*arguments) \
            else value_if_false(*arguments)
    
    elif command == 'function':
        return make_function_from_built_function(function_settings, tags_list)
    
    elif command == 'discrete distribution':
        def choice_value(values_list, r, *arguments):
            i = 0
            while (i < len(values_list) - 1) and (r > values_list[i][0](*arguments)):
                i += 1
                r -= values_list[i][0](*arguments)
            return values_list[i][1](*arguments)
        values_list = [(make_function(pair['probability'], tags_list, error_messenger), make_function(
            pair['value'], tags_list, error_messenger)) for pair in function_settings['discrete distribution']]
        return lambda *arguments: choice_value(values_list, random(), *arguments)
        """

    elif command == 'cost':
        if is_string(inputs):
            substance_name = 'energy reserve'
            action_name = inputs
        elif is_tuple_or_list(inputs):
            substance_name = inputs[1]
            action_name = inputs[0]
        elif is_dict(inputs):
            substance_name = inputs['substance']
            action_name = inputs['action']

        print "action_name", action_name, "substance_name", substance_name, "inputs", inputs
        return lambda *arguments: arguments[0].parent_ecosystem.costs[action_name][substance_name](arguments[0])

    elif command == 'constraint':
        return lambda *arguments: arguments[0].parent_ecosystem.constraints[inputs](arguments[0])

    elif command in All_operators:
        inputs_function = make_function(inputs, all_gene_names, tags_list, error_messenger)
        main_operation = Operator_definition[command]['output function']
        if command in Associative_operators:          
            return lambda *arguments: apply_associative_operator(main_operation, inputs_function(*arguments))
        elif command in Unary_operators:
            return lambda *arguments: main_operation(inputs_function(*arguments))
        else:
            return lambda *arguments: main_operation(*(inputs_function(*arguments)))
    

    print "Hey, dude! We shouldn't be here!"
    #print_dictionary( function_settings )
    error_messenger('Syntax error in', function_settings)
    error_messenger('Unknown command', command)
    error_maker = 1/0

def constrain_function_to_allowed_interval(function_to_return, interval_settings):
    if hasattr(interval_settings, '__iter__') and not is_dict(interval_settings):
        lower_bound = make_function(
            interval_settings[0], tags_list, error_messenger)
        upper_bound = make_function(
            interval_settings[1], tags_list, error_messenger)
    else:
        interval = make_function(interval_settings, tags_list, error_messenger)
    bounded_value = lambda value, a, b: a if value < a else b if value > b else value
    if number_of_organisms == 0:
        return lambda *arguments: bounded_value(
            function_to_return(*arguments), 
            lower_bound(*arguments), 
            upper_bound(*arguments))

def make_function(function_settings, all_gene_names, tags_list = [], error_messenger = default_error_messenger):
    
    if is_number(function_settings) or is_function(function_settings):
        return lambda *arguments: function_settings
    elif is_string(function_settings):
        return make_function_from_string(function_settings, all_gene_names, tags_list, error_messenger)
    elif is_tuple_or_list(function_settings):
        terms = [make_function(item, all_gene_names, tags_list, error_messenger)
                 for item in function_settings]
        return lambda *arguments: [item(*arguments) for item in terms] # This is necessary for 'shuffle' operator
    elif is_dict(function_settings):
        function_to_return = make_function_from_dict(function_settings, all_gene_names, tags_list, error_messenger)
        if 'allowed interval' in function_settings:
            return constrain_function_to_allowed_interval(
                function_to_return, 
                function_settings['allowed interval'])
        else:
            return function_to_return


def read_function_settings(function_name, all_gene_names, function_settings, error_messenger = default_error_messenger):
    return make_function(function_settings, all_gene_names, get_tags_list(function_name), error_messenger)



