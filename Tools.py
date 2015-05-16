from random import *
from functools import reduce
from math import *
from copy import *
from Ecosystem_settings import *

def is_number(x):
    try:
        x + 1
        return True
    except TypeError:
        return False

def prod(iterable): # Calculates the product of all the elements in the iterable
    return reduce((lambda x, y: x * y), iterable, 1)

def signed_random():
    return 2*random() - 1

def float_range(start, stop = 0.0, step = 1.0): # equivalent to range( ) but with float parameters
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
    
  
""" 
#unused function:

def create_empty_list_of_lists(size_x, size_y):
    return [[None] * size_y for i in range(size_x)]
"""

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

        if (x == None) or (y == None):
            print "Eh, te pille!!!"
        
        self.data[x % self.size_x][y % self.size_y] = value

    def __str__(self, traspose = False):
        if traspose:        
            return "\n".join(str(self.data[i]) for i in range(len(self.data)))
        else:
            return "\n".join(str([self.data[i][j] for i in range(self.size_x)]) for j in range(self.size_y))
""" this method returns a random function that accept no arguments: """ # This method is unused by the moment, but it may will. And it works!
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

def make_comparison_operator(comparison_operator):
    comparison_operators_dictionary = {
        '>': lambda x, y: x > y,
        '<': lambda x, y: x < y,
        '>=': lambda x, y: x >= y,
        '<=': lambda x, y: x <= y,
        '==': lambda x, y: x == y,
        '!=': lambda x, y: x != y}
    return comparison_operators_dictionary[comparison_operator]
    
def make_function(function_settings):
    if is_number(function_settings):
        return lambda organism: function_settings
    elif isinstance(function_settings, str):
        return lambda organism: organism[function_settings]
    elif isinstance(function_settings, dict):
        if 'type' in function_settings.keys():
            # RANDOM FUNCTIONS:
            if function_settings['type'] == 'random function':
                if function_settings['subtype'] == 'gaussian':
                    mean = make_function(function_settings['mean'])
                    variance = make_function(function_settings['variance'])
                    return lambda organism: gauss(mean(organism), variance(organism))
                elif function_settings['subtype'] == 'uniform distribution':
                    a = make_function(function_settings['interval'][0])
                    b = make_function(function_settings['interval'][1])
                    return lambda organism: uniform(a(organism), b(organism))
                elif function_settings['subtype'] == 'discrete distribution':
                    def choice_value(values, r):
                        i = 0
                        while r > values[i]['probability']:
                            i += 1
                        return values[i]['value']
                    values = deepcopy(function_settings['values'])
                    total = 0
                    for pair in values:
                        total += pair['probability']
                        pair['probability'] = total
                    return lambda organism: choice_value(values, random())
                elif function_settings['subtype'] == 'chi-squared distribution':
                    coefficient = make_function(function_settings['coefficient'])
                    k = make_function(function_settings['k'])
                    return lambda organism: coefficient(organism) * math.fsum(gauss(0, 1)**2 for i in range(k(organism)))
                else:
                    return lambda organism: random()
             
            # OUTAY FUNCTIONS:
            elif function_settings['type'] == 'outlay function':
                if function_settings['subtype'] == 'linear function':
                    independent_term = 0
                    dependent_terms = []
                    for term in function_settings['terms']:
                        if term['parameter'] == None:
                            independent_term = make_function(term['coefficient'])
                        else:
                            dependent_terms.append((term['parameter'], make_function(term['coefficient'])))
                    return lambda organism: sum([(organism[parameter] * coefficient(organism)) for (parameter, coefficient) in dependent_terms], independent_term(organism))
                elif function_settings['subtype'] == 'n-linear function':
                    terms = [(term['parameters'], make_function(term['coefficient'])) for term in function_settings['terms']]
                    return lambda organism: sum([(prod([organism[parameter] for parameter in parameters])*coeficient(organism)) for (parameters, coeficient) in terms])
                return lambda organism: 0
                
            # CONSTRAINT FUNCTIONS:
            if function_settings['type'] == 'constraint function':
                if function_settings['subtype'] == 'thresholds':
                    def make_term(term):
                        if term['operator'] == '>':
                            compare = lambda x, y: (x > y)
                        elif term['operator'] == '<':
                            compare = lambda x, y: (x < y)
                        else:
                            return 'error: unknown operator ' + term['operator']
                        if 'threshold' in term.keys():
                            threshold = lambda: term['threshold']
                        elif 'random threshold' in term.keys():
                            threshold = random_function_with_no_argument_maker(term['random threshold'])
                        return lambda organism: compare(organism[term['parameter']], threshold())
                    if len(function_settings['terms']) == 0:
                        return 'Error in constraint function from input data'
                    if function_settings['operator'] == 'and':
                        bool_operator = lambda x, y: (x and y)
                    elif function_settings['operator'] == 'or':
                        bool_operator = lambda x, y: (x or y)
                    else:
                        bool_operator = lambda x, y: logical_xor(x, y)
                    terms = [make_term(term) for term in function_settings['terms']]
                    return lambda organism: reduce(bool_operator, [term(organism) for term in terms[1:]], terms[0](organism))    
                elif function_settings['subtype'] == 'hunting':
                    predator_value = make_function(function_settings['predator value'])
                    prey_value = make_function(function_settings['prey value'])
                    comparison = make_comparison_operator(function_settings['operator'])
                    return lambda predator, prey: comparison(predator_value(predator), prey_value(prey))
                                
            # BUILT-IN FUNCTIONS:
            if function_settings['type'] == 'built-in function':
                if functions_settings['name'] == 'seek free location':
                    return lambda organism: organism.parent_ecosystem.biotope.seek_free_location() 
            
    elif hasattr(function_settings, '__iter__'):
        function_list = [make_function(item) for item in function_settings]
        return lambda organism: [item(organism) for item in function_list]

    print "Hey, dude! We shouldn't be here!"
    print_dictionary( function_settings )
    return lambda organism: 'Error: unknown function'

def dictionary_to_string(dictionary, indent_level = 0):
    dict_string = ""
    tabulator = " "*4
    if isinstance(dictionary, dict):
        dict_string += tabulator*indent_level + '{\n' # This line could be removed
        for key in dictionary.keys():
            if hasattr(dictionary[key], '__iter__'):
                dict_string += tabulator*indent_level + str(key)+":\n"
                dict_string += dictionary_to_string(dictionary[key], indent_level + 1)
            else:
                dict_string += tabulator*indent_level + str(key) + ": " + str(dictionary[key]) + "\n"
        dict_string +=  tabulator*indent_level + '}\n' # This line also could be removed
    elif hasattr(dictionary, '__iter__'):
        for element in dictionary:
            dict_string += dictionary_to_string(element, indent_level + 1)
    else:
        dict_string += tabulator*indent_level + str(dictionary) + "\n"
    return dict_string
    
def print_dictionary(dictionary):
    print dictionary_to_string(dictionary)

def merge_dictionaries(dictionary_to_be_completed, dictionary_to_complete_with):
    for item in dictionary_to_complete_with:
        if item in dictionary_to_be_completed:
            if isinstance(dictionary_to_be_completed[item], dict) and isinstance(dictionary_to_complete_with[item], dict):
                merge_dictionaries(dictionary_to_be_completed[item], dictionary_to_complete_with[item])
            else:
                dictionary_to_be_completed[item] = dictionary_to_complete_with[item]
                


            
            
            
            
            
            
            