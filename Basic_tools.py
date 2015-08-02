from random import *
from functools import reduce
from math import *
from copy import *
from types import FunctionType

# Variables for debuggin: # ***
print_ages = False
print_organisms = False
print_deths = False
print_number_of_deths = True
print_killed = False
print_costs = False
print_reserves = False
print_births = False
print_number_of_births = True
print_methods_names = False
print_operators = False
print_trade_transactions = 0.01  # print 0.1 per cent of them


class Default:
    def __init__(self):
        self.trade_radius = 1.5
        self.hunt_radius = 1.5
        self.speed = 1.5
        self.radius_of_procreation = 1.5

DEFAULT = Default()


class Matrix(object):

    def __init__(self, size_x, size_y, value=None):
        self.data = [[value] * size_y for i in range(size_x)]
        # No usar [[None] * size_y] * size_x, ya que no hace copia profunda
        self.size_x = size_x
        self.size_y = size_y

    def __getitem__(self, coordinates):
        x, y = coordinates
        return self.data[x % self.size_x][y % self.size_y]

    def __setitem__(self, coordinates, value):
        x, y = coordinates
        self.data[x % self.size_x][y % self.size_y] = value

    def __str__(self, traspose=False):
        if traspose:
            return "\n".join(str(self.data[i]) for i in range(len(self.data)))
        else:
            return "\n".join(
                str([self.data[i][j] for i in range(self.size_x)])
                for j in range(self.size_y)
            )


# TYPE FUNCTIONS:

def is_number(x):
    try:
        x + 1
        return True
    except TypeError:
        return False


def is_string(x):
    return isinstance(x, str)


def is_function(x):
    return isinstance(x, FunctionType)


def is_dict(x):
    return isinstance(x, dict)


def is_iterable(x):
    return hasattr(x, '__iter__')


def is_list(x):
    return isinstance(x, list)


def is_tuple(x):
    return isinstance(x, tuple)


def is_tuple_or_list(x):
    return isinstance(x, list) or isinstance(x, tuple)


def is_boolean(x):
    return isinstance(x, bool)


def count_elements(expression, *sets_list):
    results_list = [{'set': set_, 'result': 0} for set_ in sets_list]
    number_of_unknown_elements = 0
    for element in expression:
        unknown_element = True
        for pair in results_list:
            if element in pair['set']:
                pair['result'] += 1
                unknown_element = False
        if unknown_element:
            number_of_unknown_elements += 1
    return (
        [
            pair['result']
            for pair in results_list
        ] +
        [number_of_unknown_elements]
    )

# MATH FUNCTIONS:


def prod(iterable):
    # Calculates the product of all the elements in the iterable
    return reduce((lambda x, y: x * y), iterable, 1)


def signed_random():
    return 2 * random() - 1


def random_true(probability_of_True):
    return probability_of_True > random()


def chi_squared(k):
    # random value, chi-squared distribution with given degree of freedom k
    return fsum(gauss(0, 1)**2 for i in range(k))


def float_range(start, stop=0.0, step=1.0):
    # equivalent to range( ) but with float parameters
    result = []
    if step * (stop - start) < 0:
        start, stop = stop, start
    x = start
    if step > 0:
        while x < stop:
            result.append(x)
            x += step
    elif step < 0:
        while x > stop:
            result.append(x)
            x += step
    return result


def bounded_value(value, a, b):  # a and b could be infinity
    """ This function returns value if a <= value <= b,
    returns a if value < a and returns b if value > b """
    # print 'Value:', value, 'a:', a, 'b:', b  # ***
    if (
        a in {'- infinity', '-infinity'} and
        b in {'+ infinity', '+infinity', 'infinity'}
    ):  # this means no constraints
        return value
    elif a in {'- infinity', '-infinity'}:
        if value in {'- infinity', '-infinity'}:
            return value
        else:
            return min(value, b)
    elif b in {'+ infinity', '+infinity', 'infinity'}:
        if value in {'+ infinity', '+infinity', 'infinity'}:
            return value
        else:
            return max(value, a)
    else:
        return max(a, min(value, b))


def sigmoid(x):
    t = bounded_value(x, -50, 50)
    return exp(t) / (1 + exp(t))


def shuffle_function(*list_object):
    if len(list_object) == 1 and is_tuple_or_list(list_object[0]):
        result_list = list(copy(list_object[0]))
    else:
        result_list = list(copy(list_object))
    shuffle(result_list)
    return result_list


def choice_operator(inputs):
    for pair in inputs[1:]:
        if inputs[0] == pair[0]:
            return pair[1]


# DICTIONARIES:


def dictionary_to_string(dictionary, indent_level=0):
    tabulator = " " * 4
    if hasattr(dictionary, '__iter__'):
        result_list = []
        indent_level += 1
        for item in dictionary:
            if is_string(item):
                new_element = tabulator * indent_level + "'" + item + "'"
            else:
                new_element = tabulator * indent_level + str(item)
            if is_dict(dictionary):
                new_element += ": " + dictionary_to_string(
                    dictionary[item],
                    indent_level)
            result_list += [new_element]
        if is_dict(dictionary):
            return (
                '{\n' +
                ',\n'.join(result_list) +
                '\n' +
                tabulator * indent_level +
                '}'
            )
        elif is_list(dictionary):
            return (
                '[\n' +
                ',\n'.join(result_list) +
                '\n' +
                tabulator * indent_level +
                ']'
                )
        else:
            return (
                '(\n' +
                ',\n'.join(result_list) +
                '\n' +
                tabulator * indent_level +
                ')'
                )
    elif is_string(dictionary):
        return "'" + dictionary + "'"
    else:
        return str(dictionary)


def print_dictionary(dictionary, dictionary_name=''):
    if dictionary_name != '':
        print dictionary_name + " = " + dictionary_to_string(dictionary)
    else:
        print dictionary_to_string(dictionary)


def print_organism(organism, *lists_of_genes):
    for one_list in lists_of_genes:
        if is_string(one_list):
            if one_list in organism:
                print one_list + ": " + str(organism[one_list]),
            else:
                print "\n", one_list, 'NOT FOUND.'
        elif is_tuple_or_list(one_list):
            print_organism(organism, *one_list)
        else:
            print one_list, 'NOT A GENE NOR GENES LIST'
    print "\n"


def merge_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)

    """
        Es necesario encontrar la version original de esta funcion,
        porque esta no funciona.
    """

    return z


def deep_copy_of_a_dictionary(dictionary):
    if is_dict(dictionary):
        copy_to_return = {}
        for item in dictionary:
            copy_to_return[item] = deep_copy_of_a_dictionary(dictionary[item])
    elif hasattr(dictionary, '__iter__'):
        copy_to_return = []
        for item in dictionary:
            copy_to_return.append(deep_copy_of_a_dictionary(item))
        if is_tuple(dictionary):
            copy_to_return = tuple(copy_to_return)
    else:
        copy_to_return = copy(dictionary)
    return copy_to_return


def evaluate_functions_of_a_dictionary(dictionary, *inputs):
    if is_dict(dictionary):
        result = {}
        for item in dictionary:
            result[item] = evaluate_functions_of_a_dictionary(
                dictionary[item],
                *inputs)
        return result
    elif is_function(dictionary):
        return dictionary(*inputs)
    else:
        return deepcopy(dictionary)


# GENE FUNCTIONS:


def make_variation(
    gene, relative_variation=0,
    absolute_variation=0,
    probability_of_change=1
        ):
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


def make_random_variation(
    gene,
    max_relative_variation=0,
    max_absolute_variation=0,
    probability_of_change=1
        ):

    if max_relative_variation == 0:
        random_relative_variation = 0
    else:
        random_relative_variation = {'*': (
            {'uniform': (-1, 1)},
            max_relative_variation
        )}

    if max_absolute_variation == 0:
        random_absolute_variation = 0
    else:
        random_absolute_variation = {'*': (
            {'uniform': (-1, 1)},
            max_absolute_variation
        )}

    return make_variation(
        gene=gene,
        relative_variation=random_relative_variation,
        absolute_variation=random_absolute_variation,
        probability_of_change=probability_of_change)


def extract_all_gene_names(ecosystem_settings):
    categories = ecosystem_settings['organisms']
    result_set = set([])
    for category_name in categories:
        result_set = result_set.union(
            set(categories[category_name]['genes'].keys()))
    return result_set


def extract_biotope_feature_names(ecosystem_settings):
    return ecosystem_settings['biotope']['biotope features'].keys()


def extract_ecosystem_feature_names(ecosystem_settings):
    return ecosystem_settings['ecosystem features'].keys()


def extract_all_feature_names(ecosystem_settings):
    return (
        extract_biotope_feature_names(ecosystem_settings) +
        extract_ecosystem_feature_names(ecosystem_settings)
    )


def extract_all_strings(settings, exceptions=[]):
    result_set = set([])
    if is_string(settings):
        result_set = set([settings])
    if is_iterable(settings):
        for item in settings:
            result_set = result_set.union(
                extract_all_strings(item, exceptions))
    if is_dict(settings):
        for item in settings:
            if item not in exceptions:
                result_set = result_set.union(
                    extract_all_strings(settings[item], exceptions))
    return set([item for item in result_set if item not in exceptions])


def extract_from_dict(keyword, dictionary):
    result = []
    if keyword in dictionary:
        if is_tuple_or_list(dictionary[keyword]):
            result = list(dictionary[keyword])
    for item in dictionary:
        if is_dict(dictionary[item]):
            result += extract_from_dict(keyword, dictionary[item])
    return result


def get_tags_list(function_name):
    tags_list = []
    end_position = 0
    keep_looping = True
    while keep_looping:
        hash_position = function_name.find('#', end_position)
        if hash_position > -1:
            if hash_position == len(function_name) - 1:
                print "Syntax error!", function_name
                halt()
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
        while (
            hash_position > 0 and function_name[hash_position - 1] == ' '
                ):
            hash_position -= 1
        return function_name[:hash_position]


def default_error_messenger(*error_messages):
    if (
        len(error_messages) > 0 and
        error_messages[len(error_messages) - 1] == ''
            ):
        for message in error_messages:
            print message,
    else:
        for message in error_messages:
            if is_dict(message):
                print_dictionary(message)
            elif is_iterable(message):
                for item in message:
                    default_error_messenger(item)
            else:
                print message
    return True
