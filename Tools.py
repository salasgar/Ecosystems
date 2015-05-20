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

Binary_operators_dictionary = {
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
    'in': lambda x, y: x in y  
}   
for operator in {'and', 'AND', '&', '&&'}:  # Este bucle for es por ahorrarme escribir lineas repetitivas. Lo dejamos asi o lo cambiamos?
    Binary_operators_dictionary[operator] = lambda x, y: x and y
for operator in {'or', 'OR', '|', '||'}:
    Binary_operators_dictionary[operator] = lambda x, y: x or y
for operator in {'xor', 'XOR'}:
    Binary_operators_dictionary[operator] = logical_xor

Unary_operators_dictionary = {
    'abs': abs,
    'sqrt': sqrt,
    'log': log,
    'sin': sin,
    'cos': cos,
    'tan': tan,
    'tg':  tan,
    'round': lambda x: round(x, 0) }

def make_function(function_settings, number_of_arguments = 1):
    if number_of_arguments == 0:           
        if is_number(function_settings):
            return lambda: function_settings
        elif isinstance(function_settings, str):
            return lambda: function_settings
        elif hasattr(function_settings, '__iter__') and not isinstance(function_settings, dict):
            function_list = [make_function(item, number_of_arguments) for item in function_settings]
            return lambda: [item() for item in function_list]
        elif isinstance(function_settings, dict):
            if 'literal' in function_settings:
                return lambda: function_settings['literal']
             for operator in Binary_operators_dictionary:
                if operator in function_settings:
                    terms = make_function(function_settings[operator], number_of_arguments)
                    return lambda: reduce(Binary_operators_dictionary[operator], [term() for term in terms[1:]], terms[0]())        
            for operator in Unary_operators_dictionary:
                if operator in function_settings:
                    argument = make_function(function_settings[operator], number_of_arguments)
                    return lambda: Unary_operators_dictionary[operator](argument())
            if 'function' in function_settings:
                if function_settings['function'] == 'gaussian':
                    mean = make_function(function_settings['mean'], number_of_arguments)
                    variance = make_function(function_settings['variance'], number_of_arguments)
                    return lambda: gauss(mean(), variance())
                elif function_settings['function'] == 'uniform distribution':
                    a = make_function(function_settings['interval'][0], number_of_arguments)
                    b = make_function(function_settings['interval'][1], number_of_arguments)
                    return lambda: uniform(a(), b())
                elif function_settings['function'] == 'discrete distribution':
                    def choice_value(values_list, r):
                        i = 0
                        while (i < len(values_list) - 1) and (r > values_list[i][0]()):
                            i += 1
                            r -= values_list[i][0]()
                        return values_list[i][1]()
                    values_list = [(make_function(pair['probability'], number_of_arguments),
                                    make_function(pair['value'], number_of_arguments))
                                    for pair in function_settings['values list']]
                    return lambda: choice_value(, values_list, random())
                elif function_settings['function'] == 'chi-squared distribution':
                    coefficient = make_function(function_settings['coefficient'], number_of_arguments)
                    k = make_function(function_settings['k'], number_of_arguments)
                    return lambda: coefficient() * math.fsum(gauss(0, 1)**2 for i in range(k()))                    


    elif number_of_arguments == 1:                
        if is_number(function_settings):
            return lambda organism: function_settings
        elif isinstance(function_settings, str):
            return lambda organism: organism[function_settings](organism) if isinstance(organism[function_settings], FunctionType) else organism[function_settings]
        elif hasattr(function_settings, '__iter__') and not isinstance(function_settings, dict):
            function_list = [make_function(item, number_of_arguments) for item in function_settings]
            return lambda organism: [item(organism) for item in function_list]
        elif isinstance(function_settings, dict):
            if 'literal' in function_settings:
                return lambda organism: function_settings['literal']
            for operator in Binary_operators_dictionary:
                if operator in function_settings:
                    terms = make_function(function_settings[operator], number_of_arguments)
                    return lambda organism: reduce(Binary_operators_dictionary[operator], [term(organism) for term in terms[1:]], terms[0](organism))        
            for operator in Unary_operators_dictionary:
                if operator in function_settings:
                    argument = make_function(function_settings[operator], number_of_arguments)
                    return lambda organism: Unary_operators_dictionary[operator](argument(organism))
            if 'function' in function_settings:
                if function_settings['function'] == 'gaussian':
                    mean = make_function(function_settings['mean'], number_of_arguments)
                    variance = make_function(function_settings['variance'], number_of_arguments)
                    return lambda organism: gauss(mean(organism), variance(organism))
                elif function_settings['function'] == 'uniform distribution':
                    a = make_function(function_settings['interval'][0], number_of_arguments)
                    b = make_function(function_settings['interval'][1], number_of_arguments)
                    return lambda organism: uniform(a(organism), b(organism))
                elif function_settings['function'] == 'discrete distribution':
                    def choice_value(organism, values_list, r):
                        i = 0
                        while (i < len(values_list) - 1) and (r > values_list[i][0](organism)):
                            i += 1
                            r -= values_list[i][0](organism)
                        return values_list[i][1](organism)
                    values_list = [(make_function(pair['probability'], number_of_arguments),
                                    make_function(pair['value'], number_of_arguments))
                                    for pair in function_settings['values list']]
                    return lambda organism: choice_value(organism, values_list, random())
                elif function_settings['function'] == 'chi-squared distribution':
                    coefficient = make_function(function_settings['coefficient'], number_of_arguments)
                    k = make_function(function_settings['k'], number_of_arguments)
                    return lambda organism: coefficient(organism) * math.fsum(gauss(0, 1)**2 for i in range(k(organism)))                    
                elif function_settings['function'] == 'seek free location':
                    return lambda organism: organism.parent_ecosystem.biotope.seek_free_location() 
                elif function_settings['function'] == 'seek free location close to':
                    center = make_function(function_settings['center'])
                    radius = make_function(function_settings['radius'])
                    return lambda organism: organism.parent_ecosystem.biotope.seek_free_location_close_to(
                        center(organism),
                        radius(organism)) 
                elif function_settings['function'] == 'seek random organism':
                    center = make_function(function_settings['center'])
                    radius = make_function(function_settings['radius'])
                    return lambda organism: organism.parent_ecosystem.biotope.seek_free_location_close_to(
                        center(organism),
                        radius(organism))                                                 
              
    elif number_of_arguments == 2:                
        if is_number(function_settings):
            return lambda predator, prey: function_settings
        elif isinstance(function_settings, str):
            return lambda predator, prey: (
                predator[function_settings](predator) if isinstance(predator[function_settings], FunctionType) else predator[function_settings], 
                prey[function_settings](prey) if isinstance(prey[function_settings], FunctionType) else prey[function_settings])
        elif hasattr(function_settings, '__iter__') and not isinstance(function_settings, dict):
            function_list = [make_function(item, number_of_arguments) for item in function_settings]
            return lambda predator, prey: [item(predator, prey) for item in function_list]
        elif isinstance(function_settings, dict):
            if 'predator' in function_settings:
                return lambda predator, prey: predator[function_settings['predator']](predator) if isinstance(predator[function_settings['predator']], FunctionType) else predator[function_settings['predator']]
            if 'prey' in function_settings:
                return lambda predator, prey: prey[function_settings['prey']](prey) if isinstance(prey[function_settings['prey']], FunctionType) else prey[function_settings['prey']]
            if 'literal' if function_settings:
                return lambda predator, prey: function_settings['literal']
            for operator in Binary_operators_dictionary:
                if operator in function_settings:
                    terms = make_function(function_settings[operator], number_of_arguments)
                    return lambda predator, prey: reduce(Binary_operators_dictionary[operator], [term(predator, prey) for term in terms[1:]], terms[0](predator, prey))        
            for operator in Unary_operators_dictionary:
                if operator in function_settings:
                    argument = make_function(function_settings[operator], number_of_arguments)
                    return lambda predator, prey: Unary_operators_dictionary[operator](argument(predator, prey))
            if 'function' in function_settings:
                if function_settings['function'] == 'gaussian':
                    mean = make_function(function_settings['mean'], number_of_arguments)
                    variance = make_function(function_settings['variance'], number_of_arguments)
                    return lambda predator, prey: gauss(mean(predator, prey), variance(predator, prey))
                elif function_settings['function'] == 'uniform distribution':
                    a = make_function(function_settings['interval'][0], number_of_arguments)
                    b = make_function(function_settings['interval'][1], number_of_arguments)
                    return lambda predator, prey: uniform(a(predator, prey), b(predator, prey))
                elif function_settings['function'] == 'discrete distribution':
                    def choice_value(predator, prey, values_list, r):
                        i = 0
                        while (i < len(values_list) - 1) and (r > values_list[i][0](predator, prey)):
                            i += 1
                            r -= values_list[i][0](predator, prey)
                        return values_list[i][1](predator, prey)
                    values_list = [(make_function(pair['probability'], number_of_arguments),
                                    make_function(pair['value'], number_of_arguments))
                                    for pair in function_settings['values list']]
                    return lambda predator, prey: choice_value(predator, prey, values_list, random())
                elif function_settings['function'] == 'chi-squared distribution':
                    coefficient = make_function(function_settings['coefficient'], number_of_arguments)
                    k = make_function(function_settings['k'], number_of_arguments)
                    return lambda predator, prey: coefficient(predator, prey) * math.fsum(gauss(0, 1)**2 for i in range(k(predator, prey)))                    
    print "Hey, dude! We shouldn't be here!"
    print_dictionary( function_settings )
    return lambda organism: 'Error: unknown function'


""" old version:         
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

            # ITERATION: 
            elif function_settings['type'] == 'iteration':
                operator = make_operator(function_settings['operator'])
                terms = [make_function(term) for term in function_settings['terms']]
                return lambda organism: reduce(operator, [term(organism) for term in terms[1:]], terms[0](organism))    
                   
            # BOOLEAN FUNCTIONS:
            elif function_settings['type'] == 'bolean function':
                left_term = make_function(function_settings['left_term'])
                right_term = make_function(function_settings['right term'])
                operator = make_operator(function_settings['operator'])
                return lambda organism: operator(left_term(organism), right_term(organism))
                    
            # COMPARISON FUNCTIONS:
            elif function_settings['type'] == 'comparison function':
                left_term = make_function(function_settings['left_term'])
                right_term = make_function(function_settings['right term'])
                compare = make_comparison_operator(function_settings['operator'])
                return lambda organism: compare(left_term(organism), right_term(organism))
             
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
                if function_settings['subtype'] == 'threshold':
                    parameter = make_function(function_settings['parameter'])
                    threshold = make_function(function_settings['threshold'])
                    compare = make_operator(function_settings['operator'])
                    return lambda organism: compare(parameter(organism), threshold(organism))
                elif function_settings['subtype'] == 'multiple thresholds':
                    if len(function_settings['terms']) == 0:
                        return 'Error in constraint function from input data'
                    if function_settings['operator'] == 'and':
                        bool_operator = lambda x, y: (x and y)
                    elif function_settings['operator'] == 'or':
                        bool_operator = lambda x, y: (x or y)
                    else:
                        bool_operator = lambda x, y: logical_xor(x, y)
                    terms = [make_function(term) for term in function_settings['terms']]
                    return lambda organism: reduce(bool_operator, [term(organism) for term in terms[1:]], terms[0](organism))    
                elif function_settings['subtype'] == 'hunting':
                    predator_value = make_function(function_settings['predator value'])
                    prey_value = make_function(function_settings['prey value'])
                    comparison = make_comparison_operator(function_settings['operator'])
                    return lambda predator, prey: comparison(predator_value(predator), prey_value(prey))
                                
            # BUILT-IN FUNCTIONS:
            if function_settings['type'] == 'built-in function':
                if function_settings['name'] == 'seek free location':
                    return lambda organism: organism.parent_ecosystem.biotope.seek_free_location() 
                if function_settings['name'] == 'seek free location close to':
                    center = make_function(function_settings['center'])
                    radius = make_function(function_settings['radius'])
                    return lambda organism: organism.parent_ecosystem.biotope.seek_free_location_close_to(
                        center(organism),
                        radius(organism)) 
                if function_settings['name'] == 'seek random organism':
                    center = make_function(function_settings['center'])
                    radius = make_function(function_settings['radius'])
                    return lambda organism: organism.parent_ecosystem.biotope.seek_free_location_close_to(
                        center(organism),
                        radius(organism)) 
        
        # if 'type' is not in function_settings:
        if 'operator' in function_settings:        
            # MATH OPERATIONS:
            elif function_settings['operator'] == '+':
                left_term = make_function(function_settings['left term'])
                right_term = make_function(function_settings['right term'])
                return lambda organism: lef_term(organism) + right_term(organism)
            elif function_settings['operator'] == '-':
                left_term = make_function(function_settings['left term'])
                right_term = make_function(function_settings['right term'])
                return lambda organism: lef_term(organism) - right_term(organism)
            elif function_settings['operator'] == '*':
                left_term = make_function(function_settings['left term'])
                right_term = make_function(function_settings['right term'])
                return lambda organism: lef_term(organism) * right_term(organism)
            elif function_settings['operator'] == '/':
                left_term = make_function(function_settings['left term'])
                right_term = make_function(function_settings['right term'])
                return lambda organism: lef_term(organism) / right_term(organism)
            elif function_settings['operator'] == '**':
                left_term = make_function(function_settings['left term'])
                right_term = make_function(function_settings['right term'])
                return lambda organism: lef_term(organism) ** right_term(organism)
            elif function_settings['operator'] in {'sin', 'sinus'}:
                argument = make_function(function_settings['argument'])
                return lambda organism: math.sin(argument(organism))
            elif function_settings['operator'] in {'cos', 'cosinus'}:
                argument = make_function(function_settings['argument'])
                return lambda organism: math.cos(argument(organism))
            elif function_settings['operator'] in {'tan', 'tangent'}:
                argument = make_function(function_settings['argument'])
                return lambda organism: math.tan(argument(organism))
                        
    elif hasattr(function_settings, '__iter__'):
        function_list = [make_function(item) for item in function_settings]
        return lambda organism: [item(organism) for item in function_list]

    print "Hey, dude! We shouldn't be here!"
    print_dictionary( function_settings )
    return lambda organism: 'Error: unknown function'
"""

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
                


            
            
            
            
            
            
            