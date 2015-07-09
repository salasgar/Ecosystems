from random import *
from functools import reduce
from math import *
from copy import *
#from Ecosystem_settings import *
from types import FunctionType


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
            return "\n".join(str([self.data[i][j] for i in range(self.size_x)]) for j in range(self.size_y))


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
    return [pair['result'] for pair in results_list] + [number_of_unknown_elements]

# MATH FUNCTIONS:

# Calculates the product of all the elements in the iterable
def prod(iterable):
    return reduce((lambda x, y: x * y), iterable, 1)

def signed_random():
    return 2*random() - 1

def random_boolean(probability_of_True):
    return (probability_of_True > random()),

def chi_squared(k): 
	return math.fsum(gauss(0, 1)**2 for i in range(k)) # random value, chi-squared distribution with given degree of freedom k

# equivalent to range( ) but with float parameters
def float_range(start, stop=0.0, step=1.0):
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
    """ This function returns value if a <= value <= b,  returns a if value < a and returns b if value > b """
    if a in {'- infinity', '-infinity'} and b in {'+ infinity', '+infinity', 'infinity'}:  # this means no constraints
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
    return exp(t)/(1+exp(t))

def shuffle_function(list_object):
    shuffle(list_object)
    return list_object

def choice_operator(inputs):
    for pair in inputs[1:]:
        if inputs[0] == pair[0]:
            return pair[1]


# DICTIONARIES:

def dictionary_to_string(dictionary, indent_level=0):
    dict_string = ""
    tabulator = " "*4
    if is_dict(dictionary):
        # This line could be removed
        dict_string += tabulator*indent_level + '{\n'
        for key in dictionary.keys():
            if hasattr(dictionary[key], '__iter__'):
                dict_string += tabulator*indent_level + str(key)+":\n"
                dict_string += dictionary_to_string(
                    dictionary[key], indent_level + 1)
            else:
                dict_string += tabulator*indent_level + \
                    str(key) + ": " + str(dictionary[key]) + "\n"
        # This line also could be removed
        dict_string += tabulator*indent_level + '}\n'
    elif hasattr(dictionary, '__iter__'):
        for element in dictionary:
            dict_string += dictionary_to_string(element, indent_level + 1)
    else:
        dict_string += tabulator*indent_level + str(dictionary) + "\n"
    return dict_string


def print_dictionary(dictionary):
    print dictionary_to_string(dictionary)


def merge_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)

    """
    	Es necesario encontrar la version original de esta funcion, porque esta no funciona.

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
    else:
        copy_to_return = copy(dictionary)
    return copy_to_return


# GENE FUNCTIONS:

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

def make_random_variation(gene, max_relative_variation = 0, max_absolute_variation = 0, probability_of_change = 1):
    
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
        gene = gene, 
        relative_variation = random_relative_variation,
        absolute_variation = random_absolute_variation,
        probability_of_change = probability_of_change)



#print 'abc'.index('b')



