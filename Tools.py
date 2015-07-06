from random import *
from functools import reduce
from math import *
from copy import *
#from Ecosystem_settings import *
from types import FunctionType
from Basic_tools import *

# THIS IS ONLY FOR TESTING:
test_organism = {'strength': 2.0,
                 'speed': 3.0,
                 'procreating frequency': 0.3,
                 'attack capacity': 5.0,
                 'defense capacity': 2.0,
                 'photosynthesis capacity': 10.0,
                 'age': 120,
                 'procreate?': {'randbool': 0.8},
                 'energy reserve': 15.0,
                 'energy storage capacity': 1000,
                 'test': 0}

print_costs = False
print_deths = False
print_killed = False
print_births = False
print_ages = False
print_organisms = False


# GENE FUNCTIONS:

def extract_genes_names(genes_settings):
    if isinstance(genes_settings, str):
        return set([genes_settings])
    elif hasattr(genes_settings, '__iter__'):
        result_set = set([])
        for item in genes_settings:
            result_set = result_set.union(extract_genes_names(item))
        return result_set
    else:
        return set([])


def unpack_genes(genes_settings):
    """
    For convenience reason, the user can define some genes all together, like this:

        ('moving frequency', 
        'hunting frequency', 
        'procreating frequency'): {
            'initial value': {'uniform': [0, 1]},
            'mutability': {
                'absolute variation': {'gauss': (0, 0.001)},
                'allowed interval': [0, 1],
                'mutation frequency': 0.01
                }}


    Then, we have to unpack them, producing the following settings:

        'moving frequency': {
            'initial value': {'uniform': [0, 1]},
            'mutability': {
                'absolute variation': {'gauss': (0, 0.001)},
                'allowed interval': [0, 1],
                'mutation frequency': 0.01
                }},
        'hunting frequency': {
            'initial value': {'uniform': [0, 1]},
            'mutability': {
                'absolute variation': {'gauss': (0, 0.001)},
                'allowed interval': [0, 1],
                'mutation frequency': 0.01
                }}, 
        'procreating frequency': {
            'initial value': {'uniform': [0, 1]},
            'mutability': {
                'absolute variation': {'gauss': (0, 0.001)},
                'allowed interval': [0, 1],
                'mutation frequency': 0.01
                }}
   """
    def merge_gene_settings(A, B):
        if is_dictionary(A):
            dict_A = deep_copy_of_a_dictionary(A)
        else:
            dict_A = deep_copy_of_a_dictionary({'initial value': A})
        if is_dictionary(B):
            dict_B = deep_copy_of_a_dictionary(B)
        else:
            dict_B = deep_copy_of_a_dictionary({'initial value': B})
        for item in dict_B:
            dict_A[item] = dict_B[item]
        return dict_A

    settings_to_return = {}
    for item in genes_settings:
        if hasattr(item, '__iter__'):
            for gene in item:
                if gene in settings_to_return:
                    settings_to_return[gene] = merge_gene_settings(
                        settings_to_return[gene], genes_settings[item])
                else:
                    settings_to_return[gene] = deep_copy_of_a_dictionary(
                        genes_settings[item])
        else:
            if item in settings_to_return:
                settings_to_return[item] = merge_gene_settings(
                    settings_to_return[item], genes_settings[item])
            else:
                settings_to_return[item] = deep_copy_of_a_dictionary(
                    genes_settings[item])
    return settings_to_return



""" this method returns a random function that accept no arguments: """  # This method is unused by the moment, but it may will. And it works!


def random_function_with_no_argument_maker(function_settings):
    def choice_value(values, r):
        i = 0
        while r > values[i]['probability']:
            i += 1
        return values[i]['value']
    if function_settings['type'] == 'random function':
        if function_settings['subtype'] == 'gaussian':
            mean = function_settings['mean']
            variance = function_settings['variance']
            return lambda: gauss(mean, variance)
        elif function_settings['subtype'] == 'uniform distribution':
            interval = function_settings['interval']
            return lambda: uniform(*interval)
        elif function_settings['subtype'] == 'discrete distribution':
            values = copy.deepcopy(function_settings['values'])
            total = 0
            for pair in values:
                total += pair['probability']
                pair['probability'] = total
            return lambda: choice_value(values, random())
        elif function_settings['subtype'] == 'chi-squared distribution':
            k = function_settings['k']
            coefficient = function_settings['coefficient']
            return lambda: coefficient * math.fsum(gauss(0, 1)**2 for i in range(k))
    return lambda: random()



def make_function(function_settings, number_of_organisms=1, arguments=[]):
    #test_organism['test'] += 1
    function_to_return = None
    if (hasattr(function_settings, '__iter__') and
            'number of organisms' in function_settings):
        number_of_organisms = function_settings['number of organisms']
    if is_number(function_settings):
        if number_of_organisms == 0:
            return lambda: function_settings
        elif number_of_organisms == 1:
            return lambda organism: function_settings
        elif number_of_organisms == 2:
            return lambda predator, prey: function_settings
    elif isinstance(function_settings, str):
        if number_of_organisms == 0:
            return lambda: function_settings
        elif number_of_organisms == 1:
            return lambda organism: (organism[function_settings](organism) if is_function(organism[function_settings]) else organism[function_settings]) if function_settings in organism else function_settings
        elif number_of_organisms == 2:
            return lambda predator, prey: (
                (predator[function_settings](predator) if is_function(predator[function_settings]) else predator[
                 function_settings]) if function_settings in predator else function_settings,
                (prey[function_settings](prey) if is_function(prey[function_settings]) else prey[function_settings]) if function_settings in prey else function_settings)
    elif hasattr(function_settings, '__iter__') and not is_dict(function_settings):
        terms = [make_function(item, number_of_organisms)
                 for item in function_settings]
        if number_of_organisms == 0:
            return lambda: [item() for item in terms]
        elif number_of_organisms == 1:
            return lambda organism: [item(organism) for item in terms]
        elif number_of_organisms == 2:
            return lambda predator, prey: [item(predator, prey) for item in terms]
    elif is_dict(function_settings):
        if 'predator' in function_settings:
            if number_of_organisms == 2:
                function_to_return = lambda predator, prey: predator[function_settings['predator']](predator) if is_function(
                    predator[function_settings['predator']]) else predator[function_settings['predator']]
            else:
                print function_settings
                print "Error in number of organisms", 1/0
        elif 'prey' in function_settings:
            if number_of_organisms == 2:
                function_to_return = lambda predator, prey: prey[function_settings['prey']](
                    prey) if is_function(prey[function_settings['prey']]) else prey[function_settings['prey']]
            else:
                print "Error in number of organisms", 1/0
        elif 'literal' in function_settings:
            if number_of_organisms == 0:
                function_to_return = lambda: function_settings['literal']
            elif number_of_organisms == 1:
                function_to_return = lambda organism: function_settings[
                    'literal']
            elif number_of_organisms == 2:
                function_to_return = lambda predator, prey: function_settings[
                    'literal']
        elif 'value, not function' in function_settings:
            return function_settings['value, not function']
        for operator in Binary_operators_dictionary:
            if operator in function_settings:
                terms = [make_function(item, number_of_organisms)
                         for item in function_settings[operator]]
                main_operation = Binary_operators_dictionary[operator]
                if number_of_organisms == 0:
                    function_to_return = lambda: reduce(
                        main_operation, [term() for term in terms[1:]], terms[0]())
                elif number_of_organisms == 1:
                    function_to_return = lambda organism: reduce(
                        main_operation, [term(organism) for term in terms[1:]], terms[0](organism))
                elif number_of_organisms == 2:
                    function_to_return = lambda predator, prey: reduce(
                        main_operation, [term(predator, prey) for term in terms[1:]], terms[0](predator, prey))
                break  # please, don't remove this line. It's vital!!!
        for operator in Unary_operators_dictionary:
            if operator in function_settings:
                argument = make_function(
                    function_settings[operator], number_of_organisms)
                main_operation = Unary_operators_dictionary[operator]
                if number_of_organisms == 0:
                    function_to_return = lambda: main_operation(argument())
                elif number_of_organisms == 1:
                    function_to_return = lambda organism: main_operation(
                        argument(organism))
                elif number_of_organisms == 2:
                    function_to_return = lambda predator, prey: main_operation(
                        argument(predator, prey))
                break  # please, don't remove this line. It's vital!!!
        if 'choice' in function_settings:
            dictionary = {}
            for item in function_settings:
                dictionary[item] = make_function(
                    function_settings[item], number_of_organisms)
            parameter = dictionary['choice']
            if number_of_organisms == 0:
                function_to_return = lambda: dictionary[parameter()]()
            elif number_of_organisms == 1:
                function_to_return = lambda organism: dictionary[
                    parameter(organism)](organism)
            elif number_of_organisms == 2:
                function_to_return = lambda predator, prey: dictionary[
                    parameter(predator, prey)](predator, prey)
        elif 'tuple' in function_settings:
            tuple_to_return = tuple(
                make_function(item, number_of_organisms) for item in function_settings['tuple'])
            if number_of_organisms == 0:
                function_to_return = lambda: tuple(
                    item() for item in tuple_to_return)
            elif number_of_organisms == 1:
                function_to_return = lambda organism: tuple(
                    item(organism) for item in tuple_to_return)
            elif number_of_organisms == 2:
                function_to_return = lambda predator, prey: tuple(
                    item(predator, prey) for item in tuple_to_return)
        elif 'cost' in function_settings:
            if number_of_organisms == 1:
                action = function_settings['cost']
                if 'substance' in function_settings:
                    substance = function_settings['substance']
                else:
                    substance = 'energy reserve'
                function_to_return = lambda organism: organism.parent_ecosystem.costs[
                    action][substance](organism)
        elif 'constraint' in function_settings:
            action = function_settings['constraint']
            if number_of_organisms == 1:
                function_to_return = lambda organism: organism.parent_ecosystem.constraints[action]
            if number_of_organisms == 2:
                function_to_return = lambda predator, prey: predator.parent_ecosystem.constraints[
                    action]
        elif 'function' in function_settings:
            if function_settings['function'] == 'sigmoid':
                if 'homothety' in function_settings:
                    homothety = make_function(
                        function_settings['homothety'], number_of_organisms)
                else:
                    if number_of_organisms == 0:
                        homothety = lambda: 1
                    elif number_of_organisms == 1:
                        homothety = lambda organism: 1
                    elif number_of_organisms == 2:
                        homothety = lambda predator, prey: 1
                if 'translation' in function_settings:
                    translation = make_function(
                        function_settings['translation'], number_of_organisms)
                else:
                    if number_of_organisms == 0:
                        translation = lambda: 0
                    elif number_of_organisms == 1:
                        translation = lambda organism: 0
                    elif number_of_organisms == 2:
                        translation = lambda predator, prey: 0
                if 'parameter' in function_settings:
                    parameter = make_function(
                        function_settings['parameter'], number_of_organisms)
                else:
                    if number_of_organisms == 0:
                        parameter = lambda: random()
                    elif number_of_organisms == 1:
                        parameter = lambda organism: random()
                    elif number_of_organisms == 2:
                        parameter = lambda predator, prey: random()
                if number_of_organisms == 0:
                    function_to_return = lambda: sigmoid(
                        translation() + parameter() * homothety())
                elif number_of_organisms == 1:
                    function_to_return = lambda organism: sigmoid(
                        translation(organism) + parameter(organism) * homothety(organism))
                elif number_of_organisms == 2:
                    function_to_return = lambda predator, prey: sigmoid(translation(
                        predator, prey) + parameter(predator, prey) * homothety(predator, prey))
            elif function_settings['function'] == 'discrete distribution':
                def choice_value_0(values_list, r):
                    i = 0
                    while (i < len(values_list) - 1) and (r > values_list[i][0]()):
                        i += 1
                        r -= values_list[i][0]()
                    return values_list[i][1]()

                def choice_value_1(organism, values_list, r):
                    i = 0
                    while (i < len(values_list) - 1) and (r > values_list[i][0](organism)):
                        i += 1
                        r -= values_list[i][0](organism)
                    return values_list[i][1](organism)

                def choice_value_2(predator, prey, values_list, r):
                    i = 0
                    while (i < len(values_list) - 1) and (r > values_list[i][0](predator, prey)):
                        i += 1
                        r -= values_list[i][0](predator, prey)
                    return values_list[i][1](predator, prey)
                values_list = [(make_function(pair['probability'], number_of_organisms), make_function(
                    pair['value'], number_of_organisms)) for pair in function_settings['values list']]
                if number_of_organisms == 0:
                    function_to_return = lambda: choice_value_0(
                        values_list, random())
                elif number_of_organisms == 1:
                    function_to_return = lambda organism: choice_value_1(
                        organism, values_list, random())
                elif number_of_organisms == 2:
                    function_to_return = lambda predator, prey: choice_value_2(
                        predator, prey, values_list, random())

            elif (function_settings['function'] == 'seek free location') and (number_of_organisms == 1):
                function_to_return = lambda organism: organism.parent_ecosystem.biotope.seek_free_location()
            elif function_settings['function'] == 'seek free location close to':
                if 'center' in function_settings:
                    center = make_function(
                        function_settings['center'], number_of_organisms)
                else:
                    center = lambda organism: organism['location']
                radius = make_function(
                    function_settings['radius'], number_of_organisms)
                function_to_return = lambda organism: organism.parent_ecosystem.biotope.seek_free_location_close_to(
                    center(organism), radius(organism))
            elif (function_settings['function'] == 'seek random organism') and (number_of_organisms == 1):
                if 'center' in function_settings:
                    center = make_function(
                        function_settings['center'], number_of_organisms)
                else:
                    center = lambda organism: organism['location']
                radius = make_function(
                    function_settings['radius'], number_of_organisms)
                function_to_return = lambda organism: organism.parent_ecosystem.biotope.seek_free_location_close_to(
                    center(organism), radius(organism))

    if function_to_return == None:
        print "Hey, dude! We shouldn't be here!"
        #print_dictionary( function_settings )
        print function_settings
        error_maker = 1/0
        return lambda organism: 'Error: unknown function'

    if is_dict(function_settings) and 'allowed interval' in function_settings:
        interval_settings = function_settings['interval']
        if hasattr(interval_settings, '__iter__') and not is_dictionary(interval_settings):
            lower_bound = make_function(
                interval_settings[0], number_of_organisms)
            upper_bound = make_function(
                interval_settings[1], number_of_organisms)
        else:
            interval = make_function(interval_settings, number_of_organisms)
        bounded_value = lambda value, a, b: a if value < a else b if value > b else value
        if number_of_organisms == 0:
            return lambda: bounded_value(function_to_return(), lower_bound(), upper_bound())
        elif number_of_organisms == 1:
            return lambda organism: bounded_value(function_to_return(organism), lower_bound(organism), upper_bound(organism))
        elif number_of_organisms == 2:
            return lambda predator, prey: bounded_value(function_to_return(predator, prey), lower_bound(predator, prey), upper_bound(predator, prey))
    else:
        return function_to_return

