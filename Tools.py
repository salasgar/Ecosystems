from random import *
from functools import reduce
from math import *
from copy import *
from Ecosystem_settings import *
from types import FunctionType

print_outlays = False
print_deths = False
print_births = False

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
    
def sigmoid(x):
    if x > 50:
        return 1.0
    elif x < -50:
        return 0.0
    else:
        return exp(x)/(1+exp(x))    
    
    
    
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
    'in': lambda x, y: x in y,
    'randint': randint, # random integer between x and y
    'gauss': gauss,
    'uniform': uniform
}   
for operator in {'and', 'AND', '&', '&&'}:  # Este bucle for es por ahorrarme escribir lineas repetitivas. Lo dejamos asi o lo cambiamos?
    Binary_operators_dictionary[operator] = lambda x, y: x and y
for operator in {'or', 'OR', '|', '||'}:
    Binary_operators_dictionary[operator] = lambda x, y: x or y
for operator in {'xor', 'XOR'}:
    Binary_operators_dictionary[operator] = lambda x, y: (x and not y) or (y and not x)

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
    'not': lambda x: not x}

def make_function(function_settings, number_of_arguments):
    if number_of_arguments == 0:           
        if is_number(function_settings):
            return lambda: function_settings
        elif isinstance(function_settings, str):
            return lambda: function_settings
        elif hasattr(function_settings, '__iter__') and not isinstance(function_settings, dict):
            return [make_function(item, number_of_arguments) for item in function_settings]  # Yes, it's not a function, but a list of functions
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
            if 'choice' in function_settings:
                dictionary = {}
                for item in function_settings:
                    dictionary[item] = make_function(function_settings[item], number_of_arguments)
                parameter = dictionary['choice']
                return lambda: dictionary[parameter()]()               
            if 'tuple' in function_settings:
                tuple_to_return = tuple(make_function(item, number_of_arguments) for item in function_settings['tuple'] )
                return lambda: tuple(item() for item in tuple_to_return)
            if 'function' in function_settings:
                if function_settings['function'] == 'random boolean':
                    if 'probability' in function_settings:
                        probability = make_functions(functions_settings['probability'], number_of_arguments)
                    else:
                        probability = lambda: 0.5
                    return lambda: (probability() > random())
                if function_settings['function'] == 'gaussian':
                    if 'mean' in function_settings['function']:                        
                        mean = make_function(function_settings['mean'], number_of_arguments)
                    else:
                        mean = lambda: 0
                    if 'variance' in function_settings['function']:                        
                        variance = make_function(function_settings['variance'], number_of_arguments)
                    else:
                        variance = lambda: 1
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
                    return lambda: choice_value(values_list, random())
                elif function_settings['function'] == 'chi-squared distribution':
                    coefficient = make_function(function_settings['coefficient'], number_of_arguments)
                    k = make_function(function_settings['k'], number_of_arguments)
                    return lambda: coefficient() * math.fsum(gauss(0, 1)**2 for i in range(k()))                    


    elif number_of_arguments == 1:                
        if is_number(function_settings):
            return lambda organism: function_settings
        elif isinstance(function_settings, str):
            return lambda organism: (organism[function_settings](organism) if isinstance(organism[function_settings], FunctionType) else organism[function_settings]) if function_settings in organism else function_settings
        elif hasattr(function_settings, '__iter__') and not isinstance(function_settings, dict):
            return [make_function(item, number_of_arguments) for item in function_settings] # Yes, it's not a function, but a list of functions
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
            if 'choice' in function_settings:
                dictionary = {}
                for item in function_settings:
                    dictionary[item] = make_function(function_settings[item], number_of_arguments)
                parameter = dictionary['choice']
                return lambda organism: dictionary[parameter(organism)](organism)               
            if 'tuple' in function_settings:
                tuple_to_return = tuple(make_function(item, number_of_arguments) for item in function_settings['tuple'] )
                return lambda organism: tuple(item(organism) for item in tuple_to_return)
            if 'function' in function_settings:
                if function_settings['function'] == 'random boolean':
                    if 'probability' in function_settings:
                        probability = make_function(function_settings['probability'], number_of_arguments)
                    else:
                        probability = lambda organism: 0.5
                    return lambda organism: (probability(organism) > random())
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
                    if 'coefficient' in function_settings:                    
                        coefficient = make_function(function_settings['coefficient'], number_of_arguments)
                    else:
                        coeffidient = lambda organism: 1
                    k = make_function(function_settings['k'], number_of_arguments)
                    return lambda organism: coefficient(organism) * math.fsum(gauss(0, 1)**2 for i in range(k(organism)))                    
                elif function_settings['function'] == 'seek free location':
                    return lambda organism: organism.parent_ecosystem.biotope.seek_free_location() 
                elif function_settings['function'] == 'seek free location close to':
                    if 'center' in function_settings:
                        center = make_function(function_settings['center'], number_of_arguments)
                    else:
                        center = lambda organism: organism['location']
                    radius = make_function(function_settings['radius'], number_of_arguments)
                    return lambda organism: organism.parent_ecosystem.biotope.seek_free_location_close_to(
                        center(organism),
                        radius(organism)) 
                elif function_settings['function'] == 'seek random organism':
                    if 'center' in function_settings:
                        center = make_function(function_settings['center'], number_of_arguments)
                    else:
                        center = lambda organism: organism['location']
                    radius = make_function(function_settings['radius'], number_of_arguments)
                    return lambda organism: organism.parent_ecosystem.biotope.seek_free_location_close_to(
                        center(organism),
                        radius(organism))    
                elif function_settings['function'] == 'basic sigmoid':
                    return lambda x: exp(x)/(1 + exp(x))               
                elif function_settings['function'] == 'sigmoid':
                    if 'homothety' in function_settings:           
                        homothety = make_function(function_settings['homothety'], number_of_arguments)
                    else:
                        homothety = lambda organism: 1
                    if 'translation' in function_settings:           
                        translation = make_function(function_settings['translation'], number_of_arguments)
                    else:
                        translation = lambda organism: 0
                    if 'parameter' in function_settings:           
                        parameter = make_function(function_settings['parameter'], number_of_arguments)
                    else:
                        parameter = lambda organism: random()                  
                    return lambda organism: sigmoid(translation(organism) + parameter(organism) * homothety(organism))               
                              
              
    elif number_of_arguments == 2:                
        if is_number(function_settings):
            return lambda predator, prey: function_settings
        elif isinstance(function_settings, str):
            return lambda predator, prey: (
                (predator[function_settings](predator) if isinstance(predator[function_settings], FunctionType) else predator[function_settings]) if function_settings in predator else function_settings, 
                (prey[function_settings](prey) if isinstance(prey[function_settings], FunctionType) else prey[function_settings]) if function_settings in prey else function_settings)
        elif hasattr(function_settings, '__iter__') and not isinstance(function_settings, dict):
            return [make_function(item, number_of_arguments) for item in function_settings] # Yes, it's not a function, but a list of functions
        elif isinstance(function_settings, dict):
            if 'predator' in function_settings:
                return lambda predator, prey: predator[function_settings['predator']](predator) if isinstance(predator[function_settings['predator']], FunctionType) else predator[function_settings['predator']]
            if 'prey' in function_settings:
                return lambda predator, prey: prey[function_settings['prey']](prey) if isinstance(prey[function_settings['prey']], FunctionType) else prey[function_settings['prey']]
            if 'literal' in function_settings:
                return lambda predator, prey: function_settings['literal']
            for operator in Binary_operators_dictionary:
                if operator in function_settings:
                    terms = make_function(function_settings[operator], number_of_arguments)
                    return lambda predator, prey: reduce(Binary_operators_dictionary[operator], [term(predator, prey) for term in terms[1:]], terms[0](predator, prey))        
            for operator in Unary_operators_dictionary:
                if operator in function_settings:
                    argument = make_function(function_settings[operator], number_of_arguments)
                    return lambda predator, prey: Unary_operators_dictionary[operator](argument(predator, prey))
            if 'choice' in function_settings:
                dictionary = {}
                for item in function_settings:
                    dictionary[item] = make_function(function_settings[item], number_of_arguments)
                parameter = dictionary['choice']
                return lambda predator, prey: dictionary[parameter(predator, prey)](predator, prey)                
            if 'tuple' in function_settings:
                tuple_to_return = tuple(make_function(item, number_of_arguments) for item in function_settings['tuple'] )
                return lambda predator, prey: tuple(item(predator, prey) for item in tuple_to_return)
            if 'function' in function_settings:
                if function_settings['function'] == 'random boolean':
                    if 'probability' in function_settings:
                        probability = make_functions(functions_settings['probability'], number_of_arguments)
                    else:
                        probability = lambda predator, prey: 0.5
                    return lambda predator, prey: (probability(predator, prey) > random())
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
    #print_dictionary( function_settings )
    print function_settings
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
                
def deep_copy_of_a_dictionary(dictionary):
    if isinstance(dictionary, dict):            
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

            
            
            
            
            
            
            